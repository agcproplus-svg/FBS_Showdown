
import os, json, requests, time
from PIL import Image
from io import BytesIO

OUT_DIR = "img/logos"
TEAMS_FILE = "data/teams_2024.json"

WIKI_API = "https://en.wikipedia.org/w/api.php"

def search_logo(team_name):
    q = f"{team_name} football logo"
    params = {
        "action": "query", "format": "json", "prop": "pageimages",
        "piprop": "original", "generator": "search", "gsrsearch": q, "gsrlimit": 1
    }
    r = requests.get(WIKI_API, params=params, timeout=30)
    if r.status_code != 200:
        return None
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        orig = page.get("original", {})
        if orig.get("source"):
            return orig["source"]
    return None

def download_image(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return Image.open(BytesIO(r.content)).convert("RGBA")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    teams = json.load(open(TEAMS_FILE,"r",encoding="utf-8"))
    for t in teams:
        name = t.get("school") or t.get("name") or t
        team_id = (name.upper().replace(" ","_"))
        out_path = os.path.join(OUT_DIR, f"{team_id}.png")
        if os.path.exists(out_path):
            print("Logo exists:", out_path); continue
        url = search_logo(name)
        if not url:
            print("No logo found for", name); continue
        try:
            img = download_image(url)
            # constrain size
            img.thumbnail((512,512))
            img.save(out_path, "PNG")
            print("Saved", out_path)
        except Exception as e:
            print("Failed logo for", name, e)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
