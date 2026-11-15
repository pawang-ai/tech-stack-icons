// Adds an icon from the Simple Icons package (CC0) to icons/ and icons.json.
// Usage: npm i -D simple-icons && node scripts/add-from-simple-icons.mjs <simple-icons-slug> <category> [tag ...]
// Example: node scripts/add-from-simple-icons.mjs googlesearchconsole seo-webmaster seo google
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import * as si from "simple-icons";

const [slug, category, ...tags] = process.argv.slice(2);
if (!slug || !category) {
  console.error("Usage: node scripts/add-from-simple-icons.mjs <simple-icons-slug> <category> [tag ...]");
  process.exit(1);
}
const icon = Object.values(si).find((i) => i && i.slug === slug);
if (!icon) { console.error(`No Simple Icons entry with slug "${slug}"`); process.exit(1); }

const name = icon.title.toLowerCase().replace(/&/g, "and").replace(/\+/g, "plus").replace(/\./g, "dot")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const title = icon.title.replace(/&/g, "&amp;");
const svg = (fill) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img"><title>${title}</title><path fill="${fill}" d="${icon.path}"/></svg>\n`;

const dir = `icons/${name}`;
mkdirSync(dir, { recursive: true });
writeFileSync(`${dir}/${name}-original.svg`, svg(`#${icon.hex.toLowerCase()}`));
writeFileSync(`${dir}/${name}-plain.svg`, svg("currentColor"));

const catalog = JSON.parse(readFileSync("icons.json", "utf8")).filter((i) => i.name !== name);
catalog.push({
  name, altnames: [slug].filter((a) => a !== name), category,
  tags: [...new Set([category, ...tags])].sort(),
  versions: { svg: ["original", "plain"] }, color: `#${icon.hex.toLowerCase()}`,
});
catalog.sort((a, b) => a.name.localeCompare(b.name));
writeFileSync("icons.json", JSON.stringify(catalog, null, 2) + "\n");
console.log(`Added ${name} (${category}). Now run: npm run validate`);
