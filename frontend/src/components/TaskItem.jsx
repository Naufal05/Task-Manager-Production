export default function TaskItem({ task, onToggleComplete, onDelete }) {
  return (
    <li className={`task-item ${task.completed ? "completed" : ""}`}>
      <label>
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggleComplete(task)}
        />
        <span className="task-title">{task.title}</span>
      </label>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <span className={`priority-badge priority-${task.priority}`}>
        {task.priority}
      </span>

      <button onClick={() => onDelete(task.id)} className="delete-btn">
        Delete
      </button>
    </li>
  );
}
