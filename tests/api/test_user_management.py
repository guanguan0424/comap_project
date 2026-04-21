import os
import uuid
from typing import Dict, Any

import pytest

from framework.api.assertions import (
    assert_status, assert_json_has_keys, assert_response_success,
    assert_json_has_value, assert_response_error
)


@pytest.mark.api
@pytest.mark.user_management
class TestUserManagementAPI:
    """用户管理API测试用例"""
    
    def test_user_registration(self, api_client):
        """测试用户注册功能"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        # 生成唯一用户名避免重复
        unique_id = str(uuid.uuid4())[:8]
        email = f"testuser_{unique_id}@example.com"
        
        registration_data = {
            "email": email,
            "username": f"testuser_{unique_id}",
            "password": "TestPassword123!",
            "role": "user"
        }
        
        resp = api_client.post("/api/users/register", json=registration_data)
        assert_response_success(resp)
        assert_json_has_keys(resp, "user_id", "email", "username")
        assert_json_has_value(resp, "email", email)
    
    def test_user_login(self, api_client):
        """测试用户登录功能"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        login_data = {
            "username": os.getenv("TEST_USERNAME", "demo"),
            "password": os.getenv("TEST_PASSWORD", "demo")
        }
        
        resp = api_client.post("/api/auth/login", json=login_data)
        assert_response_success(resp)
        assert_json_has_keys(resp, "access_token", "token_type", "expires_in")
        assert_json_has_value(resp, "token_type", "bearer")
    
    def test_get_user_profile(self, api_client_with_auth):
        """测试获取用户个人信息"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        resp = api_client_with_auth.get("/api/users/profile")
        assert_response_success(resp)
        assert_json_has_keys(resp, "user_id", "username", "email", "role")
    
    def test_update_user_profile(self, api_client_with_auth):
        """测试更新用户个人信息"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        update_data = {
            "name": "更新后的用户名",
            "phone": "13800138000"
        }
        
        resp = api_client_with_auth.put("/api/users/profile", json=update_data)
        assert_response_success(resp)
        assert_json_has_keys(resp, "user_id", "username", "email", "name", "phone")
    
    def test_user_login_invalid_credentials(self, api_client):
        """测试使用无效凭证登录（预期失败）"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        invalid_login_data = {
            "username": "invalid_user",
            "password": "wrong_password"
        }
        
        resp = api_client.post("/api/auth/login", json=invalid_login_data)
        assert_response_error(resp, 401)
    
    def test_user_registration_duplicate_email(self, api_client):
        """测试重复邮箱注册（预期失败）"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        duplicate_email = "duplicate@example.com"
        
        # 第一次注册
        registration_data = {
            "email": duplicate_email,
            "username": "user1",
            "password": "TestPassword123!"
        }
        
        resp1 = api_client.post("/api/users/register", json=registration_data)
        
        # 第二次注册相同邮箱
        resp2 = api_client.post("/api/users/register", json=registration_data)
        assert_response_error(resp2, 400)


@pytest.mark.api
@pytest.mark.user_permissions
class TestUserPermissionsAPI:
    """用户权限API测试用例"""
    
    def test_admin_access_restricted_endpoint(self, admin_api_client):
        """测试管理员访问受限端点"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        resp = admin_api_client.get("/api/admin/users")
        assert_response_success(resp)
        assert_json_has_keys(resp, "users", "total_count")
    
    def test_normal_user_access_restricted_endpoint(self, api_client_with_auth):
        """测试普通用户访问受限端点（预期失败）"""
        if os.getenv("RUN_LIVE_TESTS") != "1":
            pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
        
        resp = api_client_with_auth.get("/api/admin/users")
        assert_response_error(resp, 403)


@pytest.mark.api
@pytest.mark.parametrize("test_data", [
    {"email": "valid@example.com", "password": "ValidPass123"},
    {"email": "test.user@example.com", "password": "TestUser123"},
])
def test_multiple_login_scenarios(api_client, test_data):
    """参数化测试多种登录场景"""
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_TESTS=1 to run against a real environment")
    
    resp = api_client.post("/api/auth/login", json=test_data)
    assert_response_success(resp)
    assert_json_has_keys(resp, "access_token")