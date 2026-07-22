import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { token, role } = useAuth();

  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const response = await api.get(`/dashboard/${role}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setDashboardData(response.data);
      } catch (error) {
        console.error(error);

        setError(
          error.response?.data?.detail ||
            "Failed to load dashboard."
        );
      } finally {
        setLoading(false);
      }
    };

    if (token && role) {
      loadDashboard();
    }
  }, [token, role]);

  if (loading) {
    return <h2>Loading dashboard...</h2>;
  }

  if (error) {
    return (
      <div>
        <h2>Dashboard Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>
        Logged in as: <strong>{role}</strong>
      </p>

      {role === "admin" && (
        <div style={styles.cardContainer}>
          <DashboardCard
            title="Total Users"
            value={dashboardData.total_users}
          />

          <DashboardCard
            title="Total APIs"
            value={dashboardData.total_apis}
          />

          <DashboardCard
            title="Total Subscriptions"
            value={dashboardData.total_subscriptions}
          />

          <DashboardCard
            title="Total Requests"
            value={dashboardData.total_requests}
          />
        </div>
      )}

      {role === "developer" && (
        <div style={styles.cardContainer}>
          <DashboardCard
            title="My APIs"
            value={dashboardData.total_apis}
          />

          <DashboardCard
            title="Total Subscribers"
            value={dashboardData.total_subscribers}
          />

          <DashboardCard
            title="Total Requests"
            value={dashboardData.total_requests}
          />

          <DashboardCard
            title="Top API"
            value={dashboardData.top_api?.name || "No data"}
          />
        </div>
      )}

      {role === "consumer" && (
        <div style={styles.cardContainer}>
          <DashboardCard
            title="Active Subscriptions"
            value={dashboardData.active_subscriptions}
          />

          <DashboardCard
            title="API Keys"
            value={dashboardData.total_api_keys}
          />

          <DashboardCard
            title="Total Requests"
            value={dashboardData.total_requests}
          />
        </div>
      )}
    </div>
  );
}

function DashboardCard({ title, value }) {
  return (
    <div style={styles.card}>
      <h3>{title}</h3>
      <p style={styles.cardValue}>{value ?? 0}</p>
    </div>
  );
}

const styles = {
  cardContainer: {
    display: "flex",
    flexWrap: "wrap",
    gap: "20px",
    marginTop: "30px",
  },

  card: {
    width: "220px",
    padding: "25px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
    backgroundColor: "white",
  },

  cardValue: {
    fontSize: "32px",
    fontWeight: "bold",
    marginBottom: "0",
  },
};

export default Dashboard;