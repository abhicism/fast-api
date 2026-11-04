import { createContext, useCallback, useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { Task } from "../types/Task";
import {
  createTask as createTaskRequest,
  deleteTask as deleteTaskRequest,
  getTasks,
  updateTask as updateTaskRequest,
} from "../services/taskservice";

type TaskContextType = {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  addTask: (title: string) => Promise<void>;
  toggleTask: (id: number) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
};

const TaskContext = createContext<TaskContextType | null>(null);

export function TaskProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshTasks = useCallback(async () => {
    setLoading(true);
    try {
      setTasks(await getTasks());
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not load tasks.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshTasks();
  }, [refreshTasks]);

  async function addTask(title: string) {
    try {
      const task = await createTaskRequest(title);
      setTasks((current) => [...current, task]);
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not add task.");
      throw requestError;
    }
  }

  async function toggleTask(id: number) {
    const task = tasks.find((item) => item.id === id);
    if (!task) return;
    try {
      const updated = await updateTaskRequest(id, { completed: !task.completed });
      setTasks((current) => current.map((item) => item.id === id ? updated : item));
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not update task.");
    }
  }

  async function deleteTask(id: number) {
    try {
      await deleteTaskRequest(id);
      setTasks((current) => current.filter((task) => task.id !== id));
      setError(null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not delete task.");
    }
  }

  return (
    <TaskContext.Provider value={{ tasks, loading, error, addTask, toggleTask, deleteTask }}>
      {children}
    </TaskContext.Provider>
  );
}

export { TaskContext };
