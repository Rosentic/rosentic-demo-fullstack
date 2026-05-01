"""Sync script — pulls user data from the gateway API for offline processing."""

import requests
import json
import sys
from datetime import datetime


def sync_users():
    """Fetch all users from the gateway and write to local cache."""
    base_url = "http://localhost:8080"

    # Fetch user list
    resp = requests.get(f"{base_url}/api/users")
    resp.raise_for_status()
    users = resp.json()

    print(f"Found {len(users)} users")

    # Fetch each user detail
    for user in users:
        user_id = user["id"]
        detail = requests.get(f"{base_url}/api/users/{user_id}")
        detail.raise_for_status()
        print(f"  Synced user {user_id}: {detail.json()['name']}")

    # Write cache
    with open("cache/users.json", "w") as f:
        json.dump({"synced_at": datetime.now().isoformat(), "users": users}, f, indent=2)

    print("Sync complete.")


def sync_orders():
    """Fetch all orders and write to cache."""
    base_url = "http://localhost:8080"

    resp = requests.get(f"{base_url}/api/orders")
    resp.raise_for_status()
    orders = resp.json()

    print(f"Found {len(orders)} orders")

    with open("cache/orders.json", "w") as f:
        json.dump({"synced_at": datetime.now().isoformat(), "orders": orders}, f, indent=2)


if __name__ == "__main__":
    sync_users()
    sync_orders()
