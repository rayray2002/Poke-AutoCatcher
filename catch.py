#!/sbin/python

from driver import *
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini', 'utf8')

with open('token.txt', 'r') as users:
    users = users.read().splitlines()

for user in users:
    name, token = user.split(':')

    try:
        catcher = AutoCatcher(config, config['default']['server_url'], token)

        present = datetime.now()
        catcher.send_message(f'{name} starts catching at {present.strftime("%H:%M:%S")}', True)

        flag = True
        count = 0
        while flag and count <= 10:
            try:
                catcher.catcher()
                flag = False
            except Exception as e:
                print(f"Error when catching. Retry {count}: {e}")
                count += 1

    except Exception as e:
        print(f"Error on {name}: {e}")
        continue

    catcher.quit()

print('Exit')
