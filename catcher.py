#!/usr/bin/python3

from main import *
import datetime

try:
    autoCatcher = AutoCatcher()
    run_minutes = autoCatcher.config['catcher']['run_minutes'].split(',')
    flag = None

    while True:
        if str(datetime.datetime.now().minute) in run_minutes or flag is None:
            autoCatcher.send_message('Start Catching')
            print('Start Catching')
            flag = True
            while flag:
                try:
                    autoCatcher.catcher()
                    flag = False
                except Exception as e:
                    print(e)
            autoCatcher.driver.refresh()
        time.sleep(60)
        print(datetime.datetime.now())

except:
    try:
        autoCatcher.driver.quit()
    except:
        pass
exit()
