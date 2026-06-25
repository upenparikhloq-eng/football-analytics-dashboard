import { useEffect, useState } from "react";
import axios from "axios";
import RadarChartComponent from "../components/RadarChartComponent";
import "../styles/dashboard.css";

import argentinaLogo from "../assets/logos/argentina.jpg";
import franceLogo from "../assets/logos/france.jpg";

function Dashboard() {
  const [teams, setTeams] = useState([]);
  const [players, setPlayers] = useState([]);

  const [selectedTeam, setSelectedTeam] = useState("");
  const [selectedPlayer, setSelectedPlayer] = useState("");

  const [playerStats, setPlayerStats] = useState(null);
  const [radarData, setRadarData] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_URL;

  const teamLogos = {
    Argentina: argentinaLogo,
    France: franceLogo,
  };

 useEffect(() => {
  axios
    .get(`${API_BASE_URL}/teams`)
    .then((response) => {
      const data = response.data || [];
      setTeams(data);

      if (data.length > 0) {
        setSelectedTeam(data[0]);
      }
    })
    .catch(console.error);
}, []);

 useEffect(() => {
  if (!selectedTeam) return;

  axios
    .get(`${API_BASE_URL}/players?team_name=${selectedTeam}`)
    .then((response) => {
      const data = response.data || [];
      setPlayers(data);

      if (data.length > 0) {
        setSelectedPlayer((prev) => prev || data[0]);
      }
    })
    .catch(console.error);
}, [selectedTeam]);

  useEffect(() => {
  if (!selectedPlayer) return;

  axios.get(
  `${API_BASE_URL}/player-stats?player_name=${encodeURIComponent(selectedPlayer)}`
)
    .then((response) => {
      setPlayerStats(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}, [selectedPlayer]);

  useEffect(() => {
    if (!selectedPlayer) return;

   axios.get(
  `${API_BASE_URL}/player-radar?player_name=${encodeURIComponent(selectedPlayer)}`
)
      .then((response) => {
        setRadarData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [selectedPlayer]);

  return (
    <div className="page-container">

      {/* HERO SECTION */}
      <div className="hero-section">
        <h1 className="page-title">⚽ Football Analytics Platform</h1>

        <p className="page-subtitle">
          Argentina vs France • FIFA World Cup Final 2022
        </p>

        <div className="hero-divider"></div>
      </div>

      {/* SELECTORS */}
      <div className="selector-wrapper">
        <div className="selector-box">
          <label className="selector-label">Team</label>

          <select
            className="selector"
            value={selectedTeam}
            onChange={(e) => setSelectedTeam(e.target.value)}
          >
            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="selector-box">
          <label className="selector-label">Player</label>

          <select
            className="selector"
            value={selectedPlayer}
            onChange={(e) => setSelectedPlayer(e.target.value)}
          >
            {players.map((player) => (
              <option key={player} value={player}>
                {player}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* PLAYER PROFILE CARD */}
      <div className="player-profile-wrapper">
  <div className="player-profile-card">

    <div className="player-avatar">
      {(selectedPlayer || "")
        .split(" ")
        .map((word) => word[0])
        .slice(0, 2)
        .join("")}
    </div>

    <div className="player-info">

      <h2>{selectedPlayer}</h2>

      <div className="team-info">

        {teamLogos[selectedTeam] && (
          <img
            src={teamLogos[selectedTeam]}
            alt={selectedTeam}
            className="team-logo"
          />
        )}

        <span>{selectedTeam}</span>

      </div>

    </div>

  </div>
</div>

      {/* PLAYER STATS */}
      {playerStats && (
        <div className="stats-grid">
          {Object.entries(playerStats)
            .filter(([key]) => key !== "Player")
            .map(([key, value]) => (
              <div key={key} className="stat-card">
                <h3>{key}</h3>
                <h1>{value}</h1>
              </div>
            ))}
        </div>
      )}

      {/* RADAR */}
      {radarData && (
        <div className="chart-card">
          <h2>📊 Player Radar</h2>

          <RadarChartComponent radarData={radarData} />
        </div>
      )}

      {/* HEATMAP */}
      {selectedPlayer && (
        <div className="chart-card">
          <h2>🔥 Player Heatmap</h2>

         <img
  src={`${API_BASE_URL}/player-heatmap?player_name=${encodeURIComponent(selectedPlayer)}`}
  alt="Heatmap"
   className="chart-image"
/>
        </div>
      )}

      {/* PASS MAP */}
      {selectedPlayer && (
        <div className="chart-card">
          <h2>🎯 Player Pass Map</h2>

         <img
  src={`${API_BASE_URL}/player-pass-map?player_name=${encodeURIComponent(selectedPlayer)}`}
  alt="Pass Map"
  className="chart-image"
/>
        </div>
      )}
    </div>
  );
}

export default Dashboard;