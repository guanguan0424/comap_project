from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class APIResponse:
    status_code: int
    json: Any | None
    text: str
    headers: dict[str, str]


class APIClient:
    def __init__(self, base_url: str, timeout: float = 10.0, default_headers: dict[str, str] | None = None):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=default_headers or {},
        )

    def with_bearer_token(self, token: str) -> "APIClient":
        headers = dict(self._client.headers)
        headers["Authorization"] = f"Bearer {token}"
        return APIClient(base_url=self.base_url, timeout=float(self._client.timeout), default_headers=headers)

    def get(self, path: str, **kwargs) -> APIResponse:
        r = self._client.get(path, **kwargs)
        return self._wrap(r)

    def post(self, path: str, json: Any = None, **kwargs) -> APIResponse:
        r = self._client.post(path, json=json, **kwargs)
        return self._wrap(r)

    def put(self, path: str, json: Any = None, **kwargs) -> APIResponse:
        r = self._client.put(path, json=json, **kwargs)
        return self._wrap(r)

    def delete(self, path: str, **kwargs) -> APIResponse:
        r = self._client.delete(path, **kwargs)
        return self._wrap(r)

    @staticmethod
    def _wrap(r: httpx.Response) -> APIResponse:
        try:
            data = r.json()
        except Exception:
            data = None
        return APIResponse(
            status_code=r.status_code,
            json=data,
            text=r.text,
            headers={k: v for k, v in r.headers.items()},
        )

