"""Notification service — sends emails and push notifications."""


def send_notification(user_id: str, message: str) -> bool:
    """Send a notification to a user."""
    print(f"Sending notification to {user_id}: {message}")
    return True


def send_bulk_notifications(user_ids: list, message: str) -> dict:
    """Send notifications to multiple users."""
    results = {}
    for uid in user_ids:
        results[uid] = send_notification(uid, message)
    return results
