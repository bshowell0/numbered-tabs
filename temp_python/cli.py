import argparse

from .services import list_active_users
from .tasks import seed_example_data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="temp_python")
    parser.add_argument("--seed", action="store_true")
    args = parser.parse_args(argv)

    if args.seed:
        seed_example_data()
    for user in list_active_users():
        print(f"{user.id}: {user.name} <{user.email}>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
