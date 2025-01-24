import asyncio

#import pyppeteer
#from pathlib import Path
#from pyppeteer import __chromium_revision__, __pyppeteer_home__

from pyppeteer import launch

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://www.baidu.com')
    await page.screenshot({'path': 'baidu.png'})
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

#print(pyppeteer.__file__)
#print(Path(__pyppeteer_home__))