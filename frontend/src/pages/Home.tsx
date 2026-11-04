
import { useEffect, useState } from "react";

import {
  getTasks,
  type Task,
} from "../services/taskservice";

function Home() {

  // Store tasks received from FastAPI
  const [tasks, setTasks] = useState<Task[]>([]);

  // Track loading status
  const [loading, setLoading] = useState(true);

  // Fetch tasks when the component loads
  useEffect(() => {

    const fetchTasks = async () => {
      try {
        const data = await getTasks();

        // Update React state with API data
        setTasks(data);

      } catch (error) {
        console.error("Failed to fetch tasks:", error);

      } finally {
        setLoading(false);
      }
    };

    fetchTasks();

  }, []);

  if (loading) {
    return <p>Loading tasks...</p>;
  }

  return (
    <div>
      <h1>TaskFlow</h1>

      {tasks.map((task) => (
        <div key={task.id}>
          <h3>{task.title}</h3>

          <p>
            Status: {task.completed ? "Completed" : "Pending"}
          </p>
        </div>
      ))}
    </div>
  );
}

export default Home;
