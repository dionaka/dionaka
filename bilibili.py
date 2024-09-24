from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options)
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




