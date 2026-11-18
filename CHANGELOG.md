# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- 120 badges with custom logos from devicon (MIT) for technologies Simple Icons lacks, such as Adobe Photoshop, Illustrator and After Effects, Heroku, MATLAB, Twilio, DynamoDB and Xamarin. Three new categories: Design & Creative, AI & Data Science, Cloud & Hosting.
- `badgekit probe`, a weekly and on-demand workflow ("Probe badges") that asks Shields.io to render every badge and checks that its logo shows.
- Validation for custom logos: SVG safety (no scripts, images, external references or entities), a 20 KB file limit and a 3000-character badge URL budget.
- `badgekit check` fails if a README grows past 450 KiB (GitHub stops rendering at 500 KiB).
- Google Search Console verification tag, a Pawang Dev credit in both READMEs, and a Discussions link in the issue chooser.

### Fixed

- Custom logo data URIs are now percent-encoded; a raw `+` in a query string is read as a space and corrupts base64.
- `logoColor` is no longer sent for custom logos, which Shields.io cannot recolor.

## [0.1.0] - 2026-11-17

### Added

- Initial catalog of 191 badges in 12 categories, stored in `data/badges.yml`.
- `badgekit` CLI (`build`, `check`, `validate`, `stats`) that generates `README.md`, `README.id.md`, `docs/badges.json` and `docs/llms.txt`.
- Bilingual (English and Bahasa Indonesia) README and CONTRIBUTING.
- Workbench site (`docs/index.html`, plain HTML/CSS/JS, no build step): category shelves, a README tray with copy-all, remove, clear with undo, reordering by drag or arrow keys, a badge style picker with live preview, a light/dark toggle, EN/ID switch, a `/` search shortcut and a mobile bottom sheet.
- "Pawang Lencana" theme: design tokens in `docs/theme.css` with light and dark modes (WCAG AA contrast measured). Follows the system setting and can be forced with `data-theme`.
- SEO, AEO and GEO foundations for the site: keyword-aligned title and description, Open Graph and Twitter cards, `FAQPage` JSON-LD, `sitemap.xml`, `og-image.png`, a "Why this collection" section and a `noscript` fallback.
- Five FAQ entries (40-60 words each) on the site and in both READMEs.
- Footer credit "Design by Pawang Dev" linking to https://www.pawang.dev/ (translated in the ID view).
- CI (lint, tests, Simple Icons slug validation), Pages deploy, Dependabot, issue forms and PR template.
- Manual SemVer release workflow (Actions → Release → patch / minor / major, with `dry_run`).

[Unreleased]: https://github.com/pawang-ai/markdown-badges-collection/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/pawang-ai/markdown-badges-collection/releases/tag/v0.1.0
