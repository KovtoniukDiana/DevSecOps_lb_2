"""Генерує ВИГАДАНИЙ рядок підключення формату dragondb://<користувач>:<пароль>@<хост>/<база>."""
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(20))
print(f"dragondb://app_user:{password}@db.clinic.local/patients")
