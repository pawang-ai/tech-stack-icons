# Custom logos

These single-color SVG logos come from [devicon](https://github.com/devicons/devicon) v2.18.0 (MIT, see
[`LICENSE-devicon`](LICENSE-devicon)). Each file was converted for use as a Shields.io custom logo:

- the `plain` variant was used (or the `original` variant when it already had a single fill color),
- every fill was replaced with one color (white or black, chosen for contrast against the badge color),
- the paths were optimized with [SVGO](https://github.com/svg/svgo) at the lowest coordinate precision
  that keeps the shape within 1.5% of the original (measured by pixel overlap).

Shields.io does not recolor custom logos, so the color is baked into each file. Logos and brand names
belong to their respective owners.

To add one, put a single-color SVG here and reference it from `data/badges.yml` with `source: custom` and
`logo_file`. `badgekit validate` checks that the file is a safe SVG and that the badge URL stays within the
length budget.
