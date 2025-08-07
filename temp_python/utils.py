import re
import time
from datetime import datetime
from typing import Any, Iterable, Iterator, List


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def snake_to_camel(name: str) -> str:
    return "".join(part.capitalize() or "_" for part in name.split("_"))


def percent_change(old: float, new: float) -> float:
    if old == 0:
        return float("inf") if new != 0 else 0.0
    return ((new - old) / old) * 100.0


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def chunks(items: Iterable[Any], size: int) -> Iterator[List[Any]]:
    chunk: List[Any] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            wrapper.last_elapsed_ms = elapsed_ms  # type: ignore[attr-defined]

    wrapper.last_elapsed_ms = 0.0  # type: ignore[attr-defined]
    return wrapper


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
