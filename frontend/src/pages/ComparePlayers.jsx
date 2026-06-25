import { useEffect, useState } from "react";
import axios from "axios";
import CompareRadarChart from "../components/CompareRadarChart";
import "../styles/dashboard.css";

function ComparePlayers() {
  const [teams, setTeams] = useState([]);

  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");

  const [players1, setPlayers1] = useState([]);
  const [players2, setPlayers2] = useState([]);

  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");

  const [comparisonData, setComparisonData] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
     axios.get(`${API_BASE_URL}/teams`)
      .then((response) => {
        setTeams(response.data);

        if (response.data.length > 0) {
          setTeam1(response.data[0]);
        }

        if (response.data.length > 1) {
          setTeam2(response.data[1]);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  useEffect(() => {
    if (!team1) return;

    axios
      .get(`${API_BASE_URL}/players?team_name=${team1}`)
      .then((response) => {
        setPlayers1(response.data);

        if (response.data.length > 0) {
          setPlayer1(response.data[0]);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, [team1]);

  useEffect(() => {
    if (!team2) return;

    axios
      .get(`${API_BASE_URL}/players?team_name=${team2}`)
      .then((response) => {
        setPlayers2(response.data);

        if (response.data.length > 0) {
          setPlayer2(response.data[0]);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, [team2]);

  useEffect(() => {
    if (!player1 || !player2) return;

    axios
      .get(
        `${API_BASE_URL}/compare-radar?player1=${encodeURIComponent(
          player1
        )}&player2=${encodeURIComponent(player2)}`
      )
      .then((response) => {
        setComparisonData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [player1, player2]);

  return (
    <div className="page-container">
      <div className="hero-section">
        <div className="hero-divider"></div>
        

        <h1 className="page-title">⚔️ Compare Players</h1>

        <p className="page-subtitle">
          Compare football players using advanced analytics
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

          <label className="selector-label">Player 1</label>

          <select
            className="selector"
            value={player1}
            onChange={(e) => setPlayer1(e.target.value)}
          >
            {players1.map((player) => (
              <option key={player} value={player}>
                {player}
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

          <label className="selector-label">Player 2</label>

          <select
            className="selector"
            value={player2}
            onChange={(e) => setPlayer2(e.target.value)}
          >
            {players2.map((player) => (
              <option key={player} value={player}>
                {player}
              </option>
            ))}
          </select>
        </div>
      </div>

      {comparisonData && (
        <div className="chart-card">
          <h2>Radar Comparison</h2>

          <CompareRadarChart comparisonData={comparisonData} />
        </div>
      )}
    </div>
  );
}

export default ComparePlayers;