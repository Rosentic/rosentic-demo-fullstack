import axios from "axios";

export interface User {
  id: number;
  name: string;
  email: string;
  avatar?: string;
}

export async function createUser(name: string, email: string): Promise<User> {
  const response = await axios.post("/api/users", { name, email });
  return response.data;
}

export async function getUser(id: number): Promise<User> {
  const response = await axios.get("/api/users/" + id);
  return response.data;
}

export async function listUsers(): Promise<User[]> {
  const response = await axios.get("/api/users");
  return response.data;
}

export async function updateUser(id: number, updates: Partial<User>): Promise<User> {
  const response = await axios.patch("/api/users/" + id, updates);
  return response.data;
}

export async function deleteUser(id: number): Promise<void> {
  await axios.delete("/api/users/" + id);
}
