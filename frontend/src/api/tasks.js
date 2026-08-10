const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// A tiny helper so every call handles errors the same way, instead of
// repeating try/catch + response.ok checks in every component.
async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    // Our FastAPI HTTPException responses look like { "detail": "..." }
    // -- we surface that message here so the UI can show something useful.
    const errorBody = await response.json().catch(() => ({}));
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
