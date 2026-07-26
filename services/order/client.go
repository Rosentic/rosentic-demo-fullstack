package order

import (
	"context"
	"fmt"

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

func (c *Client) CreateOrder(ctx context.Context, productID string, quantity int32) (*pb.OrderResponse, error) {
	req := &pb.OrderRequest{
		ProductId: productID,
		Quantity:  quantity,
	}

	resp, err := c.client.CreateOrder(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("CreateOrder RPC failed: %w", err)
	}

	return resp, nil
}

func (c *Client) GetOrder(ctx context.Context, id int64) (*pb.OrderResponse, error) {
	resp, err := c.client.GetOrder(ctx, &pb.GetOrderRequest{Id: id})
	if err != nil {
		return nil, fmt.Errorf("GetOrder RPC failed: %w", err)
	}
	return resp, nil
}
