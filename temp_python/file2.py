from .time_utils import now_iso


def append_string(text: str) -> str:
    return f"{text} string"


def timestamped(text: str) -> str:
    return f"{now_iso()} - {text}"
