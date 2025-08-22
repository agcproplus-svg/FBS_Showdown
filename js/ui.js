
let leagueData = {};
let selectedTeam = null;
let selectedPlayer = null;

async function loadLeague(){
  const res = await fetch('data/league.json');
  leagueData = await res.json();
  const teamSelect = document.getElementById('teamSelect');
  teamSelect.innerHTML = '<option value="">--Choose Team--</option>';
  for (let t of leagueData.teams) {
    const opt = document.createElement('option');
    opt.value = t.name;
    opt.textContent = t.name;
    teamSelect.appendChild(opt);
  }
  renderTeamList();
}

function renderTeamList(){
  const list = document.getElementById('teamList');
  if(!list) return;
  list.innerHTML = '';
  for (let t of leagueData.teams){
    const div = document.createElement('div');
    div.className = 'team-card';
    const logo = document.createElement('img');
    logo.src = t.logo || 'img/logos/_placeholder.png';
    const name = document.createElement('div');
    name.textContent = t.name;
    div.appendChild(logo);
    div.appendChild(name);
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
    opt.value = p;
    opt.textContent = p;
    playerSelect.appendChild(opt);
  }
}

function selectPlayer(){
  selectedPlayer = document.getElementById('playerSelect').value;
}

function runPlay(playType){
  if(!selectedTeam || !selectedPlayer){
    logMessage('Please choose a team and player first.');
    return;
  }
  const msg = resolvePlay(selectedTeam, selectedPlayer, playType);
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

window.onload = loadLeague;
