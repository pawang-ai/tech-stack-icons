// Validates icons.json against the rules in CONTRIBUTING.md. No dependencies.
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const VARIANTS = ["original", "original-wordmark", "plain", "plain-wordmark", "line", "line-wordmark"];
const CATEGORIES = ["languages", "frameworks", "databases", "cloud", "devops", "ai", "editors-terminals", "operating-systems", "design", "data-analytics", "seo-webmaster", "messaging", "email", "productivity", "other"];
const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const COLOR = /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/;
const MAX_BYTES = 32 * 1024;
const errors = [];
const err = (m) => errors.push(m);

let catalog;
try {
  catalog = JSON.parse(readFileSync("icons.json", "utf8"));
} catch (e) {
  console.error("icons.json is not valid JSON:", e.message);
  process.exit(1);
}
if (!Array.isArray(catalog)) {
  console.error("icons.json must be an array");
  process.exit(1);
}

const seen = new Set();
for (const [i, icon] of catalog.entries()) {
  const id = icon?.name ?? `#${i}`;
  if (!NAME.test(icon?.name ?? "")) err(`${id}: invalid name (lowercase letters, digits, hyphens)`);
  if (seen.has(icon.name)) err(`${id}: duplicate name`);
  seen.add(icon.name);
  if (!CATEGORIES.includes(icon.category)) err(`${id}: category must be one of ${CATEGORIES.join(", ")}`);
  if (!Array.isArray(icon.tags) || icon.tags.length === 0) err(`${id}: tags must be a non-empty array`);
  if (!COLOR.test(icon.color ?? "")) err(`${id}: color must be a hex value like #61dafb`);
  const svgs = icon.versions?.svg;
  if (!Array.isArray(svgs) || svgs.length === 0) { err(`${id}: versions.svg must be a non-empty array`); continue; }

  for (const v of svgs) {
    if (!VARIANTS.includes(v)) { err(`${id}: unknown variant "${v}"`); continue; }
    const file = join("icons", icon.name, `${icon.name}-${v}.svg`);
    if (!existsSync(file)) { err(`${id}: missing file ${file}`); continue; }
    const text = readFileSync(file, "utf8");
    if (statSync(file).size > MAX_BYTES) err(`${file}: larger than 32 KB`);
    if (!/<svg[^>]*\bviewBox=/.test(text)) err(`${file}: missing viewBox`);
    if (/<script/i.test(text)) err(`${file}: contains <script>`);
    if (/\son[a-z]+\s*=/i.test(text)) err(`${file}: contains an event handler attribute`);
    if (/<image[\s>]/i.test(text) || /data:image\/(png|jpe?g|gif|webp)/i.test(text)) err(`${file}: embeds a raster image`);
    if (/(href|src)\s*=\s*["']https?:/i.test(text)) err(`${file}: references an external resource`);
  }
}

// every icon folder must be listed in the catalog
if (existsSync("icons")) {
  for (const dir of readdirSync("icons")) {
    if (statSync(join("icons", dir)).isDirectory() && !seen.has(dir)) err(`icons/${dir}: folder not listed in icons.json`);
  }
}

if (errors.length) {
  console.error(`\n${errors.length} problem(s) found:\n- ` + errors.join("\n- "));
  process.exit(1);
}
console.log(`OK: ${catalog.length} icon(s) validated.`);
