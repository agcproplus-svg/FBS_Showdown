
# FBS Showdown — Full Data Pipeline

This package contains:
- Frontend: `index.html`, `css/`, `js/`, `data/`
- Scripts: fetch 2024 FBS teams/rosters/stats, generate 6×6 cards, and download team logos.

## 1) Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r scripts/requirements.txt
export CFB_API_KEY="YOUR_COLLEGEFOOTBALLDATA_API_KEY"  # Windows PowerShell: $env:CFB_API_KEY="..."
```

## 2) Run everything
```bash
python scripts/run_all.py
```
Outputs:
- `data/teams_2024.json`
- `data/players_by_team.json`
- `data/league.json` (the file the game uses)
- `img/logos/*.png` (team logos; verify licensing before public use)

## 3) Test locally
Open `index.html` in your browser (or use a static server).

## 4) Deploy to GitHub Pages
1. Create a new repo on GitHub (public).
2. Upload **all files and folders** (ensure `index.html` is at repo root).
3. Repo → **Settings** → **Pages** → Branch: `main`, Folder: `/root` → Save.
4. Visit `https://<username>.github.io/<repo-name>/` after a minute.

## Notes
- Your API key should never be committed to the repo.
- The Wikipedia logo fetch is best-effort and may return images with licenses not suitable for commercial/public use. Verify or replace with your own assets before publishing.
- Tweak card generation in `scripts/generate_cards.py` to change balance.
