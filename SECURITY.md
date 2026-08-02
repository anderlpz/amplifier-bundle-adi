# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in `amplifier-bundle-adi`, please report
it responsibly.

- **Do not** open a public GitHub issue for security-sensitive reports.
- Instead, open a [private security advisory](https://github.com/anderlpz/amplifier-bundle-adi/security/advisories/new)
  on this repository, or contact the maintainer directly through GitHub.

Please include:

- A description of the vulnerability and its impact.
- Steps to reproduce (a minimal proof-of-concept if possible).
- Any relevant version / commit information.

You can expect an initial acknowledgement within a reasonable timeframe. Once the
issue is confirmed, a fix will be prepared and disclosed responsibly.

## Scope

This bundle wraps external tooling (the Impeccable and agent-browser CLIs) and
composes other Amplifier bundles. Vulnerabilities in those upstream projects
should be reported to their respective maintainers; this policy covers ADI's own
code (the `tool-impeccable` / `tool-dom-extract` modules, agents, skill, and
wiring).
