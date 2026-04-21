from __future__ import annotations

import time
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
from framework.ui.locators import (
    ReactVueLocators, FormLocators, ButtonLocators, 
    NavigationLocators, TableLocators, DialogLocators,
    create_fallback_locators
)


class BasePage:
    """所有页面对象的基础类"""
    
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/")
    
    def goto(self, path: str = "") -> None:
        """导航到页面"""
        url = f"{self.base_url}/{path}".strip("/")
        self.page.goto(url)
        self._wait_for_page_load()
    
    def _wait_for_page_load(self, timeout: int = 10000) -> None:
        """等待页面加载完成"""
        try:
            # 等待主要内容加载
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            # 如果网络空闲超时，至少等待DOM稳定
            pass
        
        # 额外等待时间确保React/Vue组件渲染
        time.sleep(1)
    
    def find_element(self, *locators: str, timeout: int = 5000) -> Optional[Locator]:
        """使用多个定位器策略查找元素"""
        for locator_str in locators:
            try:
                locator = self.page.locator(locator_str)
                if locator.first.is_visible(timeout=2000):
                    return locator
            except Exception:
                continue
        return None
    
    def click_element(self, element_name: str, element_type: str = None, timeout: int = 5000) -> bool:
        """智能点击元素"""
        locators = create_fallback_locators(element_name, element_type)
        element = self.find_element(*locators, timeout=timeout)
        
        if element:
            element.click()
            return True
        return False
    
    def fill_input(self, field_name: str, value: str, element_type: str = "input", timeout: int = 5000) -> bool:
        """填充输入字段"""
        locators = create_fallback_locators(field_name, element_type)
        element = self.find_element(*locators, timeout=timeout)
        
        if element:
            element.fill(value)
            return True
        return False
    
    def wait_for_text(self, text: str, timeout: int = 10000) -> None:
        """等待页面出现特定文本"""
        self.page.wait_for_selector(f"text={text}", timeout=timeout)
    
    def wait_for_element_hidden(self, element_name: str, timeout: int = 5000) -> None:
        """等待元素隐藏"""
        locators = create_fallback_locators(element_name)
        for locator_str in locators:
            try:
                self.page.wait_for_selector(locator_str, state="hidden", timeout=timeout)
                return
            except Exception:
                continue
    
    def take_screenshot(self, name: str = "screenshot") -> None:
        """截取页面截图"""
        timestamp = int(time.time())
        screenshot_path = f"screenshots/{name}_{timestamp}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
    
    def assert_element_visible(self, element_name: str, element_type: str = None) -> None:
        """断言元素可见"""
        locators = create_fallback_locators(element_name, element_type)
        element = self.find_element(*locators)
        assert element is not None, f"Element '{element_name}' not found"
        expect(element).to_be_visible()
    
    def assert_element_contains_text(self, element_name: str, text: str, element_type: str = None) -> None:
        """断言元素包含特定文本"""
        locators = create_fallback_locators(element_name, element_type)
        element = self.find_element(*locators)
        assert element is not None, f"Element '{element_name}' not found"
        expect(element).to_contain_text(text)
    
    def assert_url_contains(self, path: str) -> None:
        """断言URL包含特定路径"""
        current_url = self.page.url
        assert path in current_url, f"Expected URL to contain '{path}', got '{current_url}'"
    
    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.page.title()
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.page.url


class ModalDialog(BasePage):
    """模态对话框基类"""
    
    def __init__(self, page: Page, dialog_title: str = ""):
        super().__init__(page)
        self.dialog_title = dialog_title
    
    def wait_for_dialog_open(self, timeout: int = 5000) -> None:
        """等待对话框打开"""
        if self.dialog_title:
            self.wait_for_text(self.dialog_title, timeout)
    
    def close_dialog(self) -> None:
        """关闭对话框"""
        # 尝试常见关闭按钮
        close_buttons = [
            '[aria-label="Close"]',
            '.close-button',
            '.modal-close',
            'button:has-text("×")',
            'button:has-text("关闭")'
        ]
        
        for button in close_buttons:
            element = self.find_element(button)
            if element:
                element.click()
                self.wait_for_dialog_closed()
                return
    
    def wait_for_dialog_closed(self, timeout: int = 5000) -> None:
        """等待对话框关闭"""
        if self.dialog_title:
            self.wait_for_element_hidden(f"text={self.dialog_title}", timeout)


class AuthMixin:
    """认证相关功能混入类"""
    
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        # 检查常见的登录后元素
        indicators = [
            '[data-testid="user-menu"]',
            '.user-avatar',
            '.logout-button',
            '[data-testid="logout"]'
        ]
        
        for indicator in indicators:
            try:
                if self.page.locator(indicator).first.is_visible(timeout=2000):
                    return True
            except Exception:
                continue
        return False
    
    def logout(self) -> None:
        """退出登录"""
        if self.is_logged_in():
            user_menu_selectors = [
                '[data-testid="user-menu"]',
                '.user-avatar',
                '.profile-menu'
            ]
            
            # 点击用户菜单
            for selector in user_menu_selectors:
                try:
                    self.page.locator(selector).first.click(timeout=2000)
                    break
                except Exception:
                    continue
            
            # 点击退出登录
            logout_selectors = [
                'button:has-text("退出登录")',
                '[data-testid="logout"]',
                'a:has-text("Logout")'
            ]
            
            for selector in logout_selectors:
                try:
                    self.page.locator(selector).first.click(timeout=2000)
                    break
                except Exception:
                    continue