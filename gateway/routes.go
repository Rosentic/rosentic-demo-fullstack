package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"`
}

func main() {
	mux := http.NewServeMux()

	// GET /api/v2/users/:userId — fetch a single user by userId
	mux.HandleFunc("/api/v2/users/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		parts := strings.Split(r.URL.Path, "/")
		if len(parts) < 5 {
			http.Error(w, "Missing userId", http.StatusBadRequest)
			return
		}
		userId := parts[4]

		user := User{
			ID:    1,
			Name:  "Alice",
			Email: "alice@example.com",
			Role:  "admin",
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(user)
		fmt.Printf("Fetched user with userId=%s\n", userId)
	})

	// GET /api/v2/users — list all users
	mux.HandleFunc("/api/v2/users", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		users := []User{
			{ID: 1, Name: "Alice", Email: "alice@example.com", Role: "admin"},
			{ID: 2, Name: "Bob", Email: "bob@example.com", Role: "member"},
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(users)
	})

	fmt.Println("Gateway listening on :8080")
	http.ListenAndServe(":8080", mux)
}
