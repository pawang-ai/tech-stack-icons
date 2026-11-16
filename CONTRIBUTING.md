# Contributing to tech-stack-icons

Thanks for helping. New icons, fixes, docs and tooling are all welcome.

## Scope: what belongs here

The goal is the most complete SVG icon library for technology. Any technology, tool, service, platform or brand that people show in a tech stack, portfolio, documentation or product belongs here.

| Category (`category` value) | Examples |
| --- | --- |
| `languages` | JavaScript, Python, Go, Rust |
| `frameworks` | React, Next.js, Hono, Django |
| `databases` | PostgreSQL, MongoDB, Redis |
| `cloud` | AWS, Cloudflare, Vercel, Fly.io |
| `devops` | GitHub Actions, Docker, Terraform |
| `ai` | Claude, Hugging Face, Ollama |
| `editors-terminals` | VS Code, Neovim, Ghostty |
| `operating-systems` | Linux, Arch, FreeBSD |
| `design` | Figma, Blender, Krita |
| `data-analytics` | Excel, Power BI, Google Analytics, Microsoft Clarity |
| `seo-webmaster` | Google Search Console, Bing Webmaster Tools, Ahrefs, Semrush |
| `messaging` | WhatsApp, Telegram, Slack, Discord |
| `email` | Gmail, Outlook, Proton Mail, Resend |
| `productivity` | Word, PowerPoint, Notion, Obsidian |
| `social-media` | GitHub, LinkedIn, YouTube, Reddit |
| `finance` | PayPal, Stripe, Bitcoin, Visa |
| `entertainment-gaming` | Steam, Spotify, Twitch |
| `education` | Udemy, Coursera, freeCodeCamp |
| `other` | Anything that fits none of the above |

New icons from Simple Icons or devicon that are already in the catalog should not be added twice. Pick a more specific category than `other` whenever one fits; recategorizing existing icons is a welcome contribution.

**Naming:** use the product's own name, and prefix with the vendor when the name is ambiguous. Example: `microsoft-clarity` (analytics) versus `clarity` (smart contract language).

## Add an icon

1. Fork the repository and create a branch named `icon/{name}`.
2. Create `icons/{name}/` where `{name}` is lowercase letters, digits and hyphens only (for example `nextjs`, `github-actions`).
3. Add at least one SVG named `{name}-{variant}.svg`. Allowed variants:
   `original`, `original-wordmark`, `original-wordmark-dark` (wordmark for dark backgrounds), `plain`, `plain-wordmark`, `line`, `line-wordmark`.
4. Add an entry to `icons.json`, including a valid `category` (see the schema in `icons.schema.json`).
5. Run `npm run validate` and fix anything it reports.
6. Open a pull request and fill in the template.

## SVG rules

- Must have a `viewBox`. Prefer a square one (`0 0 24 24` or `0 0 128 128`).
- No `<script>`, event handlers (`onclick`, ...), external references or embedded raster images.
- Optimized: no editor metadata, no hidden layers. Keep each file under 32 KB (hard limit 400 KB).
- `plain` variants should use a single fill so they can be recolored.
- Draw or source the artwork from files you have the right to use. Set `"source": "contributed"` for new icons, and keep third-party licenses in `NOTICE.md`.

## icons.json entry

```json
{
  "name": "react",
  "category": "frameworks",
  "altnames": ["reactjs"],
  "tags": ["framework", "javascript", "frontend"],
  "versions": { "svg": ["original", "plain", "line"] },
  "color": "#61dafb"
}
```

## Add an icon quickly from Simple Icons

```bash
npm i -D simple-icons
node scripts/add-from-simple-icons.mjs googlesearchconsole seo-webmaster seo google
npm run validate
```

Simple Icons is CC0, but each logo is still a trademark of its owner.

## Request an icon

Open an [icon request](../../issues/new?template=icon-request.md) with the official name, website and preferred variants.

## Trademarks

Logos belong to their owners. If a rights holder asks for a change or removal, we will act promptly.

## Code of conduct

Be respectful and constructive. Harassment is not tolerated.
