from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import configparser


class AutoCatcher:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(options=options, executable_path=self.config['default']['driver_path'])
        self.driver.get("https://discord.com/channels/878300201541062656/878302161749033021")
        self.driver.fullscreen_window()

        if int(self.config['default']['auto_login']):
            self.login_by_txt()

        try:
            wait = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')))
        except Exception as e:
            print(e)

        time.sleep(2)
        try:
            close = self.driver.find_element_by_class_name('close-relY5R')
            close.click()
        except Exception as e:
            print('no close button', e)

        time.sleep(2)
        channel = self.driver.find_element_by_link_text(self.config['default']['channel'])
        time.sleep(2)
        channel.click()

        print('logged in')
        text_box = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
        text_box.send_keys('logged in')
        text_box.send_keys(Keys.ENTER)

    def login_by_txt(self):
        email = self.config['default']['email']
        password = self.config['default']['password']

        email_input = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')
        email_input.send_keys(email)
        time.sleep(2)

        password_input = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')
        password_input.send_keys(password)
        time.sleep(2)

        confirm_button = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]')
        confirm_button.click()
        time.sleep(5)

        try:
            wait = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')))
        except Exception as e:
            print(e)

    def wait_bot(self):
        time.sleep(1)
        author = self.driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
        while 'Poké Catcher' not in author:
            author = self.driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
            time.sleep(1)

    def send_message(self, text):
        text_box = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
        text_box.send_keys(text)
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)

    def bag_check(self):
        self.send_message('!!bag')
        self.wait_bot()
        time.sleep(2)
        bag = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
        m = re.findall(r'x(\d*) ', bag)
        if int(m[0]) < int(self.config['catcher']['poke_ball']):
            self.send_message('!!buy poke ball 10')
            print('buy poke ball 10')
            self.wait_bot()

        if int(m[1]) < int(self.config['catcher']['great_ball']):
            self.send_message('!!buy great ball 10')
            print('buy great ball 10')
            self.wait_bot()

        if int(m[2]) < int(self.config['catcher']['ultra_ball']):
            self.send_message('!!buy ultra ball 10')
            print('buy ultra ball 10')
            self.wait_bot()

        if int(m[2]) < int(self.config['catcher']['master_ball']):
            self.send_message('!!buy master ball 1')
            print('buy master ball')
            self.wait_bot()
        print('bag checked')

    def catcher(self):
        self.bag_check()
        self.send_message('!!pokestop')
        time.sleep(2)

        while True:
            self.send_message('!!p')
            self.wait_bot()
            print('new pokemon')
            time.sleep(5)

            flag = True
            count = 0
            while flag and count < 10:
                try:
                    pokeball = self.driver.find_elements_by_class_name('reactionInner-15NvIl')[-2]
                    pokeball.click()
                    print('catched')
                    flag = False
                except Exception as e:
                    time.sleep(1)
                    count += 1
                    print(f'retry {count}, {e}')

            time.sleep(5)
            respond = self.driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
            print(respond)
            if 'no rolls left' in respond or 'Bot Traffic' in respond:
                print('No rolls left')
                break

    def find_last(self):
        text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
        # print(text.split('\n'))
        return len(text.split('\n'))

    def get_name(self):
        try:
            text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
            m = re.search(r'(.*) \((.*)\) \(CP: (.*)\)', text)
        except:
            time.sleep(1)
            text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
            m = re.search(r'(.*) \((.*)\) \(CP: (.*)\)', text)
        name = m.group(1).strip()
        rarity = m.group(2).strip()
        CP = int(m.group(3).strip())
        return name, rarity, CP

    def wondertrade(self):
        max_level = False
        while True:
            self.send_message('!!wondertrade')
            self.wait_bot()
            self.send_message('1')
            time.sleep(1)
            name, rarity, CP = self.get_name()
            print(name, rarity, CP)

            dream = self.config['trader']['dream'].split(',')
            if rarity == 'Legendary' or name in dream:
                self.send_message(f'!!info {name}')
                os.system('say "Legendary"')

                return
            elif rarity == 'Rare' or CP >= int(self.config['trader']['CP']):
                os.system('say "rare"')
                self.send_message(f'!!info {name}')
                self.wait_bot()
                info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                evolve = re.search(r'Evolves into: (.*)', info).group(1)
                while evolve != 'None':
                    self.send_message(f'!!info {evolve}')
                    self.wait_bot()
                    info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                    evolve = re.search(r'Evolves into: (.*)', info).group(1)
                self.send_message(f'!!info mega {evolve}')
                self.wait_bot()
                self.send_message(f'!!info {evolve} gmax')
                self.wait_bot()
                info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                max_cp = re.search(r'Max CP: (.*)', info).group(1)
                if int(max_cp) > 2000:
                    for i in range(10):
                        os.system(f'say "{10 - i}"')
                        time.sleep(1)

            while True and not max_level:
                self.send_message(f'!!powerup {name}')
                self.wait_bot()
                last = self.find_last()
                while last >= 25:
                    next = self.driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]
                    time.sleep(3)
                    next.click()
                    time.sleep(2)
                    last = self.find_last()

                self.send_message(str(last))
                time.sleep(1)
                respond = self.driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
                if 'you do not have enough candy' in respond:
                    break
                elif 'cannot powerup any' in respond:
                    max_level = True
                    break

            self.send_message(f'!!fortrade add {name}')
            time.sleep(1)
            self.wait_bot()
            self.send_message(str(self.find_last()))


if __name__ == '__main__':
    autoCatcher = AutoCatcher()
    autoCatcher.wondertrade()
    autoCatcher.driver.quit()
