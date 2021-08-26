import time

from main import *

driver = open_driver()
time.sleep(1)
channel = driver.find_element_by_link_text('正義魔人的頻道')
time.sleep(1)
channel.click()

count = 0
while True:
    if count % 30 == 0:
        flag = True
        while flag:
            try:
                catcher(driver)
                flag = False
            except Exception as e:
                print(e)
    driver.refresh()
    time.sleep(60)
    count += 1
    print(count)
