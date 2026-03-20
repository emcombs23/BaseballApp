document.addEventListener("DOMContentLoaded", async () => {
    const select = document.getElementById("year-select");
    const teamsList = document.getElementById("teams-list");

    function renderTeams(teams) {
        teamsList.innerHTML = '';
        if (!teams || teams.length === 0) {
            teamsList.innerHTML = '<p class="muted">No teams found for this season.</p>';
            return;
        }

        // Normalize items into objects with name, division, league
        const normalized = teams.map(item => {
            if (Array.isArray(item)) {
                return { name: item[0] ?? String(item), division: item[1] ?? '', league: item[2] ?? '' };
            }
            if (item && typeof item === 'object') {
                return {
                    name: item.name ?? item.teamName ?? Object.values(item).find(v=>typeof v==='string') ?? String(item),
                    division: item.division ?? item.divID ?? item.div ?? '',
                    league: item.league ?? item.lgID ?? item.lg ?? ''
                };
            }
            return { name: String(item), division: '', league: '' };
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
                    const li = document.createElement('li');
                    li.textContent = name;
                    ul.appendChild(li);
                });
                teamsList.appendChild(ul);
            });
        });
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
            return;
        }
        renderTeamsForYear(year);
    });
});
