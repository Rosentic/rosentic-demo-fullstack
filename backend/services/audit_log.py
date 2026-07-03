"""Local audit helpers for demo events."""


def format_audit_event(actor: str, action: str) -> str:
    return f"{actor}: {action}"
