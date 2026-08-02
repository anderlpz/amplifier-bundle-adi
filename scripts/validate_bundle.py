#!/usr/bin/env python3
"""Structural validation for the ADI (amplifier-bundle-adi) bundle.

Guards the exact bug classes that have cost real debugging time on this bundle:

  * A skill whose SKILL.md frontmatter doesn't parse, or whose `name` doesn't
    match its directory -> the skill silently fails to register.
  * The /adi front door losing `user-invocable: true` -> no slash command.
  * `config.skills` wired with the "@namespace:path" MENTION form, which the
    tool-skills mount-time resolver SILENTLY DROPS (it only resolves git+/https
    sources and literal filesystem paths). This made /adi undiscoverable with
    zero error and cost days. We FAIL loudly on it.
  * Broken frontmatter in bundle.md / behaviors / agents / the skill.
  * Leftover references to the deleted recipes/convergence.yaml placeholder.
  * Leftover references to design-intelligence-enhanced (Tier 2 is the official
    design-council).

Uses only the standard library + pyyaml. It does NOT import the amplifier
runtime, so it runs anywhere: `python scripts/validate_bundle.py` or via pytest.

Exits 0 and prints "VALIDATION OK" when clean; exits 1 and prints a
"VALIDATION FAILED" listing otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

BUNDLE_ROOT = Path(__file__).resolve().parent.parent

# The /adi skill directory must exist with these frontmatter guarantees.
FRONT_DELIM = "---"


def _split_frontmatter(text: str) -> str | None:
    """Return the YAML frontmatter block of a markdown file, or None."""
    if not text.startswith(FRONT_DELIM):
        return None
    parts = text.split(FRONT_DELIM, 2)
    if len(parts) < 3:
        return None
    return parts[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_skills(skills_dir: Path) -> list[str]:
    """Every <skills_dir>/<name>/SKILL.md parses and its name matches the dir."""
    errors: list[str] = []
    if not skills_dir.is_dir():
        return [f"skills dir missing: {skills_dir}"]

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append(f"no skill directories found under {skills_dir}")

    for sd in skill_dirs:
        skill_md = sd / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{sd.name}: missing SKILL.md")
            continue
        fm = _split_frontmatter(_read(skill_md))
        if fm is None:
            errors.append(f"{sd.name}: SKILL.md has no parseable frontmatter block")
            continue
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as exc:
            errors.append(f"{sd.name}: SKILL.md frontmatter YAML error: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{sd.name}: SKILL.md frontmatter is not a mapping")
            continue
        name = data.get("name")
        if name != sd.name:
            errors.append(
                f"{sd.name}: SKILL.md name '{name}' does not match directory '{sd.name}'"
            )
    return errors


def validate_adi_front_door(skills_dir: Path) -> list[str]:
    """skills/adi/SKILL.md must be the user-invocable slash-command front door."""
    errors: list[str] = []
    skill_md = skills_dir / "adi" / "SKILL.md"
    if not skill_md.is_file():
        return ["skills/adi/SKILL.md is missing (the /adi front door)"]
    fm = _split_frontmatter(_read(skill_md))
    data = yaml.safe_load(fm) if fm else None
    if not isinstance(data, dict):
        return ["skills/adi/SKILL.md frontmatter did not parse to a mapping"]
    if data.get("user-invocable") is not True:
        errors.append("skills/adi/SKILL.md must set `user-invocable: true`")
    return errors


def _iter_config_skills(node) -> list[str]:
    """Collect every entry under any tools[].config.skills list in a bundle dict."""
    entries: list[str] = []
    tools = node.get("tools") if isinstance(node, dict) else None
    if not isinstance(tools, list):
        return entries
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        cfg = tool.get("config")
        if not isinstance(cfg, dict):
            continue
        skills = cfg.get("skills")
        if isinstance(skills, list):
            entries.extend(str(s) for s in skills)
    return entries


def _is_resolvable_skill_source(entry: str) -> bool:
    """True only for source forms the mount-time resolver actually handles."""
    if entry.startswith(("git+", "http://", "https://")):
        return True
    if entry.startswith("@"):
        # The silently-dropped mention form. Never resolvable.
        return False
    # Otherwise treat it as a filesystem path; it must exist (relative to root).
    candidate = (BUNDLE_ROOT / entry).resolve()
    return candidate.exists()


def validate_skills_tool_wiring(behavior_path: Path) -> list[str]:
    """behaviors/adi.yaml must wire tool-skills with a RESOLVABLE config.skills."""
    errors: list[str] = []
    if not behavior_path.is_file():
        return [f"{behavior_path.name}: missing"]
    try:
        data = yaml.safe_load(_read(behavior_path))
    except yaml.YAMLError as exc:
        return [f"{behavior_path.name}: YAML error: {exc}"]
    if not isinstance(data, dict):
        return [f"{behavior_path.name}: did not parse to a mapping"]

    tools = data.get("tools")
    if not isinstance(tools, list) or not any(
        isinstance(t, dict) and t.get("module") == "tool-skills" for t in tools
    ):
        errors.append(f"{behavior_path.name}: does not wire the tool-skills module")

    skill_entries = _iter_config_skills(data)
    if not skill_entries:
        errors.append(
            f"{behavior_path.name}: tool-skills has no config.skills entries "
            "(the /adi skill would never be discovered)"
        )
    for entry in skill_entries:
        if entry.startswith("@"):
            errors.append(
                f"{behavior_path.name}: config.skills entry '{entry}' uses the "
                "@mention form, which the mount-time resolver SILENTLY DROPS. "
                "Use a git+/https source or an existing local path."
            )
        elif not _is_resolvable_skill_source(entry):
            errors.append(
                f"{behavior_path.name}: config.skills entry '{entry}' is not a "
                "resolvable source (not git+/https, and no such local path)."
            )
    return errors


def validate_frontmatter_parses(paths: list[Path]) -> list[str]:
    """Each markdown/yaml file has frontmatter (or top-level YAML) that parses."""
    errors: list[str] = []
    for p in paths:
        if not p.is_file():
            errors.append(f"{p}: missing")
            continue
        text = _read(p)
        if p.suffix == ".yaml":
            block = text
        else:
            block = _split_frontmatter(text)
            if block is None:
                errors.append(f"{p}: no parseable frontmatter block")
                continue
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            errors.append(f"{p}: YAML error: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{p}: frontmatter did not parse to a mapping")
    return errors


def validate_no_forbidden_references() -> list[str]:
    """No lingering refs to the deleted recipe or the dropped Tier-2 fork."""
    errors: list[str] = []
    forbidden = {
        "recipes/convergence": "deleted placeholder recipe",
        "convergence.yaml": "deleted placeholder recipe",
        "design-intelligence-enhanced": "removed Tier-2 fork (Tier 2 is design-council)",
    }
    exts = {".md", ".yaml", ".yml", ".py"}
    skip_parts = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
    # Meta files that legitimately NAME the forbidden strings to document the
    # invariant (this validator, its test, and the agent/contributor guidance).
    # Scanning them would flag the very rules that forbid the pattern.
    allowlist = {
        (BUNDLE_ROOT / "scripts" / "validate_bundle.py").resolve(),
        (BUNDLE_ROOT / "tests" / "test_bundle_validation.py").resolve(),
        (BUNDLE_ROOT / "AGENTS.md").resolve(),
        (BUNDLE_ROOT / "CONTRIBUTING.md").resolve(),
    }
    for path in BUNDLE_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in exts:
            continue
        if set(path.parts) & skip_parts:
            continue
        if path.resolve() in allowlist:
            continue
        text = _read(path)
        for needle, why in forbidden.items():
            for i, line in enumerate(text.splitlines(), 1):
                if needle in line:
                    rel = path.relative_to(BUNDLE_ROOT)
                    errors.append(f"{rel}:{i}: forbidden reference '{needle}' ({why})")
    return errors


def run_all() -> list[str]:
    skills_dir = BUNDLE_ROOT / "skills"
    errors: list[str] = []
    errors += validate_skills(skills_dir)
    errors += validate_adi_front_door(skills_dir)
    errors += validate_skills_tool_wiring(BUNDLE_ROOT / "behaviors" / "adi.yaml")
    errors += validate_frontmatter_parses(
        [
            BUNDLE_ROOT / "bundle.md",
            BUNDLE_ROOT / "behaviors" / "adi.yaml",
            BUNDLE_ROOT / "agents" / "adi-orchestrator.md",
            BUNDLE_ROOT / "agents" / "quality-gate.md",
            BUNDLE_ROOT / "skills" / "adi" / "SKILL.md",
        ]
    )
    errors += validate_no_forbidden_references()
    return errors


def main() -> int:
    errors = run_all()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("VALIDATION OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
