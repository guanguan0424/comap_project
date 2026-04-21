#!/usr/bin/env python3
"""完整登录流程测试 - 包含表单填写和登录的异常场景断言"""

import os
import time
import yaml
import allure
from playwright.sync_api import sync_playwright
from core.utils.screenshot_manager import take_screenshot

# 读取测试数据
def load_test_data():
    """从配置文件加载测试数据"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "config", "test_data.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 通用配置
LOGIN_URL = "http://risemap-dev.savehmi.cn/base/customers"

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("用户登录")
@allure.story("正确凭据登录场景")
def test_valid_credentials_login():
    """测试正确凭据登录"""
    with allure.step("准备测试数据"):
        test_data = load_test_data()
        valid_cred = test_data["ui_test_data"]["login_form"]["valid_credentials"]
        allure.attach(str(valid_cred), name="测试数据", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("启动浏览器并执行登录测试"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            page.set_viewport_size({"width": 1200, "height": 800})
            
            with allure.step("访问登录页面"):
                page.goto(LOGIN_URL)
                page.wait_for_load_state("networkidle")
            
            with allure.step("验证页面元素"):
                assert page.locator("input").count() > 0, "页面上应该存在输入框"
                assert page.locator("button").count() > 0, "页面上应该存在按钮"
                
            with allure.step("填写登录表单"):
                fill_login_form(page, valid_cred["username"], valid_cred["password"])
                
            with allure.step("提交登录并验证结果"):
                result = submit_login_form(page)
                screenshot_info = take_screenshot(page, test_valid_credentials_login, "正确凭据登录成功截图")
                allure.attach.file(screenshot_info['files'][0]['path'], name="登录后页面截图", attachment_type=allure.attachment_type.PNG)
                
                # 断言：成功登录应该跳转页面
                assert result["status"] == "success", f"正确凭据登录应该成功，实际结果: {result['status']}"
            
            browser.close()

@allure.severity(allure.severity_level.NORMAL)
@allure.feature("用户登录")
@allure.story("错误凭据登录场景")
def test_invalid_credentials_login():
    """测试错误凭据登录"""
    with allure.step("准备测试数据"):
        test_data = load_test_data()
        invalid_cred = test_data["ui_test_data"]["login_form"]["invalid_credentials"]
        allure.attach(str(invalid_cred), name="测试数据", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("启动浏览器并执行测试"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            
            with allure.step("访问登录页面"):
                page.goto(LOGIN_URL)
                page.wait_for_load_state("networkidle")
            
            with allure.step("填写错误凭据"):
                fill_login_form(page, invalid_cred["username"], invalid_cred["password"])
                
            with allure.step("验证登录失败"):
                result = submit_login_form(page)
                screenshot_info = take_screenshot(page, test_invalid_credentials_login, "错误凭据登录失败截图")
                allure.attach.file(screenshot_info['files'][0]['path'], name="错误凭据登录截图", attachment_type=allure.attachment_type.PNG)
                
                # 断言：错误凭据应该失败
                assert result["status"] in ["error", "no_change"], f"错误凭据登录应该失败，实际结果: {result['status']}"
            
            browser.close()

@allure.severity(allure.severity_level.NORMAL)
@allure.feature("用户登录")
@allure.story("空凭据登录场景")
def test_empty_credentials_login():
    """测试空凭据登录"""
    with allure.step("准备测试数据"):
        test_data = load_test_data()
        empty_cred = test_data["ui_test_data"]["login_form"]["empty_credentials"]
        allure.attach(str(empty_cred), name="测试数据", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("启动浏览器测试空凭据"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            
            with allure.step("访问登录页面"):
                page.goto(LOGIN_URL)
                page.wait_for_load_state("networkidle")
            
            with allure.step("直接提交空表单"):
                # 直接尝试提交空表单
                result = submit_login_form(page)
                screenshot_info = take_screenshot(page, test_empty_credentials_login, "空凭据登录验证截图")
                allure.attach.file(screenshot_info['files'][0]['path'], name="空凭据登录截图", attachment_type=allure.attachment_type.PNG)
                
                # 断言：空凭据应该被阻止
                assert result["status"] in ["no_change", "error"], f"空凭据登录应该被阻止，实际结果: {result['status']}"
            
            browser.close()

@allure.severity(allure.severity_level.NORMAL)
@allure.feature("用户登录")
@allure.story("正确用户名错误密码场景")
def test_incorrect_password_login():
    """测试正确用户名错误密码登录"""
    with allure.step("准备测试数据"):
        test_data = load_test_data()
        incorrect_cred = test_data["ui_test_data"]["login_form"]["incorrect_credentials"]
        allure.attach(str(incorrect_cred), name="测试数据", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("启动浏览器并执行测试"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            
            with allure.step("访问登录页面"):
                page.goto(LOGIN_URL)
                page.wait_for_load_state("networkidle")
            
            with allure.step("填写正确用户名错误密码"):
                fill_login_form(page, incorrect_cred["username"], incorrect_cred["password"])
                
            with allure.step("验证登录失败"):
                result = submit_login_form(page)
                screenshot_info = take_screenshot(page, test_incorrect_password_login, "密码错误登录失败截图")
                allure.attach.file(screenshot_info['files'][0]['path'], name="密码错误登录截图", attachment_type=allure.attachment_type.PNG)
                
                # 断言：正确用户名错误密码应该失败
                assert result["status"] in ["error", "no_change"], f"密码错误登录应该失败，实际结果: {result['status']}"
            
            browser.close()

def fill_login_form(page, username, password):
    """填写登录表单"""
    print("[FORM] 开始填写登录表单...")
    
    # 查找并填写用户名
    username_selectors = [
        "input[type='email']", "input[type='text']",
        "input[name='username']", "input[name='email']",
        "#username", "#email"
    ]
    
    for selector in username_selectors:
        if page.locator(selector).count() > 0:
            username_input = page.locator(selector).first
            username_input.click()
            username_input.fill(username)
            print(f"[INPUT] 已填写用户名: {username}")
            time.sleep(1)
            break
    
    # 查找并填写密码
    password_selectors = [
        "input[type='password']", "input[name='password']", "#password"
    ]
    
    for selector in password_selectors:
        if page.locator(selector).count() > 0:
            password_input = page.locator(selector).first
            password_input.click()
            password_input.fill(password)
            print(f"[INPUT] 已填写密码: {'*' * len(password) if password else '空'}")
            time.sleep(1)
            break
    
    take_screenshot(page, "form_filling", "表单填写完成截图")
    print("[SCREENSHOT] 表单填写完成")

def submit_login_form(page):
    """提交登录表单并返回结果"""
    original_url = page.url
    original_title = page.title()
    
    # 查找并点击登录按钮
    button_selectors = [
        "button[type='submit']", "button:has-text('登录')",
        "button:has-text('Login')", "input[type='submit']"
    ]
    
    for selector in button_selectors:
        if page.locator(selector).count() > 0:
            login_button = page.locator(selector).first
            print("[CLICK] 点击登录按钮...")
            login_button.click()
            
            # 等待响应
            time.sleep(3)
            try:
                page.wait_for_load_state("networkidle")
            except:
                pass  # 页面可能没有网络请求
            
            # 判断登录结果
            current_url = page.url
            current_title = page.title()
            
            # 检查是否有错误信息
            error_selectors = [
                ".error", ".alert-danger", ".error-message",
                "[role='alert']", "[data-error='true']"
            ]
            
            error_message = ""
            for error_selector in error_selectors:
                if page.locator(error_selector).count() > 0:
                    error_message = page.locator(error_selector).first.inner_text()
                    break
            
            if current_url != original_url:
                return {"status": "success", "message": "页面跳转"}
            elif error_message:
                return {"status": "error", "message": error_message}
            else:
                return {"status": "no_change", "message": "页面无变化"}
    
    return {"status": "no_button", "message": "未找到登录按钮"}

if __name__ == "__main__":
    test_complete_login()

if __name__ == "__main__":
    test_complete_login()