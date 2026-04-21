# Pytest测试框架

一个完整的UI业务测试和接口测试框架，基于pytest构建，支持现代Web应用测试。

## 🚀 功能特性

### 核心功能
- **完整的测试框架**：API测试 + UI测试一体化
- **多环境支持**：开发、测试、生产环境配置
- **并行执行**：pytest-xdist并行测试加速
- **智能重试**：失败用例自动重试机制
- **详细报告**：HTML/Allure测试报告生成

### API测试支持
- RESTful API测试封装
- 认证支持（Bearer Token、Cookie）
- 数据模型验证（基于Pydantic）
- 丰富的断言库
- 错误响应处理

### UI测试支持
- Playwright浏览器自动化
- React/Vue现代化定位策略
- 页面对象模型（POM）设计
- 响应式设计测试
- 视觉测试支持

## 📦 快速开始

### 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 配置环境
复制并配置环境文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```bash
# API测试地址
API_BASE_URL=http://your-api-server.com

# UI测试地址  
UI_BASE_URL=http://192.168.10.110:3000

# 测试账号
TEST_USERNAME=lp@savehmi.com
TEST_PASSWORD=123456

# 启用真实环境测试
RUN_LIVE_TESTS=1
```

### 运行测试

使用便捷脚本：
```bash
# 运行所有测试
python run_tests.py --all

# 只运行API测试
python run_tests.py --api

# 只运行UI测试
python run_tests.py --ui

# 运行冒烟测试
python run_tests.py --smoke

# 运行回归测试并生成覆盖率报告
python run_tests.py --regression --coverage
```

或直接使用pytest：
```bash
# 运行所有测试
pytest

# 运行API测试
pytest -m api

# 运行UI测试
pytest -m ui

# 运行特定标记的测试
pytest -m "api and smoke"

# 生成HTML报告
pytest --html=reports/report.html
```

## 📁 项目结构

```
comap_project/
├── config/                 # 配置文件
│   ├── dev.yaml           # 开发环境配置
│   ├── test.yaml          # 测试环境配置
│   ├── prod.yaml          # 生产环境配置
│   └── test_data.yaml     # 测试数据配置
├── framework/             # 测试框架核心
│   ├── api/               # API测试框架
│   │   ├── client.py      # API客户端
│   │   ├── assertions.py  # 断言工具
│   │   └── models.py      # 数据模型
│   ├── ui/                # UI测试框架
│   │   ├── base_page.py   # 页面基类
│   │   ├── locators.py    # 元素定位器
│   │   └── pages/         # 页面对象模型
│   ├── config/            # 配置管理
│   │   └── settings.py    # 设置管理
│   └── utils/             # 工具模块
├── tests/                 # 测试用例
│   ├── api/               # API测试用例
│   │   ├── test_health.py
│   │   ├── test_login_api.py
│   │   └── test_user_management.py
│   └── ui/                # UI测试用例
│       ├── test_login_workflow.py
│       └── test_crm_modules.py
├── reports/               # 测试报告（自动生成）
├── screenshots/           # 失败截图（自动生成）
├── run_tests.py           # 测试执行脚本
├── pytest.ini            # pytest配置
├── requirements.txt       # 依赖包
└── README.md             # 项目说明
```

## 🏷️ 测试标记系统

框架支持丰富的测试标记，便于分类执行：

```python
@pytest.mark.api           # API测试
@pytest.mark.ui            # UI测试
@pytest.mark.smoke         # 冒烟测试
@pytest.mark.regression    # 回归测试
@pytest.mark.integration   # 集成测试
@pytest.mark.performance   # 性能测试
@pytest.mark.security      # 安全测试
@pytest.mark.login         # 登录测试
@pytest.mark.navigation    # 导航测试
```

## 🛠️ API测试示例

```python
import pytest
from framework.api.assertions import assert_status, assert_json_has_keys

@pytest.mark.api
def test_user_login(api_client):
    """测试用户登录"""
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("请设置RUN_LIVE_TESTS=1以运行真实环境测试")
    
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    resp = api_client.post("/api/auth/login", json=login_data)
    
    assert_status(resp, 200)
    assert_json_has_keys(resp, "access_token", "token_type")
```

## 🎨 UI测试示例

```python
import pytest

@pytest.mark.ui
def test_login_workflow(page, ui_base_url):
    """测试登录流程"""
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("请设置RUN_LIVE_TESTS=1以运行真实环境测试")
    
    page.goto(f"{ui_base_url}/login")
    
    # 填写表单
    page.locator('input[name="username"]').fill("testuser")
    page.locator('input[name="password"]').fill("password123")
    page.locator('button[type="submit"]').click()
    
    # 验证登录成功
    page.wait_for_url(f"{ui_base_url}/dashboard")
    assert page.locator(".user-menu").is_visible()
```

## ⚙️ 高级功能

### 并行测试
```bash
# 自动检测CPU核心数并行执行
pytest -n auto

# 指定并行进程数
pytest -n 4
```

### 失败重试
```bash
# 失败用例重试1次，间隔2秒
pytest --reruns 1 --reruns-delay 2
```

### 测试覆盖率
```bash
# 生成覆盖率报告
pytest --cov=framework --cov-report=html:reports/coverage
```

### 浏览器调试模式
```bash
# 显示浏览器界面（非headless模式）
pytest -m ui --headed

# 减慢操作速度便于观察
pytest -m ui --slowmo 1000
```

## 🧪 CRM测试覆盖点

### UI测试覆盖
- **公海客户**：新建校验（客户名称、联系人必填）
- **公海客户**：创建后可领取，领取后出现在客户管理
- **客户管理**：关注客户、释放到公海
- **客户详情**：新增联系人、新增跟进记录、新增友情单、新增申请授信
- **跟进记录模块**：新增跟进记录

### API测试覆盖
- **用户管理**：注册、登录、个人信息管理
- **权限控制**：管理员权限、用户权限验证
- **业务逻辑**：核心业务API接口测试
- **错误处理**：异常场景和边界条件测试

## 🔧 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 更新pip
   pip install --upgrade pip
   
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **浏览器连接失败**
   ```bash
   # 手动安装浏览器
   playwright install chromium
   playwright install firefox
   playwright install webkit
   ```

3. **测试环境连接失败**
   - 检查对应环境变量配置
   - 确认网络连接正常
   - 设置超时时间：`API_TIMEOUT=60`

## 📋 环境变量参考

完整的环境变量配置参考 `.env.example` 文件，主要配置项：

```bash
# 必需配置
TEST_ENV=test
RUN_LIVE_TESTS=1
TEST_USERNAME=lp@savehmi.com
TEST_PASSWORD=123456
API_BASE_URL=http://localhost:8000
UI_BASE_URL=http://192.168.10.110:3000

# 可选配置
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=admin123
API_TIMEOUT=30
BROWSER=chromium
HEADLESS=true
```

这个测试框架现已完整配置，支持您进行全面的系统UI业务测试和接口测试。
根据您提供的具体测试地址配置环境变量后即可开始测试工作。


