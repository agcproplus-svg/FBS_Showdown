
let leagueData = {};
let selectedTeam = null;
let selectedDefense = null;
let selectedPlayer = null;

const situation = { down: 1, distance: "medium", field: "mid" };

async function loadLeague(){
  const res = await fetch('data/league.json');
  leagueData = await res.json();
  populateTeamSelects();
  renderTeamList();
}

function populateTeamSelects(filterText=""){
  const teamSelect = document.getElementById('teamSelect');
  const defenseSelect = document.getElementById('defenseSelect');
  teamSelect.innerHTML = '<option value="">--Choose Offense--</option>';
  defenseSelect.innerHTML = '<option value="">--Choose Defense--</option>';

  const list = leagueData.teams
    .filter(t => t.name.toLowerCase().includes(filterText.toLowerCase()));

  for (let t of list) {
    const opt1 = document.createElement('option');
    opt1.value = t.name; opt1.textContent = t.name;
    teamSelect.appendChild(opt1);

    const opt2 = document.createElement('option');
    opt2.value = t.name; opt2.textContent = t.name;
    defenseSelect.appendChild(opt2);
  }
}

function onSearchInput(el){
  populateTeamSelects(el.value || "");
  renderTeamList(el.value || "");
}

function renderTeamList(filterText=""){
  const list = document.getElementById('teamList');
  if(!list) return;
  list.innerHTML = '';
  for (let t of leagueData.teams){
    if (filterText && !t.name.toLowerCase().includes(filterText.toLowerCase())) continue;
    const div = document.createElement('div');
    div.className = 'team-card';
    const logo = document.createElement('img');
    logo.src = t.logo || 'img/logos/_placeholder.png';
    const name = document.createElement('div');
    name.textContent = t.name;
    div.appendChild(logo); div.appendChild(name);
    list.appendChild(div);
  }
}

function selectTeam(){
  const teamName = document.getElementById('teamSelect').value;
  selectedTeam = leagueData.teams.find(t => t.name === teamName);
  const playerSelect = document.getElementById('playerSelect');
  playerSelect.innerHTML = '<option value="">--Choose Player--</option>';
  if(!selectedTeam){ return; }
  for (let p in selectedTeam.players){
    const opt = document.createElement('option');
    opt.value = p; opt.textContent = p;
    playerSelect.appendChild(opt);
  }
}

function selectDefense(){
  const defName = document.getElementById('defenseSelect').value;
  selectedDefense = leagueData.teams.find(t => t.name === defName);
}

function selectPlayer(){
  selectedPlayer = document.getElementById('playerSelect').value;
}

// Situation controls
function setDown(el){ situation.down = parseInt(el.value,10); showSituation(); }
function setDistance(el){ situation.distance = el.value; showSituation(); }
function setField(el){ situation.field = el.value; showSituation(); }

function showSituation(){
  const el = document.getElementById('situationBadge');
  el.textContent = `Down ${situation.down}, ${situation.distance}, ${situation.field}`;
}

function runPlay(playType){
  if(!selectedTeam || !selectedPlayer){
    logMessage('Choose offense team and player first.');
    return;
  }
  if(!selectedDefense){
    logMessage('Choose a defense team (for defensive modifiers).');
    return;
  }
  const msg = resolvePlay(selectedTeam, selectedPlayer, playType, selectedDefense, situation);
  logMessage(msg);
}

function logMessage(msg){
  const log = document.getElementById('log');
  const d = document.createElement('div');
  d.className = 'log-line';
  d.textContent = msg;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
}

window.onload = () => { loadLeague(); showSituation(); };
