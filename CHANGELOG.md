# Changelog

## Unreleased

- **Security:** Pillow 13.0.0 (about 24 advisories, 2 critical), certifi 2026.10.19 (removes CA roots with compromised intermediate keys) and Streamlit 1.66.1, the first release that allows Pillow 13. These three are allowed past the two-week release cutoff on purpose; nothing else changed.
- Replaced the deprecated `use_container_width` with `width="stretch"`.
- Live demo on GitHub Pages: the unmodified Streamlit app runs in the browser with stlite, deployed by `.github/workflows/pages.yml`.

## 1.0.0 (2026-10-17)

First tagged release. Streamlit risk register and KRI/KPI dashboard over SQLite.

- CI on Python 3.11 / current Terraform tooling with every GitHub Action pinned to a commit SHA
- Dependencies pinned by version and hash (`requirements.in` → `requirements.txt`)
- CodeQL, OpenSSF Scorecard and Dependabot
- Security policy with private vulnerability reporting
