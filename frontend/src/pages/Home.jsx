import { useEffect, useState } from "react";
import api from "../services/api";

function Home() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    api
      .get("/")
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch(() => {
        setMessage("Backend connection failed");
      });
  }, []);

  return (
    <div>
      <h1>Home Page</h1>

      <h2>{message}</h2>
    </div>
  );
}

export default Home;