import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="navbar">

      <Link to="/">
        Dashboard
      </Link>

      <Link to="/compare-players">
        Compare Players
      </Link>

      <Link to="/team-analytics">
        Team Analytics
      </Link>

      <Link to="/team-comparison">
        Team Comparison
      </Link>

    </div>
  );
}

export default Navbar;