import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import ComparePlayers from "./pages/ComparePlayers";
import TeamAnalytics from "./pages/TeamAnalytics";
import TeamComparison from "./pages/TeamComparison";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/compare-players"
          element={<ComparePlayers />}
        />

        <Route
          path="/team-analytics"
          element={<TeamAnalytics />}
        />

        <Route
          path="/team-comparison"
          element={<TeamComparison />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;