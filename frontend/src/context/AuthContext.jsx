import { createContext, useContext, useState } from "react";
import { loginUser, registerUser } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // Initialize from localStorage so a page refresh doesn't log the user out.
  const [token, setToken] = useState(() =>
    localStorage.getItem("access_token"),
  );

  async function login(email, password) {
    const data = await loginUser(email, password);
    localStorage.setItem("access_token", data.access_token);
    setToken(data.access_token);
  }

  async function register(email, password) {
    await registerUser(email, password);
    // Immediately log in after successful registration for a smooth UX.
    await login(email, password);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setToken(null);
  }

  return (
    <AuthContext.Provider
      value={{ token, isAuthenticated: !!token, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook: components call useAuth() instead of importing AuthContext
// directly -- a common React convention that also lets us throw a clear
// error if someone uses it outside an <AuthProvider>.
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
