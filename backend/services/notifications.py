"""Notification service — sends emails and push notifications."""


def send_notification(user_id: str, message: str, channel: str) -> bool:
    """Send a notification to a user."""
    print(f"Sending {channel} notification to {user_id}: {message}")
    return True


def send_bulk_notifications(user_ids: list, message: str, channel: str) -> dict:
    """Send notifications to multiple users through the selected channel."""
    results = {}
    for uid in user_ids:
        results[uid] = send_notification(uid, message, channel)
    return results
