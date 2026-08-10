import { useState } from "react";

export default function TaskForm({ onCreate }) {
  // "Controlled inputs": React state is the single source of truth for
  // each field's value, rather than reading straight from the DOM.
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");

  async function handleSubmit(e) {
    e.preventDefault(); // stop the browser's default full-page-reload form submit
    if (!title.trim()) return;

    // This shape must match our TaskCreate Pydantic model on the backend --
    // title required, description optional, priority one of the enum values.
    await onCreate({ title, description: description || null, priority });

    // Reset the form after a successful create
    setTitle("");
    setDescription("");
    setPriority("medium");
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        placeholder="Task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button type="submit">Add Task</button>
    </form>
  );
}
