const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function registerUser(email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Registration failed");
  }
  return response.json();
}

export async function loginUser(email, password) {
  // /auth/login expects FORM data (OAuth2PasswordRequestForm on the backend),
  // not JSON -- this is a spec requirement, not a choice we made.
  const body = new URLSearchParams();
  body.append("username", email); // the spec calls it 'username', we treat it as email
  body.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || "Login failed");
  }
  return response.json(); // { access_token, token_type }
}
