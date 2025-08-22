
import json, random

IN = "data/players_by_team.json"
OUT = "data/league.json"

def clamp(n, lo, hi): return max(lo, min(hi, n))

def fill_grid(weights):
    labels = list(weights.keys())
    totalw = sum(weights.values()) or 1
    counts = {k: round(36 * (weights[k] / totalw)) for k in labels}
    s = sum(counts.values())
    while s < 36:
        best = max(labels, key=lambda k: weights[k]); counts[best]+=1; s+=1
    while s > 36:
        worst = max(counts, key=lambda k: counts[k]); counts[worst]-=1; s-=1
    cells = []
    for k in labels: cells += [k]*counts[k]
    random.Random(42).shuffle(cells)
    # Return as 2d6 map 2..12
    # Convert 36 cells to 11 outcomes: we’ll just map by frequency across sums
    # Probabilities of sums: 2:1,3:2,4:3,5:4,6:5,7:6,8:5,9:4,10:3,11:2,12:1
    probs = {2:1,3:2,4:3,5:4,6:5,7:6,8:5,9:4,10:3,11:2,12:1}
    res = {}
    idx = 0
    for ssum in range(2,13):
        take = probs[ssum]
        chunk = cells[idx:idx+take]; idx += take
        # choose most common label in this chunk
        if not chunk: res[str(ssum)] = "0"
        else:
            label = max(set(chunk), key=chunk.count)
            res[str(ssum)] = label
    return res

def generate_rb_card(stats):
    ypc = clamp(stats.get("ypc", 4.2), 2.0, 7.0)
    fum = clamp(stats.get("fum_rate", 0.01), 0, 0.05)
    tdr = clamp(stats.get("td_rate", 0.02), 0, 0.12)
    posBias = (ypc - 3.5) / 3.5
    big = clamp(6 + round(6*posBias), 1, 10)
    plus5 = clamp(10 + round(8*posBias), 3, 14)
    plus2 = clamp(10 + round(4*posBias), 6, 14)
    zero = clamp(6 - round(3*posBias), 2, 12)
    minus2 = clamp(3 - round(3*posBias), 0, 8)
    minus5 = clamp(1 - round(2*posBias), 0, 6)
    fSquares = clamp(round(36 * fum), 0, 3)
    tdSquares = clamp(round(36 * tdr), 0, 4)
    weights = {'BIG': big, '+5': plus5, '+2': plus2, '0': zero, '-2': minus2, '-5': minus5, 'FUM': fSquares, 'TD': tdSquares}
    return fill_grid(weights)

def generate_qb_card(stats):
    c = clamp(stats.get("cmpPct", 0.62), 0.45, 0.75)
    y = clamp(stats.get("ypa", 7.5), 4.0, 10.0)
    i = clamp(stats.get("intRate", 0.02), 0, 0.06)
    s = clamp(stats.get("sackRate", 0.02), 0, 0.12)
    t = clamp(stats.get("tdRate", 0.03), 0, 0.12)
    incSquares = round(36 * (1 - c))
    big = clamp(round((y - 7) * 3), 1, 8)
    plus5 = clamp(10 + round((y - 7) * 4), 6, 16)
    plus2 = clamp(8 + round((y - 7) * 2), 4, 12)
    zero = clamp(6 - round((y - 7) * 2), 1, 10)
    intSquares = clamp(round(36 * i), 0, 3)
    sackSquares = clamp(round(36 * s), 0, 4)
    tdSquares = clamp(round(36 * t), 0, 4)
    weights = {'INC': incSquares, 'BIG': big, '+5': plus5, '+2': plus2, '0': zero, 'INT': intSquares, 'SACK': sackSquares, 'TD': tdSquares}
    return fill_grid(weights)

def generate_receiver_card(stats):
    ypt = clamp(stats.get("ypt", 8.0), 5.0, 12.0)
    cp = clamp(stats.get("catchPct", 0.6), 0.4, 0.85)
    tdr = clamp(stats.get("tdRate", 0.02), 0, 0.2)
    big = clamp(round((ypt - 7) * 3), 0, 8)
    plus5 = clamp(10 + round((ypt - 7) * 3), 4, 16)
    plus2 = clamp(10 + round((ypt - 7) * 1.5), 4, 12)
    zero = clamp(6 - round((ypt - 7) * 2), 0, 10)
    incSquares = clamp(round(36 * (1 - cp) * 0.5), 0, 6)
    tdSquares = clamp(round(36 * tdr), 0, 4)
    weights = {'BIG': big, '+5': plus5, '+2': plus2, '0': zero, 'INC': incSquares, 'TD': tdSquares}
    return fill_grid(weights)

def derive_rates(stats):
    s = stats or {}
    pass_att = s.get("passingAttempts") or s.get("passAtt") or s.get("pass_att") or 0
    pass_cmp = s.get("passingCompletions") or s.get("passCmp") or s.get("pass_cmp") or 0
    pass_yds = s.get("passingYards") or s.get("passYards") or 0
    pass_td = s.get("passingTD") or s.get("pass_td") or 0
    pass_int = s.get("passingInt") or s.get("passInt") or 0
    rush_att = s.get("rushingAttempts") or s.get("rushAtt") or 0
    rush_yds = s.get("rushingYards") or s.get("rushYards") or 0
    rush_td = s.get("rushingTD") or s.get("rush_td") or 0
    rec = s.get("receptions") or s.get("rec") or 0
    rec_tgt = s.get("targets") or s.get("tgt") or max(rec*1.4, 0)  # estimate
    rec_yds = s.get("receivingYards") or s.get("recYards") or 0
    rec_td = s.get("receivingTD") or s.get("rec_td") or 0
    fumbles = s.get("fumbles") or 0
    rates = {}
    if pass_att >= 10:
        rates['cmpPct'] = pass_cmp / pass_att if pass_att else 0.62
        rates['ypa'] = pass_yds / pass_att if pass_att else 7.5
        rates['intRate'] = pass_int / pass_att if pass_att else 0.02
        rates['tdRate'] = pass_td / pass_att if pass_att else 0.03
    if rush_att >= 10:
        rates['ypc'] = rush_yds / rush_att if rush_att else 4.2
        rates['fum_rate'] = fumbles / rush_att if rush_att else 0.01
        rates['td_rate'] = rush_td / rush_att if rush_att else 0.02
    if rec_tgt >= 10:
        rates['ypt'] = rec_yds / (rec_tgt or 1)
        rates['catchPct'] = rec / (rec_tgt or 1) if rec_tgt else 0.6
        rates['tdRate'] = rec_td / (rec_tgt or 1) if rec_tgt else 0.03
    return rates

def card_for_player(p):
    pos = (p.get("position") or "").upper()
    stats = p.get("stats_api") or {}
    rates = derive_rates(stats)
    if "QB" in pos:
        return generate_qb_card(rates)
    elif pos in ("RB","HB","FB"):
        return generate_rb_card(rates)
    else:
        return generate_receiver_card(rates)

def synthetic_defense_card():
    # Placeholder balanced defense tables; replace with real team-allowed stats in future.
    # Run defense outcomes
    run = {str(s): lab for s, lab in zip(range(2,13), [
        "STUFF","TFL","TACKLE","TACKLE","TACKLE","TACKLE","TACKLE","TACKLE","TFL","TACKLE","STUFF"
    ])}
    # Pass defense outcomes
    pdef = {str(s): lab for s, lab in zip(range(2,13), [
        "PBU","SACK","PBU","PBU","PBU","PBU","PBU","INT","PBU","SACK","PBU"
    ])}
    return {"run": run, "pass": pdef}

def main():
    src = json.load(open(IN,"r",encoding="utf-8"))
    out = {"season": src.get("season", 2024), "division":"D1-FBS", "teams":[]}
    for t in src.get("teams", []):
        team = {"id":t["id"],"name":t["name"],"conf":t.get("conf"),
                "logo": f"img/logos/{t['id']}.png", "players":{}, "defense": synthetic_defense_card()}
        for p in t.get("players", []):
            team["players"][p["name"]] = {
                "position": p.get("position","UNK"),
                # For frontend: convert card grid to simple 2d6 map; here we already produce 2d6 maps
                "run": card_for_player(p),  # Using same generator; could split by play type in future
                "pass": card_for_player(p)
            }
        out["teams"].append(team)
    with open(OUT,"w",encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
