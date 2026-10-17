# Security policy

## Supported versions

Only the latest release receives fixes.

## Reporting a vulnerability

Please **don't open a public issue** for security problems. Report them privately through GitHub's private vulnerability reporting:

**https://github.com/Mihirajmera/grc-risk-dashboard/security/advisories/new**

What to expect:

- **Acknowledgement within 5 business days.**
- **An assessment within 14 days**: whether it's accepted as a vulnerability, its severity, and a planned fix.
- **Coordinated disclosure**: a fix is released and the advisory published together, normally within 90 days of the report. You'll be credited in the advisory unless you'd rather not be.

## Scope

A local Streamlit app over a SQLite risk register. Especially relevant: SQL injection through dashboard inputs or unsafe handling of uploaded data.

## Supply chain

GitHub Actions are pinned to commit SHAs, dependencies are pinned by hash, and CodeQL, OpenSSF Scorecard and Dependabot run on this repository.
