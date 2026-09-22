## Project

Personal academic website for Alexander Jung (Associate Professor for Machine Learning, Aalto University), served at **alexjung.at** from a Hetzner box (nginx), deployed from this repo by GitHub Actions.

- Built with **Jekyll** (Jekyll Now template, v1.2.0), Kramdown + Rouge, MathJax 3 enabled in [_layouts/default.html](_layouts/default.html).
- Repo name is `MachineLearningForAll.github.io` (User Pages repo). GitHub Pages still builds it as a standby mirror at `machinelearningforall.github.io`, but the live site is the Hetzner deploy; `_config.yml` `url` is `https://alexjung.at` and every page carries a canonical link to it.
- Plugins: `jekyll-sitemap`, `jekyll-feed` (declared under `plugins:` in `_config.yml`).

## Layout

Top-nav pages (nav is hardcoded in [_layouts/default.html](_layouts/default.html) — edit it there when adding pages):
Home (`/`, [index.html](index.html) landing page — there is no blog / `_posts/`) · [about.md](about.md) · [research.md](research.md) · [teaching.md](teaching.md) · [supervision.md](supervision.md) · [books.md](books.md) · [talks.md](talks.md) · [offerings.md](offerings.md) · [service.md](service.md) · [activism.md](activism.md)

Other content:
- [offerings.md](offerings.md) links to [amlday.md](amlday.md) (`/aml-day/`) and [personal-ml-coach.md](personal-ml-coach.md), and contains the German seminar offer under the `#seminare` anchor. [seminare.md](seminare.md) (`/seminare/`) is only a redirect stub pointing there.
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

## Deployment

Every push to `master` runs [.github/workflows/deploy.yml](.github/workflows/deploy.yml): it builds
the site with the pinned `github-pages` gem set and rsyncs `_site/` to `/var/www/alexjung.at/html`
on the Hetzner box (ssh host `dictionaryofml`, 178.105.197.122 — the same box serves
dictionaryofml.org, ml-theses.org and fightacademicbullies.org). Pull requests build without
deploying. Nothing on the box is edited by hand; the repo is the single source of truth.

- The workflow authenticates as the box's `deploy` user with the repo secrets `SSH_PRIVATE_KEY`,
  `SSH_HOST`, `SSH_USER`, `DEPLOY_PATH`. That key is restricted on the box to
  `command="/usr/bin/rrsync /var/www/alexjung.at/html"`, so it can write only that docroot.
- nginx vhost: `/etc/nginx/sites-available/alexjung.at` (apex + a `www` → apex redirect).
  TLS via Let's Encrypt, renewed automatically by certbot's nginx authenticator.
- Because the deploy rsyncs with `--delete`, **anything the box keeps for this site must live
  outside `html/`**. The daily GoAccess report is therefore written to
  `/var/www/alexjung.at/stats/` and served through an nginx `alias` at a non-guessable
  `/stats-df784a5468bdde46/` path (script `/usr/local/bin/goaccess-alexjung-report`, cron
  `/etc/cron.d/goaccess-alexjung`, own log `/var/log/nginx/alexjung.at.access.log`).

## Local preview

```
bundle exec jekyll serve
```

The [Gemfile](Gemfile) pins the `github-pages` gem set, which is what the deploy workflow builds
with — keep it that way so local, CI and the live site agree.
