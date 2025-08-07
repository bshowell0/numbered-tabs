from .time_utils import now_iso


def timestamped(text: str) -> str:
    return f"{now_iso()} - {text}"
