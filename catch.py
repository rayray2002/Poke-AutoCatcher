from driver import *
from pyvirtualdisplay import Display

display = Display(visible=False, size=(1920, 1080))
display.start()

config = configparser.ConfigParser()
config.read('config.ini', 'utf8')

with open('token.txt', 'r') as tokens:
    tokens = tokens.read().splitlines()

for token in tokens:
    catcher = AutoCatcher(config, config['default']['server_url'], token)
    catcher.send_message('Start Catching', True)

    flag = True
    while flag:
        try:
            catcher.catcher()
            flag = False
        except Exception as e:
            print(e)
    catcher.quit()

display.stop()
