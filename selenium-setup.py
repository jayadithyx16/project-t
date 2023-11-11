import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
webdriver_service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get("https://moviesmod.vip/")
fmovie=driver.find_element(By.CSS_SELECTOR,"#post-123004 > header > h2 > a")
print(fmovie.text)
print('doneeee')
time.sleep(4)


