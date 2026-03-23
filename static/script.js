document.addEventListener("DOMContentLoaded", async () => {
    const select = document.getElementById("year-select");
    const teamsList = document.getElementById("teams-list");
    // cache players per year+team to avoid refetching
    const playersCache = new Map();

    function renderTeams(teams) {
        teamsList.innerHTML = '';
        if (!teams || teams.length === 0) {
            teamsList.innerHTML = '<p class="muted">No teams found for this season.</p>';
            return;
        }

        // Normalize items into objects with name, division, league, team_id
        const normalized = teams.map(item => {
            if (Array.isArray(item)) {
                return { name: item[0] ?? String(item), division: item[1] ?? '', league: item[2] ?? '', team_id: item[3] ?? '' };
            }
            if (item && typeof item === 'object') {
                return {
                    name: item.name ?? item.teamName ?? Object.values(item).find(v=>typeof v==='string') ?? String(item),
                    division: item.division ?? item.divID ?? item.div ?? '',
                    league: item.league ?? item.lgID ?? item.lg ?? '',
                    team_id: item.team_id ?? item.teamID ?? item.team ?? ''
                };
            }
            return { name: String(item), division: '', league: '', team_id: '' };
        });

        // Group by league -> division
        const byLeague = {};
        normalized.forEach(t => {
            const lg = t.league || 'Unknown League';
            const div = t.division || 'Unknown Division';
            byLeague[lg] = byLeague[lg] || {};
            byLeague[lg][div] = byLeague[lg][div] || [];
            byLeague[lg][div].push(t.name);
        });

        // Render grouped structure
        Object.keys(byLeague).forEach(lg => {
            const lgHeader = document.createElement('h3');
            lgHeader.className = 'league-header';
            lgHeader.textContent = lg;
            teamsList.appendChild(lgHeader);

            const divisions = byLeague[lg];
            Object.keys(divisions).forEach(div => {
                const divHeader = document.createElement('h4');
                divHeader.className = 'division-header';
                divHeader.textContent = div;
                teamsList.appendChild(divHeader);

                const ul = document.createElement('ul');
                ul.className = 'team-items';
                divisions[div].forEach(name => {
                    // find the full team object for this name so we can attach team_id
                    const team = normalized.find(t => t.name === name && t.division === div && t.league === lg) || { team_id: '' };
                    const li = document.createElement('li');
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'team-button';
                    btn.dataset.team = team.team_id || '';
                    btn.textContent = name;
                    // ensure click triggers players dropdown
                    btn.addEventListener('click', (ev) => {
                        ev.stopPropagation();
                        const year = select.value;
                        if (!year) return;
                        const teamID = btn.dataset.team;
                        const li = btn.closest('li');
                        togglePlayersDropdown(li, year, teamID);
                    });
                    li.appendChild(btn);
                    ul.appendChild(li);
                });
                teamsList.appendChild(ul);
            });
        });
    }

    async function fetchPlayers(year, teamID) {
        const cacheKey = `${year}|${teamID}`;
        if (playersCache.has(cacheKey)) return playersCache.get(cacheKey);
        const res = await fetch(`/players?year=${encodeURIComponent(year)}&team=${encodeURIComponent(teamID)}`);
        if (!res.ok) throw new Error('Network response was not ok');
        const players = await res.json();
        playersCache.set(cacheKey, players);
        return players;
    }

    function closeOtherDropdowns(exceptEl) {
        document.querySelectorAll('.players-dropdown.open').forEach(d => {
            if (d === exceptEl) return;
            d.classList.remove('open');
            d.style.display = 'none';
        });
    }

    async function togglePlayersDropdown(li, year, teamID) {
        if (!li) return;
        let dropdown = li.querySelector('.players-dropdown');
        // close others
        closeOtherDropdowns(dropdown);
        if (dropdown) {
            // toggle
            const isOpen = dropdown.classList.contains('open');
            if (isOpen) {
                dropdown.classList.remove('open');
                dropdown.style.display = 'none';
                return;
            }
            dropdown.classList.add('open');
            dropdown.style.display = 'block';
            return;
        }

        dropdown = document.createElement('div');
        dropdown.className = 'players-dropdown open';
        dropdown.style.display = 'block';
        dropdown.innerHTML = '<p class="muted">Loading players...</p>';
        li.appendChild(dropdown);

        try {
            const players = await fetchPlayers(year, teamID);
            if (!players || players.length === 0) {
                dropdown.innerHTML = '<p class="muted">No players found for this team/season.</p>';
                return;
            }
            const ul = document.createElement('ul');
            ul.className = 'player-items';
            players.forEach(p => {
                const pli = document.createElement('li');
                const fname = p.first_name || p.nameFirst || '';
                const lname = p.last_name || p.nameLast || '';
                pli.textContent = `${fname} ${lname}`.trim();
                ul.appendChild(pli);
            });
            dropdown.innerHTML = '';
            dropdown.appendChild(ul);
        } catch (err) {
            dropdown.innerHTML = '<p class="muted">Failed to load players.</p>';
        }
    }

    async function renderTeamsForYear(year) {
        teamsList.innerHTML = '<p class="muted">Loading teams...</p>';
        try {
            const res = await fetch(`/teams?year=${encodeURIComponent(year)}`);
            if (!res.ok) throw new Error('Network response was not ok');
            const teams = await res.json();
            renderTeams(teams);
        } catch (err) {
            teamsList.innerHTML = '<p class="muted">Failed to load teams.</p>';
        }
    }

    try {
        const response = await fetch("/years");
        const years = await response.json();

        select.innerHTML = '<option value="">-- Choose a season --</option>';
        years.forEach((year) => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = year;
            select.appendChild(option);
        });
        select.disabled = false;
    } catch {
        select.innerHTML = '<option value="">Failed to load seasons</option>';
    }

    select.addEventListener('change', (e) => {
        const year = select.value;
        if (!year) {
            teamsList.innerHTML = '<p class="muted">Select a season to view teams.</p>';
            if (playersList) playersList.innerHTML = '<p class="muted">Select a team to view players.</p>';
            return;
        }
        // close any open dropdowns when changing year
        document.querySelectorAll('.players-dropdown').forEach(d => d.remove());
        renderTeamsForYear(year);
    });
});
