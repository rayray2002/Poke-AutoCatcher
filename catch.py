from driver import *
from pyvirtualdisplay import Display
from datetime import datetime

display = Display(visible=False, size=(1920, 1080))
display.start()

config = configparser.ConfigParser()
config.read('config.ini', 'utf8')

with open('token.txt', 'r') as users:
    users = users.read().splitlines()

for user in users:
    name, token = user.split(':')
    present = datetime.now()
    catcher = AutoCatcher(config, config['default']['server_url'], token)
    catcher.send_message(f'{name} starts catching at {present.strftime("%H:%M:%S")}', True)

    flag = True
    while flag:
        try:
            catcher.catcher()
            flag = False
        except Exception as e:
            print(e)
    catcher.quit()

display.stop()
