const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export interface Order {
  id: number;
  product_id: string;
  quantity: number;
  status: "pending" | "confirmed" | "shipped" | "delivered";
}

export interface CreateOrderPayload {
  product_id: string;
  quantity: number;
  shipping_address: string;
}

export async function createOrder(
  payload: CreateOrderPayload
): Promise<Order> {
  const response = await fetch(`${API_BASE}/api/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      product_id: payload.product_id,
      quantity: payload.quantity,
      shipping_address: payload.shipping_address,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create order: ${response.statusText}`);
  }

  return response.json();
}

export async function getOrders(): Promise<Order[]> {
  const response = await fetch(`${API_BASE}/api/orders`);

  if (!response.ok) {
    throw new Error(`Failed to list orders: ${response.statusText}`);
  }

  return response.json();
}
