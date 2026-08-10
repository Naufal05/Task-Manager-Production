import { useEffect, useState } from "react";
import { tasksApi } from "./api/tasks";
import TaskForm from "./components/TaskForm";
import TaskItem from "./components/TaskItem";
import "./App.css";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadTasks() {
    try {
      setLoading(true);
      const data = await tasksApi.list();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // useEffect with an empty dependency array [] runs once, right after
  // the component first mounts -- this is our "on page load, fetch data" hook.
  useEffect(() => {
    loadTasks();
  }, []);

  async function handleCreate(newTask) {
    try {
      await tasksApi.create(newTask);
      await loadTasks(); // re-fetch so the list reflects the DB's actual state
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleToggleComplete(task) {
    try {
      await tasksApi.update(task.id, { completed: !task.completed });
      await loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(taskId) {
    try {
      await tasksApi.remove(taskId);
      await loadTasks();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="app">
      <h1>Task Manager</h1>

      <TaskForm onCreate={handleCreate} />

      {error && <p className="error-banner">Error: {error}</p>}

      {loading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p>No tasks yet -- add one above.</p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </div>
  );
}
