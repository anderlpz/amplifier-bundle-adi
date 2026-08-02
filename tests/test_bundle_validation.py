"""Anti-regression acceptance gate for the ADI (amplifier-bundle-adi) bundle.

Guards the exact bug classes that cost real debugging time: dropped skills, the
/adi front door losing user-invocability, the silently-broken "@mention" skill
source form, unparseable frontmatter, and leftover references to removed pieces
(the deleted convergence recipe, the removed design-intelligence-enhanced Tier-2
fork).

Runnable two ways, with only stdlib + pyyaml (no amplifier runtime imports):

    python -m pytest tests/test_bundle_validation.py
    python tests/test_bundle_validation.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_bundle import (  # pyright: ignore[reportMissingImports]
    BUNDLE_ROOT,
    run_all,
    validate_adi_front_door,
    validate_frontmatter_parses,
    validate_no_forbidden_references,
    validate_skills,
    validate_skills_tool_wiring,
)

SKILLS_DIR = BUNDLE_ROOT / "skills"
BEHAVIOR = BUNDLE_ROOT / "behaviors" / "adi.yaml"


class TestBundleValidation(unittest.TestCase):
    def test_all_skills_parse_and_names_match_dirs(self):
        errors = validate_skills(SKILLS_DIR)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_adi_front_door_is_user_invocable(self):
        errors = validate_adi_front_door(SKILLS_DIR)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_skills_tool_wiring_uses_resolvable_source(self):
        errors = validate_skills_tool_wiring(BEHAVIOR)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_core_frontmatter_parses(self):
        errors = validate_frontmatter_parses(
            [
                BUNDLE_ROOT / "bundle.md",
                BUNDLE_ROOT / "behaviors" / "adi.yaml",
                BUNDLE_ROOT / "agents" / "adi-orchestrator.md",
                BUNDLE_ROOT / "agents" / "quality-gate.md",
                BUNDLE_ROOT / "skills" / "adi" / "SKILL.md",
            ]
        )
        self.assertEqual(errors, [], "\n".join(errors))

    def test_no_forbidden_references(self):
        errors = validate_no_forbidden_references()
        self.assertEqual(errors, [], "\n".join(errors))

    def test_full_run_is_clean(self):
        errors = run_all()
        self.assertEqual(errors, [], "\n".join(errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
