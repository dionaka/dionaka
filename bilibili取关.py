from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Chrome()
driver.get("https://space.bilibili.com/2053691795/dynamic")
sleep(2)
login=driver.find_element(By.XPATH,"//span[contains(text(),'登录')]")
login.click()
sleep(12)#扫码
n=11
js_script=f"document.getElementsByClassName('bili-dyn-item__main')[{n}].scrollIntoView();"
driver.execute_script(js_script)
elements=driver.find_elements(By.XPATH,"//span[contains(text(),'互动抽奖')]")
for i in elements:
    i.click()
    sleep(3)
    iframe1=driver.find_element(By.XPATH,"//iframe[@class='bili-popup__content__browser']")
    driver.switch_to.frame(iframe1)
    element=driver.find_element(By.XPATH, "//div[@class='join-button join-button--disable']")
    if "已成功参与" in element.text:
        print("已成功参与")
    else:
        print("已开奖")
        driver.switch_to.default_content()
        sleep(2)
        unlock=driver.find_element(By.CLASS_NAME,"bili-dyn-more__menu")
        ActionChains(driver).move_to_element(unlock).perform()
        sleep(2)
        delete1=driver.find_element(By.XPATH,"//div[contains(text(),'删除')]")
        delete1.click()
        sleep(1)
        delete2=driver.find_element(By.XPATH,"//button[contains(text(),'删除')]")
        delete2.click()
        continue
    driver.switch_to.default_content()
    closeButton=driver.find_element(By.XPATH, "//div[@class='bili-popup__header__close']")
    closeButton.click()
    sleep(3)

