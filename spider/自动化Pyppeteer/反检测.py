import asyncio
from pyppeteer_stealth import stealth
from pyppeteer import launch

async def main():
    browser = await launch(headless=False, args=[ #args传递给浏览器的额外参数
        '--disable-infobars',
        '--disable-blink-features=AutomationControlled',  # 禁用自动化控制特征
        '--no-sandbox',  # 禁用沙箱模式
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',  # 解决某些系统上的问题
        '--start-maximized'  # 最大化窗口
    ])
    page = await browser.newPage()
    await stealth(page)  # 加入 stealth 模块，来隐藏特征
    await page.goto('https://hao.360.com/')
    dimensions = await page.evaluate('''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
        }''')
    print(dimensions)
    await page.screenshot({'path': '360.jpg'})
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

