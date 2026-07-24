import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();


  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      login(
        response.data.access_token,
        response.data.role
      );

      alert("Login Successful!");

      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      alert("Login Failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button type="submit">
          Login
        </button>
      </form>

      <hr />

      <p>Or</p>

      <button
        type="button"
        onClick={() => {
          window.location.href =
            "http://localhost:8000/auth/google/login";
        }}
      >
        Continue with Google
      </button>
    </div>
  );
}

export default Login;