from time import sleep
from selenium import webdriver
import os
import pprint
import json
from selenium.webdriver.common.by import By
option=webdriver.ChromeOptions()
prefs={

}
option.add_experimental_option("prefs",prefs)
option.add_argument("--window-size=1024,1024")
#option.add_argument("--headless")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
driver=webdriver.Chrome(option)
driver.get("https://www.baidu.com")
sleep(3)
driver.maximize_window()
login=driver.find_element(By.XPATH,"//a[@id='s-top-loginbtn']")
login.click()
sleep(15)
cookie=driver.get_cookies()
with open("cookie.json","w",encoding="utf-8") as f:
    json.dump(cookie,f)
driver.refresh()
sleep(5)
#delete_all_cookies 是已经获取cookie，模拟调试窗口第一次打开
#如果已经在调试窗口扫码登陆，不用重新获取，refresh或者get方法网页仍有cookies
driver.delete_all_cookies()
""""
with open("cookie.json","r",encoding="utf-8") as f:
    recookies=json.load(f)
    for recookie in recookies:
        cookie_dict={
                'domain': '.baidu.com',
                'name': recookie.get('name'),
                'value': recookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
        }
        driver.add_cookie(cookie_dict)
"""        
#print(recookie)观察得到此时recookie实际上是[{}，{}，{}]列表套许多字典
driver.get("https://baidu.com")
sleep(20)
driver.refresh()
sleep(500)
