from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()#最高权限运行
#options.add_argument('--headless')#无头模式
options.add_argument("--no--sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")# navigator.webdriver 设置为 false
options.add_experimental_option("excludeSwitches",["enable-automation"])##隐藏"Chrome正在受到自动软件的控制"提示
options.add_experimental_option('useAutomationExtension',False)##禁用了 Chrome 的自动化扩展

driver = webdriver.Chrome(options)
#生成 stealth.min.js文件：npx extract-stealth-evasions
with open("stealth.min.js","r") as f:
    js=f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{"source":js})
driver.get("https://www.bilibili.com/opus/950342787927113728")
driver.maximize_window()
sleep(20)
resource=driver.find_elements(By.XPATH,"//div[@class='opus-module-content']/ul/li/a")
for i in resource:
    driver.switch_to.window(driver.window_handles[0])
    print(i.text)
    i.click()
    sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(3)
    try:
        buttons=driver.find_elements(By.XPATH,"//span[contains(text(),'互动抽奖')] | //a[contains(text(),'互动抽奖')]")
        for button1 in buttons:
            try:
                button1.click()
                break
            except:
                print("切换通道二")
        sleep(2)
        try:
            driver.switch_to.window(driver.window_handles[-1])
            iframe_label=driver.find_element(By.XPATH,"//iframe[@class='bili-popup__content__browser']")
            driver.switch_to.frame(iframe_label)
            sleep(4)
            button=driver.find_element(By.CLASS_NAME,"join-button")
            button.click()
            sleep(2)
            driver.switch_to.default_content()
        except:
            print("抽奖已结束或已预约")
            driver.close()
            continue
    except:
        print("未发现，可能为动态加载")
        driver.close()
        continue
    driver.close()
    print("完成")
    sleep(2)




