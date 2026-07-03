"""Trial reminder job with stale notification call."""

from backend.services.notifications import send_notification


def remind_trial_owner(user_id: str):
    send_notification(user_id, "Your trial workspace expires tomorrow")
