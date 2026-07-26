import axios from "axios";

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
  const response = await axios.post("/api/users", { name, email });
  return response.data;
}

export async function getLegacyUser(id: number): Promise<LegacyUser> {
  const response = await axios.get("/api/users/" + id);
  return response.data;
}

export async function listLegacyUsers(): Promise<LegacyUser[]> {
  const response = await axios.get("/api/users");
  return response.data;
}
