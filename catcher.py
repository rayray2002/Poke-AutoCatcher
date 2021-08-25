from main import *

driver = open_driver()

count = 0
while True:
    if count % 20 == 0:
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
