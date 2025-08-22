
function resolvePlay(team, player, playType) {
    let roll = roll2d6();
    let outcome = "";
    if(playType === "Run") {
        outcome = team.players[player].run[roll] || "No gain";
    } else if(playType === "Pass") {
        outcome = team.players[player].pass[roll] || "Incomplete";
    }
    return `${player} (${playType}) rolled ${roll}: ${outcome}`;
}
