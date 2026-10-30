
# 电商平台 Web UI 自动化测试框架

## 📖 项目简介
本项目基于 **Python + Selenium + Pytest**，采用 **POM (Page Object Model)** 设计模式，针对 SauceDemo 电商平台实现了端到端（E2E）的全链路自动化测试。

## 🛠️ 技术栈
- **语言**：Python 3.12
- **UI 测试工具**：Selenium WebDriver
- **测试框架**：Pytest
- **报告**：pytest-html

## 🎯 核心覆盖场景 (10条用例全通过)
1. **登录鉴权**：正常登录、密码错误、账号锁定、空字段拦截（参数化驱动）。
2. **商品操作**：多维度价格排序验证、多商品动态加购、移除与角标联动。
3. **订单结算与财务**：必填项校验、取消结算流转、**订单金额精准校验（总价=小计+税费）**。
4. **端到端 (E2E)**：完整模拟用户从登录到最终支付成功的全链路闭环。

## 📁 目录结构
```text
├── pages/          # POM 页面对象层（封装页面元素与动作）
├── tests/          # 测试用例层
├── pytest.ini      # pytest 配置文件
├── report.html     # 测试报告
└── README.md

## 🚀 快速开始
1. 安装依赖：`pip install selenium pytest pytest-html`
2. 运行测试：`python -m pytest tests/ --html=report.html --self-contained-html`

<img width="861" height="944" alt="Snipaste_2026-10-30_18-11-28" src="https://github.com/user-attachments/assets/0429c0bc-83d7-4571-a4ae-4aa5d84e75ac" />
<img width="858" height="264" alt="Snipaste_2026-10-30_18-12-18" src="https://github.com/user-attachments/assets/4b3afc92-36ff-4c23-891d-0a05aebae765" />
