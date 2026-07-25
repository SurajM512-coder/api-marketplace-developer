import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import { subscribeToApi } from "../services/api";

function ApiDetails() {
  const { id } = useParams();

  const [apiData, setApiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadApi = async () => {
      try {
        const response = await api.get(`/apis/${id}`);
        setApiData(response.data);
      } catch (err) {
        console.error(err);

        setError(
          err.response?.data?.detail ||
            "Failed to load API details."
        );
      } finally {
        setLoading(false);
      }
    };

    loadApi();
  }, [id]);

  if (loading) {
    return <h2>Loading API Details...</h2>;
  }

  if (error) {
    return (
      <div style={styles.container}>
        <h2>Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  const handleSubscribe = async () => {
    try {
      await subscribeToApi(id);
      alert("Subscribed successfully!");
    } catch (error) {
      console.error(error.response);

      alert(
        error.response?.data?.detail ||
        error.message ||
        "Subscription failed."
      );
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>{apiData.name}</h1>

        <p style={styles.description}>
          {apiData.description}
        </p>
      </div>

      <div style={styles.card}>
        <DetailRow
          label="Category"
          value={apiData.category}
        />

        <DetailRow
          label="Version"
          value={apiData.version}
        />

        <DetailRow
          label="Pricing"
          value={apiData.pricing}
        />

        <DetailRow
          label="Base URL"
          value={apiData.baseUrl}
        />

        <DetailRow
          label="Created On"
          value={new Date(apiData.created_at).toLocaleDateString()}
        />
      </div>

      <button
        style={styles.button}
        onClick={handleSubscribe}
      >
        Subscribe
      </button>
    </div>
  );
}

function DetailRow({ label, value }) {
  return (
    <div style={styles.row}>
      <span style={styles.label}>
        {label}
      </span>

      <span>{value || "-"}</span>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "900px",
    margin: "40px auto",
    padding: "20px",
  },

  header: {
    marginBottom: "30px",
  },

  description: {
    fontSize: "18px",
    color: "#555",
    marginTop: "12px",
    marginBottom: "25px",
    lineHeight: "1.6",
  },

  card: {
    backgroundColor: "#fff",
    border: "1px solid #ddd",
    borderRadius: "12px",
    padding: "25px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
  },

  row: {
    display: "flex",
    justifyContent: "space-between",
    padding: "16px 0",
    borderBottom: "1px solid #eee",
    fontSize: "17px",
  },

  label: {
    fontWeight: "bold",
  },

  button: {
    marginTop: "25px",
    padding: "12px 28px",
    fontSize: "16px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default ApiDetails;