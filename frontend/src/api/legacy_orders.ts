import axios from "axios";
import { z } from "zod";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export const LegacyCreateOrderSchema = z.object({
  product_id: z.string(),
  quantity: z.number().int().min(1),
});

export type LegacyCreateOrderPayload = z.infer<typeof LegacyCreateOrderSchema>;

export interface LegacyOrder {
  id: number;
  product_id: string;
  quantity: number;
  status: "pending" | "confirmed" | "shipped" | "delivered";
}

export async function createLegacyOrder(
  payload: LegacyCreateOrderPayload
): Promise<LegacyOrder> {
  const validated = LegacyCreateOrderSchema.parse(payload);
  const response = await axios.post(`${API_BASE}/api/orders`, validated);
  return response.data;
}
