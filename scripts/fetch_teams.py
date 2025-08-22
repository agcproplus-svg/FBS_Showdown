
import os, requests, json

API_KEY = os.environ.get('CFB_API_KEY')
if not API_KEY:
    raise SystemExit("Set CFB_API_KEY environment variable.")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
OUT = "data/teams_2024.json"

def get_fbs_teams(season=2024):
    url = f"https://api.collegefootballdata.com/teams/fbs?year={season}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    teams = get_fbs_teams(2024)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(teams, f, indent=2)
    print(f"Wrote {len(teams)} teams to {OUT}")
