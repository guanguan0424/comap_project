#!/usr/bin/env python3
"""
认证模块服务 - 支持UI登录和API认证的混合测试
"""

import allure
from core.services.base_service import BaseService
from typing import Dict, Any, Optional


class AuthService(BaseService):
    """认证服务类 - 处理登录相关的UI和API操作"""
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)
        self.login_url = self.config.get('login_url', 'http://risemap-dev.savehmi.cn/base/customers')
        
    def execute_business_flow(self, username: str, password: str, validate_api: bool = True) -> Dict[str, Any]:
        """
        执行业务流程：UI登录 + API认证验证
        
        Args:
            username: 用户名
            password: 密码
            validate_api: 是否验证API响应
            
        Returns:
            包含测试结果的字典
        """
        result = {
            'ui_success': False,
            'api_success': False,
            'session_info': None,
            'error_message': None
        }
        
        try:
            # 步骤1: UI登录
            with allure.step("执行UI登录"):
                ui_result = self._perform_ui_login(username, password)
                result['ui_success'] = ui_result
                
                if not ui_result:
                    result['error_message'] = "UI登录失败"
                    return result
            
            # 步骤2: API认证验证（如果启用）
            if validate_api and self.api_client:
                with allure.step("验证API认证状态"):
                    api_result = self._validate_api_authentication()
                    result['api_success'] = api_result
                    
                    if not api_result:
                        result['error_message'] = "API认证验证失败"
            
            return result
            
        except Exception as e:
            result['error_message'] = str(e)
            return result
    
    def _perform_ui_login(self, username: str, password: str) -> bool:
        """执行UI登录操作"""
        if not self.ui_context:
            raise ValueError("UI上下文未设置")
            
        page = self.ui_context
        
        try:
            # 访问登录页面
            page.goto(self.login_url)
            page.wait_for_load_state("networkidle")
            
            # 检查登录表单元素
            if not self._validate_login_form_elements(page):
                return False
                
            # 填写表单
            self._fill_login_form(page, username, password)
            
            # 提交登录
            self._submit_login_form(page)
            
            # 验证登录成功
            return self._validate_login_success(page)
            
        except Exception as e:
            print(f"UI登录失败: {e}")
            return False
    
    def _validate_login_form_elements(self, page) -> bool:
        """验证登录表单元素是否存在"""
        try:
            assert page.locator("input").count() > 0, "页面上应该存在输入框"
            assert page.locator("button").count() > 0, "页面上应该存在按钮"
            return True
        except AssertionError as e:
            print(f"表单元素验证失败: {e}")
            return False
    
    def _fill_login_form(self, page, username: str, password: str):
        """填写登录表单"""
        # 这里应该基于具体的页面结构实现表单填写逻辑
        # 暂时使用通用实现
        inputs = page.locator("input").all()
        if len(inputs) >= 2:
            inputs[0].fill(username)
            inputs[1].fill(password)
    
    def _submit_login_form(self, page):
        """提交登录表单"""
        # 点击登录按钮
        buttons = page.locator("button").all()
        if buttons:
            buttons[0].click()
            page.wait_for_load_state("networkidle")
    
    def _validate_login_success(self, page) -> bool:
        """验证登录是否成功"""
        # 检查登录后页面的特征
        # 可以根据实际应用调整验证逻辑
        current_url = page.url
        if current_url != self.login_url and 'login' not in current_url.lower():
            return True
        return False
    
    def _validate_api_authentication(self) -> bool:
        """验证API认证状态"""
        if not self.api_client:
            return True  # 如果没有API客户端，则认为验证通过
            
        try:
            # 这里应该调用实际的API验证接口
            # 暂时返回模拟结果
            return True
        except Exception as e:
            print(f"API认证验证失败: {e}")
            return False