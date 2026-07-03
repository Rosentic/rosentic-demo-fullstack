import axios from "axios";
import { z } from "zod";

export const CreateOrderSchema = z.object({
  product_id: z.string(),
  quantity: z.number().min(1),
});

export type CreateOrderPayload = z.infer<typeof CreateOrderSchema>;

export interface Order {
  id: number;
  product_id: string;
  quantity: number;
  status: "pending" | "confirmed" | "shipped" | "delivered";
}

export async function createOrder(payload: CreateOrderPayload): Promise<Order> {
  const validated = CreateOrderSchema.parse(payload);
  const response = await axios.post("/api/orders", validated);
  return response.data;
}

export async function getOrders(): Promise<Order[]> {
  const response = await axios.get("/api/orders");
  return response.data;
}

export async function cancelOrder(orderId: number): Promise<void> {
  await axios.post("/api/orders/" + orderId + "/cancel");
}
