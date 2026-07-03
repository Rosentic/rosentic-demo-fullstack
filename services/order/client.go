package order

import (
	"context"
	"fmt"
	"log"

	pb "github.com/rosentic/demo/proto/order"
	"google.golang.org/grpc"
)

type Client struct {
	conn   *grpc.ClientConn
	client pb.OrderServiceClient
}

func NewClient(addr string) (*Client, error) {
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		return nil, fmt.Errorf("failed to connect to order service: %w", err)
	}

	return &Client{
		conn:   conn,
		client: pb.NewOrderServiceClient(conn),
	}, nil
}

func (c *Client) Close() error {
	return c.conn.Close()
}

func (c *Client) CreateOrder(ctx context.Context, productID string, quantity int32, priority string) (*pb.OrderResponse, error) {
	req := &pb.OrderRequest{
		ProductId: productID,
		Quantity:  quantity,
		Priority:  priority,
	}

	resp, err := c.client.CreateOrder(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("CreateOrder RPC failed: %w", err)
	}

	log.Printf("Created order %d: product=%s qty=%d priority=%s",
		resp.Id, resp.ProductId, resp.Quantity, resp.Priority)

	return resp, nil
}

func (c *Client) GetOrder(ctx context.Context, id int64) (*pb.OrderResponse, error) {
	resp, err := c.client.GetOrder(ctx, &pb.GetOrderRequest{Id: id})
	if err != nil {
		return nil, fmt.Errorf("GetOrder RPC failed: %w", err)
	}
	return resp, nil
}

func (c *Client) CreateBulkOrders(ctx context.Context, items []struct {
	ProductID string
	Quantity  int32
	Priority  string
}) ([]*pb.OrderResponse, error) {
	var results []*pb.OrderResponse
	for _, item := range items {
		resp, err := c.CreateOrder(ctx, item.ProductID, item.Quantity, item.Priority)
		if err != nil {
			return results, fmt.Errorf("bulk order failed at product %s: %w", item.ProductID, err)
		}
		results = append(results, resp)
	}
	return results, nil
}
