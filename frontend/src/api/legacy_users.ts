import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface LegacyUser {
  id: number;
  name: string;
  email: string;
  avatar?: string;
}

export async function createLegacyUser(
  name: string,
  email: string
): Promise<LegacyUser> {
  const response = await axios.post(`${API_BASE}/api/users`, { name, email });
  return response.data;
}

export async function getLegacyUser(id: number): Promise<LegacyUser> {
  const response = await axios.get(`${API_BASE}/api/users/${id}`);
  return response.data;
}

export async function listLegacyUsers(): Promise<LegacyUser[]> {
  const response = await axios.get(`${API_BASE}/api/users`);
  return response.data;
}
