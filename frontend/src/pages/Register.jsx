import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("consumer");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/register", {
        name,
        email,
        password,
        role,
      });

      alert(
        "Registration successful! Please check your email and verify your account."
      );

      navigate("/login");
    } catch (error) {
      console.error(error);

      const detail = error.response?.data?.detail;

      let message = "Registration failed";

      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail
          .map((item) => item.msg)
          .join("\n");
      }

      alert(message);
    }
  };

  return (
    <div>
      <h1>Register</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <br />
        <br />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />
        <br />

        <label>
          Account Type:{" "}
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="consumer">Consumer</option>
            <option value="developer">Developer</option>
          </select>
        </label>

        <br />
        <br />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;