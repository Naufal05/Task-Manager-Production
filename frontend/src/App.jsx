import { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginForm from "./components/LoginForm";
import SignupForm from "./components/SignupForm";
import TaskManager from "./components/TaskManager";
import "./App.css";

// Small inner component so it can call useAuth() -- useAuth only works
// INSIDE an <AuthProvider>, so the Provider has to wrap this, not be inside it.
function AppContent() {
  const { isAuthenticated } = useAuth();
  const [showSignup, setShowSignup] = useState(false);

  if (!isAuthenticated) {
    return (
      <div className="app auth-screen">
        {showSignup ? (
          <SignupForm onSwitchToLogin={() => setShowSignup(false)} />
        ) : (
          <LoginForm onSwitchToSignup={() => setShowSignup(true)} />
        )}
      </div>
    );
  }

  return <TaskManager />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
