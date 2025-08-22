
let leagueData = {};
let selectedTeam = null;
let selectedPlayer = null;

async function loadLeague() {
    const res = await fetch('data/league.json');
    leagueData = await res.json();
    const teamSelect = document.getElementById('teamSelect');
    teamSelect.innerHTML = '<option value="">--Choose Team--</option>';
    for (let t of leagueData.teams) {
        let opt = document.createElement('option');
        opt.value = t.name;
        opt.textContent = t.name;
        teamSelect.appendChild(opt);
    }
}

function selectTeam() {
    const teamName = document.getElementById('teamSelect').value;
    selectedTeam = leagueData.teams.find(t => t.name === teamName);
    const playerSelect = document.getElementById('playerSelect');
    playerSelect.innerHTML = '<option value="">--Choose Player--</option>';
    for (let p in selectedTeam.players) {
        let opt = document.createElement('option');
        opt.value = p;
        opt.textContent = p;
        playerSelect.appendChild(opt);
    }
}

function selectPlayer() {
    selectedPlayer = document.getElementById('playerSelect').value;
}

function runPlay(playType) {
    if (!selectedTeam || !selectedPlayer) {
        logMessage("Please choose a team and player first.");
        return;
    }
    let result = resolvePlay(selectedTeam, selectedPlayer, playType);
    logMessage(result);
}

function logMessage(msg) {
    const log = document.getElementById('log');
    let p = document.createElement('div');
    p.textContent = msg;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
}

window.onload = loadLeague;
