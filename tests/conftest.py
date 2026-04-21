import sys
import os
from pathlib import Path
from typing import Dict, Any

import pytest
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from framework.api.client import APIClient
from framework.config.settings import load_settings


@pytest.fixture(scope="session")
def settings():
    load_dotenv()
    return load_settings()


@pytest.fixture(scope="session")
def api_client(settings):
    """基础API客户端（无认证）"""
    return APIClient(base_url=settings.api_base_url)


@pytest.fixture(scope="session")
def api_client_with_auth(api_client, ui_credentials):
    """带认证的API客户端"""
    # 获取访问令牌的逻辑
    login_data = {
        "username": ui_credentials["username"],
        "password": ui_credentials["password"]
    }
    
    try:
        # 尝试获取访问令牌
        resp = api_client.post("/api/auth/login", json=login_data)
        if resp.status_code == 200 and "access_token" in resp.json:
            token = resp.json["access_token"]
            return api_client.with_bearer_token(token)
    except Exception:
        pass
    
    # 如果获取认证失败，返回基础客户端
    return api_client


@pytest.fixture(scope="session")
def admin_api_client(api_client):
    """管理员API客户端"""
    admin_credentials = {
        "username": os.getenv("ADMIN_USERNAME", "admin@example.com"),
        "password": os.getenv("ADMIN_PASSWORD", "admin123")
    }
    
    try:
        resp = api_client.post("/api/auth/login", json=admin_credentials)
        if resp.status_code == 200 and "access_token" in resp.json:
            token = resp.json["access_token"]
            return api_client.with_bearer_token(token)
    except Exception:
        pass
    
    return api_client


@pytest.fixture(scope="session")
def ui_base_url(settings):
    return settings.ui_base_url


@pytest.fixture(scope="session")
def ui_entry_url(settings):
    return settings.login_url


@pytest.fixture(scope="session")
def ui_credentials():
    return {
        "username": os.getenv("TEST_USERNAME", "lp@savehmi.com"),
        "password": os.getenv("TEST_PASSWORD", "123456"),
    }


@pytest.fixture(scope="session")
def admin_credentials():
    return {
        "username": os.getenv("ADMIN_USERNAME", "admin@example.com"),
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
    }


@pytest.fixture
def logged_in_page(page, ui_base_url, ui_credentials):
    """返回已登录状态的页面"""
    # 登录逻辑
    try:
        page.goto(f"{ui_base_url}/login")
        page.locator('input[name="username"]').fill(ui_credentials["username"])
        page.locator('input[name="password"]').fill(ui_credentials["password"])
        page.locator('button[type="submit"]').click()
        
        # 等待登录完成
        page.wait_for_url(f"{ui_base_url}/dashboard", timeout=10000)
        return page
    except Exception:
        # 如果登录失败，返回原始的页面对象
        return page


@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    """加载测试数据配置文件"""
    import yaml
    
    test_data_path = PROJECT_ROOT / "config" / "test_data.yaml"
    if test_data_path.exists():
        with open(test_data_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


@pytest.fixture(scope="session")
def run_live_tests():
    return os.getenv("RUN_LIVE_TESTS") == "1"


@pytest.fixture(scope="session", autouse=True)
def setup_reporting():
    """设置测试报告目录"""
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # 创建截图目录
    screenshots_dir = PROJECT_ROOT / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)


@pytest.fixture
def browser_context_args(browser_context_args):
    """配置浏览器的上下文参数"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def capture_failure_screenshot(request, page):
    """在测试失败时捕获截图"""
    yield
    
    if request.node.rep_call.failed:
        # 创建测试失败的截图
        test_name = request.node.name
        screenshot_path = f"screenshots/failure_{test_name}.png"
        page.screenshot(path=screenshot_path, full_page=True)


# Hook 在测试结束后调用
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """为每个测试创建报告以支持失败截图"""
    outcome = yield
    rep = outcome.get_result()
    
    # 为每个测试函数设置rep_call
    setattr(item, "rep_" + rep.when, rep)

