import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function BrowseApis() {
  const [apis, setApis] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchApis();
  }, []);

  const fetchApis = async (searchValue = "") => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/apis", {
        params: {
          search: searchValue || undefined,
        },
      });

      setApis(response.data);
    } catch (error) {
      console.error(error);
      setError("Failed to load APIs.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchApis(search);
  };

  return (
    <div>
      <h1>Browse APIs</h1>

      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search APIs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <button type="submit">Search</button>
      </form>

      <br />

      {loading && <p>Loading APIs...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && apis.length === 0 && (
        <p>No APIs found.</p>
      )}

      {!loading &&
        !error &&
        apis.map((apiItem) => (
          <div
            key={apiItem.id}
            style={{
              border: "1px solid #ddd",
              padding: "20px",
              marginBottom: "15px",
              borderRadius: "8px",
            }}
          >
            <h2>{apiItem.name}</h2>

            <p>{apiItem.description}</p>

            <p>
              <strong>Category:</strong> {apiItem.category}
            </p>

            <p>
              <strong>Pricing:</strong> {apiItem.pricing}
            </p>

            <p>
              <strong>Version:</strong> {apiItem.version}
            </p>

            <Link to={`/apis/${apiItem.id}`}>
              View Details
            </Link>
          </div>
        ))}
    </div>
  );
}

export default BrowseApis;