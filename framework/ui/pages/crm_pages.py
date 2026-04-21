from __future__ import annotations

from playwright.sync_api import Page, expect


class CRMTopNav:
    def __init__(self, page: Page):
        self.page = page

    def _click_nav_item(self, name: str) -> bool:
        candidates = [
            self.page.get_by_role("link", name=name),
            self.page.get_by_role("button", name=name),
            self.page.get_by_role("tab", name=name),
            self.page.get_by_text(name, exact=True),
            self.page.get_by_text(name),
        ]
        for locator in candidates:
            try:
                target = locator.first
                if target.is_visible(timeout=2000):
                    target.click()
                    return True
            except Exception:
                continue
        return False

    def goto_public_sea(self, base_url: str) -> None:
        # Prefer entering customer module first, then switch to public sea.
        self.page.goto(f"{base_url}/base/customers")
        clicked = self._click_nav_item("公海客户")
        if not clicked:
            # Some builds expose public sea as an independent route.
            self.page.goto(f"{base_url}/base/public-customers")
        expect(self.page.get_by_text("公海客户")).to_be_visible()

    def goto_customer_management(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/base/customers")
        if not self._click_nav_item("客户管理"):
            # If already inside customer module, no extra click is required.
            pass
        expect(self.page.get_by_text("客户管理")).to_be_visible()

    def goto_followup_records(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/base/customers")
        if not self._click_nav_item("跟进记录"):
            # Fallback route name for followup module.
            self.page.goto(f"{base_url}/base/followup-records")
        expect(self.page.get_by_text("跟进记录管理")).to_be_visible()


class PublicSeaPage:
    def __init__(self, page: Page):
        self.page = page

    def open_create_dialog(self) -> None:
        self.page.get_by_role("button", name="新建公海客户").click()
        expect(self.page.get_by_text("新建公海客户")).to_be_visible()

    def create_public_customer(self, customer_name: str, contact_name: str, phone: str = "13000000000") -> None:
        self.open_create_dialog()
        self.page.get_by_placeholder("请输入客户公司全称").fill(customer_name)
        self.page.get_by_placeholder("联系人姓名").fill(contact_name)
        self.page.get_by_placeholder("电话号码").fill(phone)
        self.page.get_by_role("button", name="创建").click()

    def assert_required_fields(self) -> None:
        self.open_create_dialog()
        self.page.get_by_role("button", name="创建").click()
        expect(self.page.get_by_text("客户名称")).to_be_visible()
        expect(self.page.get_by_text("联系人")).to_be_visible()

    def claim_customer(self, customer_name: str) -> None:
        row = self.page.locator("tr", has_text=customer_name).first
        expect(row).to_be_visible()
        row.get_by_role("button", name="领取").click()


class CustomerManagementPage:
    def __init__(self, page: Page):
        self.page = page

    def assert_customer_in_list(self, customer_name: str) -> None:
        expect(self.page.get_by_text(customer_name)).to_be_visible()

    def open_customer_detail(self, customer_name: str) -> None:
        self.page.get_by_role("link", name=customer_name).first.click()
        expect(self.page.get_by_text("客户详情")).to_be_visible()

    def release_to_public_sea(self, customer_name: str) -> None:
        row = self.page.locator("tr", has_text=customer_name).first
        expect(row).to_be_visible()
        row.get_by_role("button", name="释放").click()

    def follow_customer(self, customer_name: str) -> None:
        row = self.page.locator("tr", has_text=customer_name).first
        expect(row).to_be_visible()
        row.get_by_role("button", name="关注").click()


class CustomerDetailPage:
    def __init__(self, page: Page):
        self.page = page

    def add_contact(self, contact_name: str, phone: str = "13100000000") -> None:
        self.page.get_by_role("button", name="新增联系人").click()
        self.page.get_by_placeholder("联系人姓名").fill(contact_name)
        self.page.get_by_placeholder("电话号码").fill(phone)
        self.page.get_by_role("button", name="创建").click()

    def add_followup_record(self, content: str, result: str) -> None:
        self.page.get_by_role("button", name="新增跟进记录").click()
        self.page.get_by_placeholder("详细记录本次跟进的沟通内容").fill(content)
        self.page.get_by_placeholder("简要总结跟进结果").fill(result)
        self.page.get_by_role("button", name="创建").click()

    def add_friend_order(self, summary: str) -> None:
        self.page.get_by_role("button", name="新增友情单").click()
        self.page.get_by_placeholder("请输入").first.fill(summary)
        self.page.get_by_role("button", name="创建").click()

    def add_credit_application(self, amount: str) -> None:
        self.page.get_by_role("button", name="新增申请授信").click()
        self.page.get_by_placeholder("请输入授信金额").fill(amount)
        self.page.get_by_role("button", name="提交").click()


class FollowupPage:
    def __init__(self, page: Page):
        self.page = page

    def create_followup(self, content: str, result: str) -> None:
        self.page.get_by_role("button", name="新增跟进").click()
        self.page.get_by_placeholder("详细记录本次跟进的沟通内容").fill(content)
        self.page.get_by_placeholder("简要总结跟进结果").fill(result)
        self.page.get_by_role("button", name="创建").click()

