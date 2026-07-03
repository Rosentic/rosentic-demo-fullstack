"""Welcome job — sends onboarding notifications to new users."""

from backend.services.notifications import send_notification, send_bulk_notifications


def welcome_new_user(user_id: str, name: str):
    """Send welcome notification when a user signs up."""
    message = f"Welcome to the platform, {name}! Check out our getting started guide."
    send_notification(user_id, message)


def remind_inactive_users(user_ids: list):
    """Remind inactive users to complete onboarding."""
    message = "You haven't finished setting up your account. Need help?"
    results = send_bulk_notifications(user_ids, message)
    failed = [uid for uid, ok in results.items() if not ok]
    if failed:
        print(f"Failed to notify {len(failed)} users: {failed}")


def send_trial_followups(user_id: str, team_ids: list[str]):
    """Send onboarding reminders for a trial account."""
    send_notification(user_id, "Your trial workspace is ready")
    send_bulk_notifications(team_ids, "A teammate has opened a trial workspace")
