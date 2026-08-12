const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// A tiny helper so every call handles errors the same way, instead of
// repeating try/catch + response.ok checks in every component.
async function request(path, options = {}) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      // Every protected endpoint needs this header. If token is missing/
      // expired, FastAPI's get_current_user dependency rejects with 401
      // before our route code ever runs.
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...options,
  });

  if (!response.ok) {
    // Our FastAPI HTTPException responses look like { "detail": "..." }
    // -- we surface that message here so the UI can show something useful.
    const errorBody = await response.json().catch(() => ({}));
    if (response.status === 401) {
      // Token missing/expired/invalid -- clear it so the UI drops back
      // to the login screen instead of looping on failed requests.
      localStorage.removeItem("access_token");
    }
    throw new Error(
      errorBody.detail || `Request failed with status ${response.status}`,
    );
  }

  // DELETE returns 204 No Content -- there's no JSON body to parse.
  if (response.status === 204) return null;

  return response.json();
}

export const tasksApi = {
  list: (completed) => {
    const query = completed === undefined ? "" : `?completed=${completed}`;
    return request(`/tasks${query}`);
  },
  create: (task) =>
    request("/tasks", { method: "POST", body: JSON.stringify(task) }),
  update: (id, updates) =>
    request(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(updates) }),
  remove: (id) => request(`/tasks/${id}`, { method: "DELETE" }),
};
