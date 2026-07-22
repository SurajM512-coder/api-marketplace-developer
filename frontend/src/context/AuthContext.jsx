import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [role, setRole] = useState(
    localStorage.getItem("user_role")
  );

  const login = (newToken, userRole) => {
    localStorage.setItem("access_token", newToken);
    localStorage.setItem("user_role", userRole);

    setToken(newToken);
    setRole(userRole);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");

    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        role,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);