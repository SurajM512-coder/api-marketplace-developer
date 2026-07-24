import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function OAuthSuccess() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    const token = searchParams.get("token");
    const role = searchParams.get("role");

    if (token && role) {
      login(token, role);

      navigate("/dashboard", {
        replace: true,
      });
    } else {
      navigate("/login", {
        replace: true,
      });
    }
  }, [searchParams, login, navigate]);

  return (
    <div>
      <h2>Completing Google login...</h2>
    </div>
  );
}

export default OAuthSuccess;