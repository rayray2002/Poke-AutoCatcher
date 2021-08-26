from main import *

driver = open_driver()
channel = driver.find_element_by_link_text('正義魔人的頻道')
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

    time.sleep(60)
    count += 1
    print(count)
