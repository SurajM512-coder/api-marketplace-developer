import { useEffect, useState } from "react";
import {
  getMySubscriptions,
  cancelSubscription,
} from "../services/api";

function MySubscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    fetchSubscriptions();
  }, []);

  const fetchSubscriptions = async () => {
    try {
      const data = await getMySubscriptions();
      setSubscriptions(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCancel = async (subscriptionId) => {
    try {
      await cancelSubscription(subscriptionId);

      alert("Subscription cancelled.");

      fetchSubscriptions();
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Unable to cancel subscription."
      );
    }
  };

  return (
    <div style={styles.container}>
      <h1>My Subscriptions</h1>

      {subscriptions.length === 0 ? (
        <p>You haven't subscribed to any APIs yet.</p>
      ) : (
        subscriptions.map((subscription) => (
          <div
            key={subscription.id}
            style={styles.card}
          >
            <h3>Subscription #{subscription.id}</h3>

            <p>
              <strong>API ID:</strong> {subscription.api_id}
            </p>

            <p>
              <strong>Status:</strong>{" "}
              {subscription.is_active
                ? "Active"
                : "Inactive"}
            </p>

            {subscription.is_active && (
              <button
                style={styles.button}
                onClick={() =>
                  handleCancel(subscription.id)
                }
              >
                Cancel Subscription
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "900px",
    margin: "40px auto",
  },

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "20px",
    marginBottom: "20px",
  },

  button: {
    marginTop: "15px",
    padding: "10px 20px",
    cursor: "pointer",
  },
};

export default MySubscriptions;