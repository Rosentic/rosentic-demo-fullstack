const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface User {
  id: number;
  name: string;
  email: string;
}

export async function createUser(name: string, email: string): Promise<User> {
  const response = await fetch(`${API_BASE}/api/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create user: ${response.statusText}`);
  }

  return response.json();
}

export async function getUser(id: number): Promise<User> {
  const response = await fetch(`${API_BASE}/api/users/${id}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`);
  }

  return response.json();
}

export async function listUsers(): Promise<User[]> {
  const response = await fetch(`${API_BASE}/api/users`);

  if (!response.ok) {
    throw new Error(`Failed to list users: ${response.statusText}`);
  }

  return response.json();
}
