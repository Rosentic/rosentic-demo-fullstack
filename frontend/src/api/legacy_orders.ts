import axios from "axios";
import { z } from "zod";

export const LegacyCreateOrderSchema = z.object({
  product_id: z.string(),
  quantity: z.number().min(1),
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
  const response = await axios.post("/api/orders", validated);
  return response.data;
}
