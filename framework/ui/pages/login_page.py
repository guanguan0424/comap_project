class LoginPage:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, login_url: str | None = None) -> None:
        target = login_url or self.base_url
        self.page.goto(target)
        # Fallback: if the target page does not render login form,
        # jump to conventional /login route.
        if self.page.locator('input[name="account"]').count() == 0 and self.page.locator('input[name="password"]').count() == 0:
            self.page.goto(f"{self.base_url}/login")

    def login(self, username: str, password: str) -> None:
        # Prefer stable selectors from actual DOM attributes.
        if self.page.locator('input[name="account"]').count() > 0 and self.page.locator('input[name="password"]').count() > 0:
            self.page.locator('input[name="account"]').first.fill(username)
            self.page.locator('input[name="password"]').first.fill(password)
            if self.page.get_by_role("button", name="登 录").count() > 0:
                self.page.get_by_role("button", name="登 录").first.click()
            elif self.page.locator('button[type="submit"]').count() > 0:
                self.page.locator('button[type="submit"]').first.click()
            return

        username_candidates = [
            self.page.get_by_label("Username"),
            self.page.get_by_label("用户名"),
            self.page.get_by_label("账号"),
            self.page.get_by_placeholder("请输入邮箱"),
            self.page.get_by_placeholder("请输入用户名"),
            self.page.get_by_placeholder("请输入账号"),
            self.page.get_by_placeholder("邮箱"),
        ]
        password_candidates = [
            self.page.get_by_label("Password"),
            self.page.get_by_label("密码"),
            self.page.get_by_placeholder("请输入密码"),
            self.page.get_by_placeholder("密码"),
        ]
        login_btn_candidates = [
            self.page.get_by_role("button", name="Login"),
            self.page.get_by_role("button", name="登录"),
            self.page.get_by_role("button", name="登 录"),
            self.page.get_by_text("登录"),
        ]

        username_input = self._first_visible(username_candidates)
        password_input = self._first_visible(password_candidates)

        # If no login form is visible, assume the session is already authenticated.
        if username_input is None or password_input is None:
            return

        username_input.fill(username)
        password_input.fill(password)

        login_btn = self._first_visible(login_btn_candidates)
        if login_btn is not None:
            login_btn.click()

    def _first_visible(self, locators):
        for locator in locators:
            try:
                if locator.first.is_visible(timeout=1500):
                    return locator.first
            except Exception:
                continue
        return None

