# The site is built with the same gem set GitHub Pages used to build it, so the
# self-hosted build on alexjung.at renders byte-for-byte like the old one --
# this pulls in the GitHub Pages default plugins the site relies on
# (jekyll-titles-from-headings, jekyll-relative-links, ...) alongside the
# jekyll-sitemap / jekyll-feed listed in _config.yml.
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins

# Windows/JRuby do not ship zoneinfo; not needed on macOS or the CI runner.
gem "webrick", "~> 1.8"
