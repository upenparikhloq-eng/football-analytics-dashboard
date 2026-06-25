import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";

function TeamAnalytics() {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");

  const [teamStats, setTeamStats] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_URL;

  const averagePositionUrl =
  `${API_BASE_URL}/average-positions?team_name=${encodeURIComponent(selectedTeam)}`;

const passingNetworkUrl =
  `${API_BASE_URL}/passing-network?team_name=${encodeURIComponent(selectedTeam)}`;

const xgTimelineUrl =
  `${API_BASE_URL}/xg-timeline`;
  useEffect(() => {
    axios.get(`${API_BASE_URL}/teams`)
      .then((response) => {
        setTeams(response.data);

        if (response.data.length > 0) {
          setSelectedTeam(response.data[0]);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  useEffect(() => {
    if (!selectedTeam) return;

    axios
      .get(
        `${API_BASE_URL}/team-stats?team_name=${encodeURIComponent(
          selectedTeam
        )}`
      )
      .then((response) => {
        setTeamStats(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [selectedTeam]);

  return (
    <div className="page-container">
      <div className="hero-section">
        <div className="hero-divider"></div>

        <h1 className="page-title">🏆 Team Analytics</h1>

        <p className="page-subtitle">
          Analyze team performance, structure and tactical patterns
        </p>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "30px",
        }}
      >
        <div className="selector-box">
          <label className="selector-label">Select Team</label>

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
      </div>

      {teamStats && (
        <>
          <div className="stats-grid">
            {Object.entries(teamStats).map(([key, value]) => (
              <div key={key} className="stat-card">
                <h3>{key}</h3>

                <h1
                  style={{
                    fontSize: key === "Team" ? "2rem" : "3rem",
                  }}
                >
                  {value}
                </h1>
              </div>
            ))}
          </div>

          <div className="chart-card">
            <h2>Average Positions</h2>

            <img
              src={averagePositionUrl}
              alt="Average Positions"
              className="chart-image"
            />
          </div>

          <div className="chart-card">
            <h2>Passing Network</h2>

            <img
              src={passingNetworkUrl}
              alt="Passing Network"
              className="chart-image"
            />
          </div>

          <div className="chart-card">
            <h2>xG Timeline</h2>

            <img src={xgTimelineUrl} alt="xG Timeline" className="chart-image" />
          </div>
        </>
      )}
    </div>
  );
}

export default TeamAnalytics;