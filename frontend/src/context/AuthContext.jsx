import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api, { getErrorMessage } from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("rsa_token");
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get("/api/auth/me")
      .then((response) => setUser(response.data))
      .catch(() => {
        localStorage.removeItem("rsa_token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    setError("");
    try {
      const response = await api.post("/api/auth/login", { email, password });
      localStorage.setItem("rsa_token", response.data.access_token);
      const me = await api.get("/api/auth/me");
      setUser(me.data);
      return me.data;
    } catch (err) {
      const message = getErrorMessage(err, "Unable to sign in.");
      setError(message);
      throw err;
    }
  };

  const register = async (name, email, password) => {
    setError("");
    try {
      const response = await api.post("/api/auth/register", { name, email, password });
      localStorage.setItem("rsa_token", response.data.access_token);
      const me = await api.get("/api/auth/me");
      setUser(me.data);
      return me.data;
    } catch (err) {
      const message = getErrorMessage(err, "Unable to create this account.");
      setError(message);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem("rsa_token");
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, loading, error, setError, login, register, logout }),
    [user, loading, error]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
