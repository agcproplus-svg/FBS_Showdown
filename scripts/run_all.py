
import os, subprocess, sys
def run(cmd):
    print("▶", " ".join(cmd)); sys.stdout.flush()
    subprocess.check_call(cmd)
if __name__ == "__main__":
    if not os.environ.get("CFB_API_KEY"):
        print("WARNING: CFB_API_KEY not set. fetch_teams/rosters will fail. You can still run generate_cards on existing data.")
    # Optional fetches if you already have scripts; omitted here for brevity.
    # run([sys.executable, "scripts/fetch_teams.py"])
    # run([sys.executable, "scripts/fetch_rosters_and_stats.py"])
    run([sys.executable, "scripts/generate_cards.py"])
    print("Done. data/league.json updated with defense cards and weighted tables.")
