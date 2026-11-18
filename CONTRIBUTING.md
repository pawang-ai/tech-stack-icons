# Contributing / Kontribusi

**English** · [Bahasa Indonesia](#kontribusi-bahasa-indonesia)

## Contributing (English)

Thanks for helping! Most contributions are one line in `data/badges.yml`.

### Adding a badge

1. Confirm the logo exists on [simpleicons.org](https://simpleicons.org) and note its **slug** and **hex**.
2. Add one line under the right category comment in `data/badges.yml`:

   ```yaml
   - {id: apachekafka, name: "Apache Kafka", slug: apachekafka, hex: "231F20", logo_color: white, category: database}
   ```

3. `logo_color` is `white` on dark colors and `black` on light colors (check the preview).
4. Regenerate and verify:

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   badgekit build
   badgekit check --simple-icons https://cdn.jsdelivr.net/npm/simple-icons/data/simple-icons.json
   ruff check . && black --check . && pytest
   ```

5. Commit `data/badges.yml` together with the regenerated `README.md`, `README.id.md` and `docs/` files.

### Badge criteria

- The product is a real, widely used technology, tool or service.
- `name` is the official product name; `hex` is the official brand color from Simple Icons.
- No duplicates: `badgekit validate` rejects repeated ids, names and slugs.
- Logos missing from Simple Icons can be added with `source: custom` and a single-color SVG under `assets/logos/` (see [`assets/logos/README.md`](assets/logos/README.md)). Shields.io cannot recolor custom logos, so bake the color into the file. `badgekit validate` rejects unsafe SVGs and any badge URL longer than 3000 characters.
- After merging new badges, run **Actions → Probe badges** to confirm each one renders with its logo on Shields.io.

### Workflow and commits

We use [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow): branch from `main`, open a pull request, and squash-merge after CI passes. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org), for example `feat(badges): add Apache Kafka` or `fix(render): escape underscores in labels`.

Never edit `README.md`, `README.id.md`, `docs/badges.json` or `docs/llms.txt` outside the marked sections; the generator owns them. Be kind: see the [Code of Conduct](CODE_OF_CONDUCT.md).

### Releasing (maintainers)

Releases are created from GitHub Actions, never by hand. Go to **Actions → Release → Run workflow** on `main` and choose the bump:

| Bump | Use it for | Example |
|---|---|---|
| `patch` | Fixes and small data corrections | `v0.1.0` → `v0.1.1` |
| `minor` | New badges, categories or features | `v0.1.1` → `v0.2.0` |
| `major` | Breaking changes (renamed ids, changed `badges.json` schema) | `v0.2.0` → `v1.0.0` |

The workflow requires green CI on the commit, creates the `vX.Y.Z` tag and publishes a GitHub release with generated notes. Tick **dry_run** to preview the next version without releasing. Move the finished items from `[Unreleased]` to a new version heading in `CHANGELOG.md` in the pull request that precedes the release.

## Kontribusi (Bahasa Indonesia)

Terima kasih sudah membantu! Sebagian besar kontribusi cukup satu baris di `data/badges.yml`.

### Menambah badge

1. Pastikan logonya ada di [simpleicons.org](https://simpleicons.org), lalu catat **slug** dan **hex**-nya.
2. Tambahkan satu baris di bawah komentar kategori yang tepat di `data/badges.yml` (contoh format ada di bagian English di atas).
3. `logo_color` diisi `white` untuk warna gelap dan `black` untuk warna terang (cek di preview).
4. Regenerasi dan verifikasi dengan perintah yang sama seperti di atas (`badgekit build`, `badgekit check`, `ruff`, `black`, `pytest`).
5. Commit `data/badges.yml` bersama file hasil generate: `README.md`, `README.id.md`, dan `docs/`.

### Kriteria badge

- Produknya teknologi, tool, atau layanan nyata yang banyak dipakai.
- `name` adalah nama resmi produk; `hex` adalah warna brand resmi dari Simple Icons.
- Tidak boleh duplikat: `badgekit validate` menolak id, nama, dan slug yang berulang.
- Logo yang tidak ada di Simple Icons bisa ditambahkan dengan `source: custom` dan SVG satu warna di `assets/logos/` (lihat [`assets/logos/README.md`](assets/logos/README.md)). Shields.io tidak bisa mewarnai ulang logo custom, jadi tanamkan warnanya di file. `badgekit validate` menolak SVG yang tidak aman dan URL badge yang lebih panjang dari 3000 karakter.
- Setelah badge baru ter-merge, jalankan **Actions → Probe badges** untuk memastikan tiap badge tampil beserta logonya di Shields.io.

### Alur kerja dan commit

Kami memakai [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow): buat branch dari `main`, buka pull request, lalu squash-merge setelah CI lulus. Pesan commit mengikuti [Conventional Commits](https://www.conventionalcommits.org), misalnya `feat(badges): add Apache Kafka`.

Jangan mengedit `README.md`, `README.id.md`, `docs/badges.json`, atau `docs/llms.txt` di luar bagian yang bertanda; generator yang mengelolanya. Bersikaplah baik: lihat [Code of Conduct](CODE_OF_CONDUCT.md).

### Rilis (maintainer)

Rilis dibuat lewat GitHub Actions, bukan manual. Buka **Actions → Release → Run workflow** di `main`, lalu pilih jenis kenaikan versi:

| Bump | Dipakai untuk | Contoh |
|---|---|---|
| `patch` | Perbaikan dan koreksi data kecil | `v0.1.0` → `v0.1.1` |
| `minor` | Badge, kategori, atau fitur baru | `v0.1.1` → `v0.2.0` |
| `major` | Perubahan yang merusak kompatibilitas (id diganti, skema `badges.json` berubah) | `v0.2.0` → `v1.0.0` |

Workflow mewajibkan CI hijau pada commit tersebut, membuat tag `vX.Y.Z`, dan menerbitkan GitHub release dengan catatan otomatis. Centang **dry_run** untuk melihat versi berikutnya tanpa merilis. Pindahkan item yang selesai dari `[Unreleased]` ke heading versi baru di `CHANGELOG.md` lewat pull request sebelum rilis.
