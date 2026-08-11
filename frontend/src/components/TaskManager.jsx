import { useEffect, useState } from "react";
import { tasksApi } from "../api/tasks";
import { useAuth } from "../context/AuthContext";
import TaskForm from "./TaskForm";
import TaskItem from "./TaskItem";

export default function TaskManager() {
  const { logout } = useAuth();
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

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleCreate(newTask) {
    try {
      await tasksApi.create(newTask);
      await loadTasks();
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
      <div className="app-header">
        <h1>Task Manager</h1>
        <button onClick={logout} className="logout-btn">
          Log Out
        </button>
      </div>

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
