## Project

Personal academic website for Alexander Jung (Associate Professor for Machine Learning, Aalto University), served at **alexjung.at** via GitHub Pages.

- Built with **Jekyll** (Jekyll Now template, v1.2.0), Kramdown + Rouge, MathJax 3 enabled in [_layouts/default.html](_layouts/default.html).
- Repo name is `MachineLearningForAll.github.io` (User Pages repo); custom domain configured via [CNAME](CNAME) (contains `alexjung.at`; `_config.yml` `url` matches).
- Plugins: `jekyll-sitemap`, `jekyll-feed` (declared under `plugins:` in `_config.yml`).

## Layout

Top-nav pages (nav is hardcoded in [_layouts/default.html](_layouts/default.html) — edit it there when adding pages):
Home (`/`, [index.html](index.html) landing page — there is no blog / `_posts/`) · [about.md](about.md) · [research.md](research.md) · [teaching.md](teaching.md) · [supervision.md](supervision.md) · [books.md](books.md) · [talks.md](talks.md) · [offerings.md](offerings.md)

Other content:
- [offerings.md](offerings.md) is a hub linking to [amlday.md](amlday.md) (`/aml-day/`), [personal-ml-coach.md](personal-ml-coach.md) and [seminare.md](seminare.md) (`/seminare/`, German).
- [mlbook.md](mlbook.md) / [flbook.md](flbook.md) are landing pages for the two Springer textbooks.
- [baukasten/](baukasten/) is a standalone HTML seminar-configurator fed by dictionary terms (see its own commit history).
- Static assets in [images/](images/) and [assets/](assets/).
- Styling: [style.scss](style.scss) compiled via [_sass/](_sass/).

## Conventions when editing

- The thesis list on [supervision.md](supervision.md) (everything between the `theses:begin`/`theses:end` markers) is **generated** from `theses.csv` in the `~/masterthesis` repo via `compile_theses.py --supervision` (run by that repo's `build_site.sh`). Never edit that section by hand — fix the CSV and re-sync. The intro above the markers is hand-written and safe to edit.
- Keep page front-matter minimal: `layout: page`, `title:`, `permalink:`.
- Permalinks are title-based globally (`permalink: /:title/`), but explicit `permalink:` in front-matter overrides.
- **Image/link paths in pages must be absolute** (`/images/foo.png`), never relative — pages live under `/<permalink>/`, so relative paths 404.
- In kramdown, consecutive `**Label**: value` lines need two trailing spaces to render as separate lines.
- Don't commit `.DS_Store` or build artifacts (`_site/`, `.jekyll-cache/`).
- `CLAUDE.md` is in `_config.yml` `exclude:` so it is not published to the live site.

## Local preview

```
bundle exec jekyll serve
```

(Requires a `Gemfile` — not currently in repo; GitHub Pages builds remotely on push.)
