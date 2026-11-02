#!/usr/bin/env bash
# Додаткове завдання (варіант 3): правило ловить пароль усередині рядка підключення
# (secretGroup), а рядок без пароля dragondb://host/db — ні.
# Запуск з кореня репозиторію: bash scripts/demo_rule.sh
set -u
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

echo "$(python scripts/gen_fake_dsn.py)"        > "$tmp/bad.txt"
echo "dragondb://host/db"                       > "$tmp/good_no_password.txt"
echo "dragondb://app_user@host/db"              > "$tmp/good_no_user_password.txt"
echo "dragondb://app_user:<пароль>@host/db"     > "$tmp/good_placeholder.txt"

echo "=== Очікуємо рівно 1 знахідку: bad.txt ==="
gitleaks dir "$tmp" -c .gitleaks.toml -v
