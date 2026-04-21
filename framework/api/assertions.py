from __future__ import annotations

from typing import Any, Dict, List

from framework.api.client import APIResponse


def assert_status(resp: APIResponse, expected: int) -> None:
    """断言HTTP状态码"""
    assert resp.status_code == expected, f"expected status {expected}, got {resp.status_code}; body={resp.text[:500]}"


def assert_json_has_keys(resp: APIResponse, *keys: str) -> None:
    """断言JSON响应包含指定键"""
    assert isinstance(resp.json, dict), f"expected json object, got {type(resp.json).__name__}; body={resp.text[:500]}"
    missing = [k for k in keys if k not in resp.json]
    assert not missing, f"missing keys: {missing}; json={resp.json}"


def assert_json_has_value(resp: APIResponse, key: str, expected_value: Any) -> None:
    """断言JSON响应中指定键的值"""
    assert isinstance(resp.json, dict), f"expected json object, got {type(resp.json).__name__}"
    assert key in resp.json, f"key '{key}' not found in response"
    assert resp.json[key] == expected_value, f"expected {expected_value}, got {resp.json[key]}"


def assert_response_success(resp: APIResponse) -> None:
    """断言API调用成功"""
    assert resp.status_code in [200, 201], f"expected success status, got {resp.status_code}"
    if isinstance(resp.json, dict):
        assert resp.json.get('success', True) == True, f"API responded with failure: {resp.json}"


def assert_response_error(resp: APIResponse, expected_code: int = 400) -> None:
    """断言API调用返回错误"""
    assert resp.status_code == expected_code, f"expected error status {expected_code}, got {resp.status_code}"
    if isinstance(resp.json, dict):
        assert resp.json.get('success', False) == False, f"API responded with success but expected error"


def assert_json_matches_schema(resp: APIResponse, schema_keys: List[str]) -> None:
    """断言JSON响应符合预期的模式"""
    assert isinstance(resp.json, dict), f"expected json object, got {type(resp.json).__name__}"
    
    response_keys = set(resp.json.keys())
    schema_keys_set = set(schema_keys)
    
    # 检查所有必需的键都在响应中
    missing_keys = schema_keys_set - response_keys
    assert not missing_keys, f"missing required keys: {missing_keys}"


def assert_list_length(resp: APIResponse, list_key: str, expected_length: int) -> None:
    """断言列表类型的响应长度"""
    assert isinstance(resp.json, dict), f"expected json object, got {type(resp.json).__name__}"
    assert list_key in resp.json, f"key '{list_key}' not found"
    assert isinstance(resp.json[list_key], list), f"key '{list_key}' is not a list"
    assert len(resp.json[list_key]) == expected_length, f"expected length {expected_length}, got {len(resp.json[list_key])}"


def assert_string_contains(resp: APIResponse, key: str, substring: str) -> None:
    """断言字符串包含特定内容"""
    assert isinstance(resp.json, dict), f"expected json object, got {type(resp.json).__name__}"
    assert key in resp.json, f"key '{key}' not found"
    assert substring in str(resp.json[key]), f"expected '{substring}' in '{resp.json[key]}'"


def get_json_value(resp: APIResponse, key: str, default: Any = None) -> Any:
    """安全地获取JSON响应中的值"""
    if not isinstance(resp.json, dict):
        return default
    return resp.json.get(key, default)


def assert_response_time(resp: httpx.Response, max_time: float) -> None:
    """断言响应时间不超过最大限制"""
    elapsed = resp.elapsed.total_seconds()
    assert elapsed <= max_time, f"response time {elapsed:.2f}s exceeds limit of {max_time:.2f}s"

