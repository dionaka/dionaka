from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#不自动关闭浏览器
option=webdriver.ChromeOptions()
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
option.add_experimental_option("detach",True)
driver=webdriver.Chrome(options=option)
driver.get('https://show.bilibili.com/platform/home.html')
driver.maximize_window()
textLabel=driver.find_element(By.XPATH,"//*[@class='nav-header-search-bar unlogin']")
print(textLabel.get_attribute('placeholder'))
textLabel.send_keys("崩铁")
button=driver.find_element(By.XPATH,"//*[@class='search-link']")
#ActionChains(driver).double_click(button).perform()
button.click()
#选择展会

buttonTOShow=driver.find_element(By.XPATH,"(//*[@class='project-list-item'])[1]")
buttonTOShow.click()
buy=driver.find_element(By.XPATH,"//*[@class='product-buy enable']")
buy.click()
 
