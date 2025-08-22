
import os, json, time, requests
from tqdm import tqdm

API_KEY = os.environ.get('CFB_API_KEY')
if not API_KEY:
    raise SystemExit("Set CFB_API_KEY environment variable.")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

SEASON = 2024
TEAMS_FILE = "data/teams_2024.json"
OUT = "data/players_by_team.json"

def fetch_roster(team_name, year=SEASON):
    url = "https://api.collegefootballdata.com/roster"
    params = {"school": team_name, "year": year}
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_player_season(player_id, year=SEASON):
    # aggregated per-season stats for the player
    url = "https://api.collegefootballdata.com/player/season"
    params = {"id": player_id, "season": year}
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if r.status_code == 200:
        try:
            return r.json()
        except Exception:
            return {}
    return {}

def main():
    teams = json.load(open(TEAMS_FILE, "r", encoding="utf-8"))
    league = {"season": SEASON, "teams": []}
    for t in tqdm(teams):
        school = t.get("school") or t.get("name") or t
        try:
            roster = fetch_roster(school, SEASON)
        except Exception as e:
            print("Roster fetch failed for", school, e)
            roster = []
        players = []
        for p in roster:
            pid = p.get("id") or p.get("playerId") or p.get("athleteId") or None
            name = " ".join([p.get('firstName','').strip(), p.get('lastName','').strip()]).strip() or p.get('name') or "Unknown"
            if pid is None:
                pid = (school + "_" + name).replace(" ", "_")
            stats = {}
            try:
                stats = fetch_player_season(pid, SEASON)
            except Exception:
                stats = {}
            players.append({
                "id": f"{school.upper().replace(' ','_')}_{pid}",
                "name": name,
                "position": (p.get("position") or p.get("pos") or "UNK").upper(),
                "teamId": school.upper().replace(" ","_"),
                "teamName": school,
                "stats_api": stats
            })
            time.sleep(0.05)
        league["teams"].append({
            "id": school.upper().replace(" ","_"),
            "name": school,
            "conf": t.get("conference"),
            "players": players
        })
        time.sleep(0.2)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(league, f, indent=2)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
