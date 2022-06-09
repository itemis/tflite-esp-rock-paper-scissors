import os
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import Select


folder_name=Path("data/esp-eye-paper")
IP = "http://192.168.178.143"

#os.environ['PATH'] += r"C:/Webdriver"
folder_name.mkdir(exist_ok=True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
#driver = webdriver.Firefox()
driver.get(IP)
driver.implicitly_wait(10)
start_stream = driver.find_element_by_id('toggle-stream')
start_stream.click()
time.sleep(1)
select = Select(driver.find_element_by_id('framesize'))
select.select_by_value('0')
select = Select(driver.find_element_by_id('special_effect'))
select.select_by_value('2')
#driver.execute_script("""
#   var l = document.getElementsByClassName("button save")[0];
#   l.parentNode.removeChild(l);
#""")
counter = 0
while(counter < 1000):
    time.sleep(0.0333)
    with open(f'paper/out{counter}.png', 'wb') as file:
        stream = driver.find_element_by_id('stream')
        file.write(stream.screenshot_as_png)
        counter += 1
driver.quit()