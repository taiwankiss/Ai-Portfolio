# Ai Work — Wei's AI Portfolio

Cinematic portfolio for Wei's AI projects: a 3D orbit of project cards on the home page, and a five-chapter deck for each project. Plain HTML, CSS and JS — no build step.

## Editing content

Everything lives in `data.js`:

- `PROJECTS` — one object per project (title, one-line intro, three steps, three stats, tools, link, screenshots, videos)
- `ABOUT` — the About me page (`showcase: true` adds the desktop + mobile résumé chapter)

To add a project, append one object to `PROJECTS`; the orbit and project page lay themselves out.

Media goes in `media/`, named after the project key:

- `<key>-1.webp`, `<key>-2.webp`… — desktop screenshots (2× capture)
- `<key>-m.webp` — mobile screenshot (used on phones)
- `<key>.mp4`, `<key>-m.mp4` — desktop and mobile screen recordings
- `halftone: true` — for sites recorded without their dot texture; the page adds the dots in CSS

## Preview locally

```bash
python3 -m http.server 4174
```

Then open http://localhost:4174.

## Other folders

- `v1/` — the previous bento-style site (built with `python3 v1/tools/build.py`)
- `concepts/` — the other two v2 design directions (Kinetic Index, Bento OS)
