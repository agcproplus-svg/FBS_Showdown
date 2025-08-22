
import os, subprocess, sys, time

def run(cmd):
    print("▶", " ".join(cmd)); sys.stdout.flush()
    subprocess.check_call(cmd)

if __name__ == "__main__":
    # Ensure API key
    if not os.environ.get("CFB_API_KEY"):
        print("ERROR: Set CFB_API_KEY environment variable.")
        sys.exit(1)
    # Step 1: teams
    run([sys.executable, "scripts/fetch_teams.py"])
    # Step 2: rosters + stats
    run([sys.executable, "scripts/fetch_rosters_and_stats.py"])
    # Step 3: generate cards + league.json
    run([sys.executable, "scripts/generate_cards.py"])
    # Step 4: fetch logos (best-effort)
    run([sys.executable, "scripts/fetch_logos.py"])
    print("All done. Your data/league.json and img/logos/ are ready.")
