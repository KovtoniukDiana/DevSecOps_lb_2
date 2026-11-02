#!/usr/bin/env bash
# Крок 9. Чистка історії (ЛИШЕ в полігоні!). replacements.txt і .gitleaks.toml лежать у батьківській теці.
set -e
LOGIN="<логін>"

cd ..   # вийти з leak-drill
git clone "git@github.com:${LOGIN}/leak-drill.git" leak-drill-clean
cd leak-drill-clean

git filter-repo --replace-text ../replacements.txt
git remote add origin "git@github.com:${LOGIN}/leak-drill.git"   # filter-repo видаляє origin
git push --force --all
git push --force --tags

cp ../.gitleaks.toml .gitleaks.toml    # лише для перевірки, не комітити
gitleaks git -v                        # очікуємо: no leaks found
git log --oneline > ../hashes_after.txt
git log --show-signature > ../signatures_after.txt
diff ../hashes_before.txt ../hashes_after.txt || true
