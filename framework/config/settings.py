from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Settings:
    env: str
    api_base_url: str
    ui_base_url: str
    login_url: str


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data or {}


def load_settings() -> Settings:
    env = os.getenv("TEST_ENV", "test")
    root = _project_root()
    cfg = _load_yaml(root / "config" / f"{env}.yaml")

    api_base_url = os.getenv("API_BASE_URL", cfg.get("api_base_url", "http://localhost:8000")).rstrip("/")
    ui_base_url = os.getenv("UI_BASE_URL", cfg.get("ui_base_url", "http://localhost:3000")).rstrip("/")
    login_url = os.getenv("LOGIN_URL", cfg.get("login_url", f"{ui_base_url}/base/customers"))

    return Settings(env=env, api_base_url=api_base_url, ui_base_url=ui_base_url, login_url=login_url)

