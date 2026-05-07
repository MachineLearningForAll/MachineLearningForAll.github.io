## Project

Personal academic website for Alexander Jung (Associate Professor for Machine Learning, Aalto University), served at **alexjung.at** via GitHub Pages.

- Built with **Jekyll** (Jekyll Now template, v1.2.0), Kramdown + Rouge, MathJax 3 enabled in [_layouts/default.html](_layouts/default.html).
- Repo name is `MachineLearningForAll.github.io` (User Pages repo); custom domain configured via [CNAME](CNAME).
- Plugins: `jekyll-sitemap`, `jekyll-feed`.

## Layout

Top-nav pages (rendered in [_layouts/default.html](_layouts/default.html)):
Blog (`/`) · [about.md](about.md) · [research.md](research.md) · [teaching.md](teaching.md) · [books.md](books.md) · [offerings.md](offerings.md)

Other content:
- [offerings.md](offerings.md) is a hub linking to [amlday.md](amlday.md) (ML Day) and [personal-ml-coach.md](personal-ml-coach.md) (ML Coaching).
- [_posts/](_posts/) holds the blog (currently one welcome post from 2024-11-17).
- Loose `.tex` files at repo root (`crossentropy.tex`, `markovsinequality.tex`, `pmf.tex`, `sample.tex`, `spectraldecomp.tex`) — sources for embedded math content; not auto-rendered by Jekyll. Consider moving to `assets/tex/` or `_tex/`.
- Static assets in [images/](images/) and [assets/](assets/).
- Styling: [style.scss](style.scss) compiled via [_sass/](_sass/).

## Known issues / suggested improvements

1. **CNAME is empty** — only a newline. For `alexjung.at` to work, it must contain `alexjung.at`. This is likely why the domain is currently broken or fallback-routed.
2. **`_config.yml` `url`** is `https://alexjungaalto.github.io/` — should be `https://alexjung.at` so sitemap/feed/canonical URLs are correct.
3. **`feed.title` is "Aalto Dictionary of Machine Learning"** — looks copy-pasted from another project. Should match this site (e.g. "Alexander Jung — Blog").
4. **Google Analytics is commented out** in [_config.yml](_config.yml); enable or remove the include in [_includes/analytics.html](_includes/analytics.html).
5. **`.DS_Store` is committed** — add to [.gitignore](.gitignore) and `git rm --cached` it.
6. **Loose `.tex` files at root** clutter the repo — relocate to a subfolder.
7. **Nav is hardcoded** in [_layouts/default.html](_layouts/default.html); when adding pages, edit it there.

## Adding a "Public Talks" section — recommended

Yes, this is worth adding. The Arbeiterkammer / Volkshochschule / Katholisches Bildungswerk talks are a distinct audience (general public / adult education) from `research` (academic) and `teaching` (university courses) and `offerings` (paid services), so they don't fit cleanly into existing pages.

Suggestion:
- Create `talks.md` with `permalink: /talks/`, `layout: page`, `title: "Public Talks"`.
- Add `<a href="{{ site.baseurl }}/talks">Talks</a>` to the nav in [_layouts/default.html](_layouts/default.html).
- Structure as a reverse-chronological list grouped by venue/series, each entry: date, title, venue (with link), city, language (DE/EN), and optional slides/recording link.
- If the list grows, convert to a Jekyll **collection** (`_talks/` with one file per talk + a listing page) so each talk gets its own URL — useful for sharing and SEO.

Alternative naming: "Outreach" or "Public Engagement" if you want to also include podcasts, panels, op-eds, etc. under one roof.

## Local preview

```
bundle exec jekyll serve
```

(Requires a `Gemfile` — not currently in repo; GitHub Pages builds remotely on push.)

## Conventions when editing

- Keep page front-matter minimal: `layout: page`, `title:`, `permalink:`.
- Permalinks are title-based globally (`permalink: /:title/`), but explicit `permalink:` in front-matter overrides.
- Don't commit `.DS_Store` or build artifacts (`_site/`, `.jekyll-cache/`).
