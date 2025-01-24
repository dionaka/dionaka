from selenium import webdriver
from time import time
from selenium.webdriver.common.by import By
options=webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')
options.add_argument("--headless")
driver=webdriver.Chrome(options=options)
driver.get("https://sso.scnu.edu.cn/AccountService/user/index.html?sysname=%E7%BB%BC%E5%90%88%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0")
driver.implicitly_wait(5)
start=time()
try:
    driver.find_element(By.ID,'v')
except Exception as e:
    print(e)
    print(f'耗时:{time()-start}')