
// ======= Configurable Weights & Modifiers =======
const CONFIG = {
  offenseWeights: {
    // Outcome normalization weights (used when building synthetic tables)
    // Not used to overwrite existing 2d6 tables, but can tweak mapping later.
    BIG: 6, "+5": 10, "+2": 10, "0": 6, "-2": 3, "-5": 1, "FUM": 1, "TD": 2,
    "INC": 10, "SACK": 2, "INT": 1
  },
  defenseBias: {
    // How defense outcomes bias offense result
    // map(defOutcome, offenseOutcome) -> newOutcome (high-level)
    STUFF: { Run: { "+5":"0", "+2":"-2", "0":"-2", "BIG":"+2" }, Pass: {} },
    TFL:   { Run: { "+5":"-2", "+2":"-5", "0":"-5", "BIG":"0" }, Pass: {} },
    TACKLE:{ Run: { "+5":"+2", "+2":"0",  "0":"0" }, Pass: {} },
    PBU:   { Pass: { "COMP":"INC", "+5":"INC", "+2":"INC", "BIG":"INC" }, Run: {} },
    SACK:  { Pass: { "COMP":"SACK", "INC":"SACK", "BIG":"SACK", "+5":"SACK", "+2":"SACK", "0":"SACK" }, Run: {} },
    INT:   { Pass: { "COMP":"INT", "BIG":"INT", "+5":"INT", "+2":"INT" }, Run: {} },
  },
  situationModifiers: {
    // Adjust outcomes by situation
    // Keys: down (1-4), distance: short/medium/long, field: own/mid/redzone
    thirdLong: { Pass: { "COMP":"+2", "INC":"INC", "SACK":"SACK", "INT":"INT", "BIG":"+5" },
                 Run:  { "+5":"+2", "+2":"0", "BIG":"+2" } },
    redZone:   { Pass: { "BIG":"+5" }, Run: { "+5":"+2" } },
    goalToGo:  { Pass: { "BIG":"+5", "+5":"+2" }, Run: { "BIG":"+5", "+5":"+2" } }
  }
};

function normalizeOutcomeLabel(text, isPass){
  // Map free-form text to canonical category for biasing
  const t = (text||"").toUpperCase();
  if (t.includes("TD")) return "TD";
  if (t.includes("FUM")) return "FUM";
  if (t.includes("INT")) return "INT";
  if (t.includes("SACK")) return "SACK";
  if (t.includes("INC")) return "INC";
  if (t.includes("BIG")) return "BIG";
  if (t.includes("+5")) return "+5";
  if (t.includes("+2")) return "+2";
  if (t.includes("-5")) return "-5";
  if (t.includes("-2")) return "-2";
  if (t.includes("NO GAIN") || t === "0" || t === "0 YARDS") return "0";
  if (isPass){
    if (t.includes("COMP") || t.match(/\bYARDS?\b/)) return "COMP"; // generic completion bucket
  }
  // Try to parse yards
  const m = t.match(/(-?\d+)\s*YARDS?/);
  if (m){
    const y = parseInt(m[1],10);
    if (y >= 15) return "BIG";
    if (y >= 5) return "+5";
    if (y >= 1) return "+2";
    if (y === 0) return "0";
    if (y <= -5) return "-5";
    return "-2";
  }
  return isPass ? "INC" : "0";
}

function applyDefenseBias(offenseLabel, defLabel, playType){
  const table = CONFIG.defenseBias[defLabel];
  if (!table) return offenseLabel;
  const map = table[playType] || {};
  return map[offenseLabel] || offenseLabel;
}

function applySituation(offenseLabel, playType, situation){
  const { down, distance, field } = situation;
  // third & long
  if (down === 3 && distance === "long"){
    const m = CONFIG.situationModifiers.thirdLong[playType] || {};
    return m[offenseLabel] || offenseLabel;
  }
  // red zone (inside 20)
  if (field === "redzone"){
    const m = CONFIG.situationModifiers.redZone[playType] || {};
    return m[offenseLabel] || offenseLabel;
  }
  // goal-to-go (distance short and redzone and down<=4)
  if (field === "redzone" && distance === "short"){
    const m = CONFIG.situationModifiers.goalToGo[playType] || {};
    return m[offenseLabel] || offenseLabel;
  }
  return offenseLabel;
}

// Resolve a 2d6 table stored as { "2": "...", ..., "12": "..." }
function resolveFromTable(table){
  const roll = roll2d6();
  return { roll, outcome: table[String(roll)] || "0" };
}

// Get defense outcome from team defense card
function resolveDefense(defCard, playType){
  const table = (playType === "Run") ? defCard.run : defCard.pass;
  if (!table) return { roll: null, label: null, text: null };
  const r = resolveFromTable(table);
  return { roll: r.roll, label: (r.outcome||"").toUpperCase(), text: r.outcome };
}

function renderFinalText(playerName, playType, offRoll, defRoll, offenseText, finalLabel){
  let detail = "";
  switch(finalLabel){
    case "INT": detail = "Intercepted!"; break;
    case "SACK": detail = "Quarterback sacked."; break;
    case "INC": detail = "Incomplete."; break;
    case "TD": detail = "Touchdown!"; break;
    case "BIG": detail = "Big gain!"; break;
    case "+5": detail = "+5 yards."; break;
    case "+2": detail = "+2 yards."; break;
    case "0": detail = "No gain."; break;
    case "-2": detail = "-2 yards."; break;
    case "-5": detail = "-5 yards."; break;
    case "FUM": detail = "Fumble!"; break;
    default: detail = offenseText;
  }
  return `${playerName} (${playType}) off-roll ${offRoll}${defRoll?`, def-roll ${defRoll}`:""} → ${detail}`;
}

function resolvePlay(team, playerName, playType, defenseTeam, situation){
  const player = team.players[playerName];
  if(!player){ return `Player not found: ${playerName}`; }

  const offTable = (playType === "Run") ? player.run : player.pass;
  const offRes = resolveFromTable(offTable);
  const baseText = offRes.outcome;
  const isPass = playType === "Pass";
  let offLabel = normalizeOutcomeLabel(baseText, isPass);

  // Defense
  let defRoll = null;
  if (defenseTeam && defenseTeam.defense){
    const defRes = resolveDefense(defenseTeam.defense, playType);
    defRoll = defRes.roll;
    const defLabel = (defRes.label || "").trim();
    if (defLabel){
      offLabel = applyDefenseBias(offLabel, defLabel, playType);
    }
  }

  // Situation
  if (situation){
    offLabel = applySituation(offLabel, playType, situation);
  }

  return renderFinalText(playerName, playType, offRes.roll, defRoll, baseText, offLabel);
}
