import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { token, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav
      style={{
        background: "#1f2937",
        padding: "20px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <h2 style={{ color: "white", margin: 0 }}>
        API Marketplace
      </h2>

      <div
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center",
        }}
      >
        <Link to="/" style={linkStyle}>
          Home
        </Link>

        <Link to="/apis" style={linkStyle}>
          APIs
        </Link>

        {token ? (
          <>
            <Link to="/dashboard" style={linkStyle}>
              Dashboard
            </Link>

            {role === "consumer" && (
              <Link to="/my-subscriptions" style={linkStyle}>
                My Subscriptions
              </Link>
            )}

            <button
              onClick={handleLogout}
              style={{
                background: "none",
                border: "none",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                padding: 0,
                fontFamily: "inherit",
                fontSize: "inherit",
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={linkStyle}>
              Login
            </Link>

            <Link to="/register" style={linkStyle}>
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

const linkStyle = {
  color: "white",
  textDecoration: "none",
  fontWeight: "bold",
};

export default Navbar;