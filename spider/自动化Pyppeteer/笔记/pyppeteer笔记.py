#Puppeteer是一个基于 Node.js 的自动化工具
#Pyppeteer 就是 Puppeteer 的 Python 版
#Pyppeteer 是一个使用 Python 语言封装的 Google Chrome 浏览器的非官方 API。
#可以通过 pip 包管理器进行安装。
#除了Pyppeteer 本身外，还需要安装 asyncio 库和一个兼容的 Chrome 浏览器版本。
#bash:
#pip install pyppeteer
#pyppeteer install(用于 pyppeteer 的 chromium，这一步可以省略，因为第一次运行 Pyppeteer 时会自动检测是否安装了 chromium 浏览器，如果没有安装程序会自动进行安装配置。)
#Pyppeteer 基于异步实现，所以它支持异步操作。
"""
安装时报错
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
playwright 1.49.1 requires pyee==12.0.0, but you have pyee 11.1.1 which is incompatible.
"""
"""
保持登陆缓存,使用cookies
browser = await launch(userDataDir='./filedata')
执行 JS 语句
通过调用 Page 对象下的 evaluate 方法可以执行一段 JS 语句。
dimensions = await page.evaluate('''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
        }''')
print(dimensions)
"""
#反检测
#与 Selenium 和 Playwright 有些区别，但是思想是一样的。
#pip install pyppeteer_stealth
# 隐藏特征
#from pyppeteer_stealth import stealth
# await stealth(page)