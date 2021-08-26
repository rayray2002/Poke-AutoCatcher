from main import *

autoCatcher = AutoCatcher()

count = 0
while True:
    if count % 30 == 0:
        flag = True
        while flag:
            try:
                autoCatcher.catcher()
                flag = False
            except Exception as e:
                print(e)
        autoCatcher.driver.refresh()
    elif count % 5 == 0:
        autoCatcher.send_message(str(count % 30))

    time.sleep(60)
    count += 1
    print(count)
