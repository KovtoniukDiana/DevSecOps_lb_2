import pytest

from dragon_clinic.config import load_config, mask_dsn

# Явно тестовий рядок. Він відповідає формату правила, тому хук його б зупинив:
# точковий виняток коментарем gitleaks:allow (обґрунтування — у звіті, крок 6).
TEST_DSN = "dragondb://test:test-password-0000@localhost/test"  # gitleaks:allow


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DRAGON_DB_URL", TEST_DSN)
    monkeypatch.setenv("APP_ENV", "dev")
    cfg = load_config()
    assert cfg["DRAGON_DB_URL"].startswith("dragondb://test:")
    assert cfg["LOG_LEVEL"] == "INFO"


def test_missing_variable_stops_app(monkeypatch):
    monkeypatch.delenv("DRAGON_DB_URL", raising=False)
    monkeypatch.setenv("APP_ENV", "dev")
    with pytest.raises(SystemExit) as exc:
        load_config()
    assert "DRAGON_DB_URL" in str(exc.value)


def test_bad_format_message_has_no_password(monkeypatch):
    monkeypatch.setenv("DRAGON_DB_URL", "postgres://test:test-password-0000@h/db")
    monkeypatch.setenv("APP_ENV", "dev")
    with pytest.raises(SystemExit) as exc:
        load_config()
    assert "test-password-0000" not in str(exc.value)


def test_mask_dsn_hides_password():
    assert "test-password-0000" not in mask_dsn(TEST_DSN)
    assert mask_dsn(TEST_DSN) == "dragondb://test:***@localhost/test"
