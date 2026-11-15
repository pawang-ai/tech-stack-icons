<div align="center">

<img src="assets/hero.svg" alt="tech-stack-icons: open-source SVG icons for programming languages, frameworks, developer tools, cloud platforms and AI brands" width="100%">

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-7ffbe6?style=for-the-badge&labelColor=0d1630)](LICENSE)
[![Format: SVG](https://img.shields.io/badge/Format-SVG-3ac7ff?style=for-the-badge&labelColor=0d1630)](#quick-start)
[![CDN: jsDelivr](https://img.shields.io/badge/CDN-jsDelivr-8a5cff?style=for-the-badge&labelColor=0d1630)](#use-via-cdn)
[![Icons](https://img.shields.io/badge/Icons-157-5fd0ff?style=for-the-badge&labelColor=0d1630)](icons.json)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ffd84d?style=for-the-badge&labelColor=0d1630)](CONTRIBUTING.md)
[![Request an icon](https://img.shields.io/badge/Request-an%20icon-ff7a9c?style=for-the-badge&labelColor=0d1630)](../../issues/new?template=icon-request.md)

**[Browse the gallery](#)** · **[Quick start](#quick-start)** · **[FAQ](#faq)** · **[Contribute](#contributing)**

</div>

<img src="assets/divider.svg" alt="" width="100%">

## What is tech-stack-icons?

**tech-stack-icons is a free, open-source library of SVG icons for programming languages, frameworks, developer tools, cloud platforms, databases, AI products and popular brands.** Every icon ships in several variants (original, plain, line, wordmark) and works in README files, portfolios, documentation sites and web apps.

Scope rules are in [CONTRIBUTING.md](CONTRIBUTING.md#scope-what-belongs-here). It is built and maintained by [pawang-ai](https://github.com/pawang-ai) and is designed as a drop-in complement to [devicon](https://github.com/devicons/devicon): the same idea, with a wider catalog that includes AI tools, modern frameworks, terminals, editors and more.

## Why use it

- **Wide coverage.** Languages, frameworks, databases, cloud, CI/CD, AI, editors, operating systems, plus data, SEO, messaging, email and office tools.
- **Clean SVG.** Optimized, scalable, no tracking, no runtime dependency.
- **Multiple variants.** Colored and monochrome, with or without wordmark.
- **CDN-ready.** Load any icon by URL, no install needed.
- **Machine-readable.** One `icons.json` with names, aliases, tags and brand colors.
- **Open and permissive.** MIT-licensed code, with a clear trademark policy for logos.

<img src="assets/divider.svg" alt="" width="100%">

## Quick start

### Use via CDN

```html
<img
  src="https://cdn.jsdelivr.net/gh/pawang-ai/tech-stack-icons@main/icons/hono/hono-original.svg"
  alt="Hono"
  width="48"
  height="48"
/>
```

URL pattern:

```text
https://cdn.jsdelivr.net/gh/pawang-ai/tech-stack-icons@main/icons/{name}/{name}-{variant}.svg
```

### Use in a GitHub README

```md
<p align="left">
  <img src="https://cdn.jsdelivr.net/gh/pawang-ai/tech-stack-icons@main/icons/hono/hono-original.svg" width="40" alt="Hono" />
  <img src="https://cdn.jsdelivr.net/gh/pawang-ai/tech-stack-icons@main/icons/whatsapp/whatsapp-original.svg" width="40" alt="WhatsApp" />
  <img src="https://cdn.jsdelivr.net/gh/pawang-ai/tech-stack-icons@main/icons/google-search-console/google-search-console-original.svg" width="40" alt="Google Search Console" />
</p>
```

### Install from npm

```bash
npm install tech-stack-icons
```

```js
import icons from "tech-stack-icons/icons.json";

const hono = icons.find((i) => i.name === "hono");
console.log(hono.versions.svg); // ["original", "plain"]
```

### Copy the SVG

Open any file in [`/icons`](icons) and paste the raw SVG into your project.

<img src="assets/divider.svg" alt="" width="100%">

## Icon variants

| Variant | Description | Typical use |
| --- | --- | --- |
| `original` | Full-color brand logo | Portfolios, READMEs |
| `original-wordmark` | Full-color logo with the name | Tech stack sections |
| `plain` | Single-shape, uses `currentColor` (black when loaded via `<img>`, recolor by inlining the SVG) | Themes, dark mode |
| `plain-wordmark` | Single-shape with the name | Footers, badges |
| `line` | Outline style | Minimal UIs |

## Categories

| Category | Examples |
| --- | --- |
| Programming languages | AssemblyScript, MDX, Scratch |
| Frameworks and libraries | Hono, Preact, LangChain, Pydantic |
| Databases and ORM | Drizzle, ArangoDB, PlanetScale |
| Cloud and hosting | Hetzner, Fly.io, Render, Dropbox |
| CI/CD and DevOps | Dependabot, Snyk, Ruff, JSR |
| AI and machine learning | DeepSeek, Mistral AI, Perplexity, Qwen |
| Editors and terminals | Ghostty, Warp, Sublime Text, Wezterm |
| Operating systems | FreeBSD, Manjaro, Alpine Linux |
| Design | Krita, Dribbble, SketchUp |
| Data and analytics | Google Analytics, Google Sheets, Looker, Hotjar |
| SEO and webmaster tools | Google Search Console, Semrush |
| Messaging | WhatsApp, Telegram, Discord, Zoom |
| Email | Gmail, Proton Mail, Thunderbird, Resend |
| Productivity and office | Notion, Obsidian, Asana |

> The catalog grows with every release. See [`icons.json`](icons.json) for the full, current list.

## Repository structure

```text
tech-stack-icons/
├─ icons/
│  └─ {name}/
│     ├─ {name}-original.svg
│     ├─ {name}-plain.svg
│     └─ {name}-original-wordmark.svg
├─ assets/              # README visuals
├─ icons.json           # catalog: name, altnames, tags, versions, color
├─ CONTRIBUTING.md
├─ CITATION.cff
├─ llms.txt             # summary for AI assistants
└─ LICENSE
```

### `icons.json` entry

```json
{
  "name": "hono",
  "altnames": [
    "hono"
  ],
  "category": "frameworks",
  "tags": [
    "framework",
    "frameworks"
  ],
  "versions": {
    "svg": [
      "original",
      "plain"
    ]
  },
  "color": "#e36002"
}
```

<img src="assets/divider.svg" alt="" width="100%">

## FAQ

### What is tech-stack-icons?
A free, open-source SVG icon library of programming languages, frameworks, tools, cloud platforms and AI brands, available through a CDN, npm or direct download.

### How do I add tech icons to my GitHub README?
Use an `<img>` tag that points to the jsDelivr URL of the icon, as shown in [Quick start](#use-in-a-github-readme). Set `width` to control the size.

### How is it different from devicon?
It follows the same naming and variant conventions, so migration is easy, and it focuses on additional coverage such as newer AI tools, frameworks, terminals and editors. Both projects can be used side by side.

### Can I change an icon's color?
Yes. Inline the SVG and set `fill` on its paths, or use the `plain` variants, which are built for recoloring.

### Can I use the icons commercially?
The repository code and original artwork are MIT-licensed. Brand logos remain the property of their owners and must be used according to each brand's guidelines. See [Trademarks](#trademarks-and-takedown).

### How do I request a missing icon?
[Open an icon request](../../issues/new?template=icon-request.md) with the official name, website and preferred variants.

## Contributing

Contributions are welcome: new icons, fixes, docs and tooling.

1. Fork the repository and create a branch.
2. Add the SVG under `icons/{name}/` following the naming pattern.
3. Add or update the entry in `icons.json`.
4. Open a pull request. CI validates naming, size and SVG structure.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## Trademarks and takedown

All product names, logos and brands are the property of their respective owners. Their use here is for identification only and does not imply endorsement. Follow each brand's usage policy.

If you are a rights holder and want a logo changed or removed, [open an issue](../../issues) or contact the maintainers and it will be handled promptly.

## Credits

Icon artwork in this release is generated from [Simple Icons](https://simpleicons.org) (CC0 1.0). Inspired by [devicon](https://github.com/devicons/devicon) and [md-badges](https://github.com/inttter/md-badges). Thanks to every contributor.

## Citation

If you use this library in research or documentation, cite it using [`CITATION.cff`](CITATION.cff).

## License

Code and original artwork are released under the [MIT License](LICENSE).

<img src="assets/divider.svg" alt="" width="100%">

<div align="center">

Built with care by **[pawang-ai](https://github.com/pawang-ai)**

</div>
