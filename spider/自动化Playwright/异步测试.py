#2025.1.22
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome", timeout=30000)
        page = await browser.new_page()
        await page.goto("https://baidu.com")
        await page.screenshot(path="example.png")
        print(await page.title())
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())