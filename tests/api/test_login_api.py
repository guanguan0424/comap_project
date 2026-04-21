import os

import pytest

from framework.api.assertions import assert_json_has_keys, assert_status, get_json_value


@pytest.mark.api
def test_login_success_example(api_client):
    """
    这是一个示例用例：请根据你的系统把 LOGIN_PATH / 字段名改成真实值。
    为了避免把账号密码写死在仓库里，优先从环境变量读取。
    """
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")

    login_path = os.getenv("LOGIN_PATH", "/api/login")
    username = os.getenv("TEST_USERNAME", "demo")
    password = os.getenv("TEST_PASSWORD", "demo")

    resp = api_client.post(login_path, json={"username": username, "password": password})
    # 很多系统会返回 200/201/204 或者 401；这里先按成功示例写 200
    assert_status(resp, 200)
    assert_json_has_keys(resp, "token")
    token = get_json_value(resp, "token")
    assert isinstance(token, str) and token

