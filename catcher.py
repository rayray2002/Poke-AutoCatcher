from main import *

driver = open_driver()

count = 0
while True:
    if count % 60 == 0:
        try:
            catcher(driver, 15)
        except Exception as e:
            print(e)
    time.sleep(60)
    count += 1
    print(count)
