# 2025/1/22
#pip install playwright
#playwright install
from playwright.sync_api import sync_playwright

# 调用sync_playwright方法，返回浏览器上下文管理器
with sync_playwright() as p:

    # 创建谷歌浏览器示例，playwright默认启动无头模式，设置headless=False，即关闭无头模式
    browser = p.chromium.launch(headless=False, channel="chrome", timeout=30000)

    # 新建选项卡
    page = browser.new_page()

    # 访问页面
    page.goto("https://baidu.com")

    # 获取页面截图
    page.screenshot(path='example.png')

    # 打印页面的标题，也就是title节点中的文本信息
    print(page.title())

    # 关闭浏览器
    browser.close()