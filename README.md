# The Flavor Lab — COTHM Culinary Arts Midterm Prep
Static site (no backend). All 285 MCQs live in `data/questions.json`, extracted from the PDF by `scripts/extract.py` and checked against the PDF answer key.

## Run locally
    python scripts/validate.py   # data checks
    python scripts/build.py      # embeds data into index.html
    open index.html              # or: python -m http.server

## Deploy (GitHub Pages)
1. Push this folder to a GitHub repo (branch `main`).
2. Settings → Pages → Source: **GitHub Actions**.
3. The workflow validates, builds and publishes at [https://faseeh56.github.io/Culinary-art-mcqs-preparation/].
Uses relative paths and hash routing (`#/…`), so any repo name and page refresh work. Edit `app.template.html`, then re-run `build.py`.

Progress is saved in this browser's localStorage only (no sync). Export/Import JSON is on the Progress page.
