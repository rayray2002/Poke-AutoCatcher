from main import *
import datetime

autoCatcher = AutoCatcher()

run_minutes = autoCatcher.config['catcher']['run_minutes'].split(',')
while True:
    if str(datetime.datetime.now().minute) in run_minutes:
        autoCatcher.send_message('run')
        flag = True
        while flag:
            try:
                autoCatcher.catcher()
                flag = False
            except Exception as e:
                print(e)
        autoCatcher.driver.refresh()
    time.sleep(10)
    print(datetime.datetime.now().minute)
