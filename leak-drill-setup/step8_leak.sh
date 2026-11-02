#!/usr/bin/env bash
# Крок 8. Запускати в теці, де буде клон leak-drill. Підставте ЛОГІН і вигаданий рядок (scripts/gen_fake_dsn.py).
set -e
LOGIN="<логін>"
FAKE_DSN="<вставте сюди вигаданий dragondb://… рядок>"

git clone "git@github.com:${LOGIN}/leak-drill.git" && cd leak-drill

echo "# Leak drill" > README.md
git add README.md && git commit -m "docs: опис полігону"

mkdir config && echo "DRAGON_DB_URL=${FAKE_DSN}" > config/settings.env
git add config && git commit -m "feat: підключення до бази"

git rm config/settings.env && git commit -m "fix: прибрати пароль з репозиторію"
git push -u origin main

# Далі вручну. Скопіюйте .gitleaks.toml з основного репозиторію в полігон (НЕ комітьте):
#   gitleaks dir . -v          # нічого не знайдено
#   gitleaks git -v            # пароль у старому коміті (запишіть хеш)
#   git log -p -S "dragondb://"
#   git log --oneline > ../hashes_before.txt
#   git log --show-signature > ../signatures_before.txt
