import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";

function TeamComparison() {
  const [teams, setTeams] = useState([]);

  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    axios.get(`${API_BASE_URL}/teams`)
      .then((response) => {
        setTeams(response.data);

        if (response.data.length >= 2) {
          setTeam1(response.data[0]);
          setTeam2(response.data[1]);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const comparisonUrl =
  team1 && team2
    ? `${API_BASE_URL}/team-comparison?team1=${encodeURIComponent(team1)}&team2=${encodeURIComponent(team2)}`
    : "";

  return (
    <div className="page-container">
      <div className="hero-section">
        <div className="hero-divider"></div>

        <h1 className="page-title">⚔️ Team Comparison</h1>

        <p className="page-subtitle">
          Compare complete team performance metrics
        </p>
      </div>

      <div className="selector-wrapper">
        <div className="selector-box">
          <label className="selector-label">Team 1</label>

          <select
            className="selector"
            value={team1}
            onChange={(e) => setTeam1(e.target.value)}
          >
            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="selector-box">
          <label className="selector-label">Team 2</label>

          <select
            className="selector"
            value={team2}
            onChange={(e) => setTeam2(e.target.value)}
          >
            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>
      </div>

      {team1 && team2 && (
        <div className="chart-card">
          <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
            Match Statistics Comparison
          </h2>

          <img
            src={comparisonUrl}
            alt="Team Comparison"
            className="chart-image"
          />
        </div>
      )}
    </div>
  );
}

export default TeamComparison;