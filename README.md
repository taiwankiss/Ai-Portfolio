# Wei’s AI Portfolio

Bento-style portfolio for Wei’s AI projects. Plain HTML, CSS and JS — no build step needed to host it.

## Editing content

Text and links live in two files:

- `data/site.json` — home page copy, card order, toolkit icons, social links
- `data/projects.json` — each project page (title, summary, sections, images, project link)

After editing, regenerate the pages:

```bash
python3 tools/build.py
```

The email address used by the Email buttons is set at the top of `assets/js/main.js`.

## Preview locally

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.
