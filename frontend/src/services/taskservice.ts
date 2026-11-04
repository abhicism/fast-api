
import type { Task } from "../types/Task";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `API request failed (${response.status})`);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export type { Task };

// Retrieve all tasks from FastAPI.
export const getTasks = (): Promise<Task[]> => request("/tasks");

// Create a task in the backend database.
export const createTask = (title: string): Promise<Task> =>
  request("/tasks", {
    method: "POST",
    body: JSON.stringify({ title, completed: false }),
  });

// Update task fields in the backend database.
export const updateTask = (
  id: number,
  changes: Partial<Omit<Task, "id">>,
): Promise<Task> =>
  request(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(changes) });

// Delete a task from the backend database.
export const deleteTask = (id: number): Promise<void> =>
  request(`/tasks/${id}`, { method: "DELETE" });
