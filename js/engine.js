
function resolvePlay(team, playerName, playType){
  const player = team.players[playerName];
  if(!player){ return `${playerName} not found.`; }
  const roll = roll2d6();
  let table = playType==='Run' ? player.run : player.pass;
  if(!table){ table = {}; }
  const outcome = table[String(roll)] || (playType==='Run' ? 'No gain' : 'Incomplete');
  return `${playerName} (${playType}) rolled ${roll}: ${outcome}`;
}
