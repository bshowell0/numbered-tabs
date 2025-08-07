from dataclasses import dataclass
import os

DEFAULT_CURRENCY = "USD"


@dataclass(frozen=True)
class Settings:
    environment: str
    currency: str = DEFAULT_CURRENCY
    send_emails: bool = False


def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def load_settings() -> Settings:
    return Settings(
        environment=get_env("APP_ENV", "dev"),
        currency=get_env("APP_CURRENCY", DEFAULT_CURRENCY),
        send_emails=get_env("APP_SEND_EMAILS", "0") == "1",
    )
