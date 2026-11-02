"""Конфігурація застосунку «Драконяча клініка»: усе береться із середовища."""
import os
import re
import sys

REQUIRED = ["DRAGON_DB_URL", "APP_ENV"]

# dragondb://<користувач>:<пароль>@<хост>/<база>
_DSN_RE = re.compile(r"^dragondb://([^\s:@/]+):([^\s@/]+)@([^\s/]+)/(\S+)$")


def mask_dsn(dsn: str) -> str:
    """Повертає рядок підключення без пароля — його безпечно писати в журнал."""
    return re.sub(r"(dragondb://[^\s:@/]+:)[^\s@/]+(@)", r"\1***\2", dsn)


def load_config() -> dict:
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        # називаємо змінні, але ніколи не друкуємо значень
        sys.exit(f"Не задано змінні середовища: {', '.join(missing)}. "
                 "Скопіюйте .env.example у .env і заповніть значення.")

    dsn = os.environ["DRAGON_DB_URL"]
    if not _DSN_RE.match(dsn):
        # повідомлення без значення: у ньому може бути пароль
        sys.exit("DRAGON_DB_URL має формат dragondb://<користувач>:<пароль>@<хост>/<база>.")

    return {
        "DRAGON_DB_URL": dsn,
        "APP_ENV": os.environ["APP_ENV"],
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    }
