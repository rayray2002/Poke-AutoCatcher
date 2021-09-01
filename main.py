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

    def __init__(self, path='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(path, 'utf8')
        self.textbox_xpath = '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/' \
                             'main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div'

        self.driver = webdriver.Chrome(executable_path=self.config['default']['driver_path'])
        self.driver.get(self.config['default']['server_url'])
        self.driver.maximize_window()

        if int(self.config['default']['auto_login']):
            self.login_by_txt()

        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, self.textbox_xpath)))
        except Exception as e:
            print(e)

        time.sleep(1)
        try:
            close = self.driver.find_element_by_class_name('close-relY5R')
            close.click()
        except Exception as e:
            print('no close button', e)

        time.sleep(1)
        channel = self.driver.find_element_by_link_text(self.config['default']['channel'])
        channel.click()

        self.send_message('Logged in', log=True)

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

    def wait_bot(self, timeout=10):
        t = time.time()
        time.sleep(1)
        author = self.driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
        while 'Poké Catcher' not in author and time.time() - t < timeout:
            author = self.driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
            time.sleep(1)
        return 'Poké Catcher' in author

    def try_function(self, func, timeout, **kwargs):
        func(**kwargs)
        if not self.wait_bot(timeout):
            print('No respond, retrying')
            self.try_function(func, timeout, **kwargs)

    def send_message(self, text, log=False):
        text_box = self.driver.find_element_by_xpath(self.textbox_xpath)
        text_box.send_keys(text)
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)
        if log:
            print(text)

    def bag_check(self, timeout):
        self.try_function(self.send_message, timeout, text='!!bag')
        time.sleep(2)
        bag = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
        ball_order = ['Poke', 'Great', 'Ultra', 'Master']
        for ball in ball_order:
            current = int(re.search(rf'x(\d*) {ball}', bag).group(1))
            ball_amount = int(self.config['catcher'][ball])
            # print(current)
            if current < ball_amount:
                self.try_function(self.send_message, 5, text=f"!!buy {ball} ball {ball_amount}", log=True)
                time.sleep(1)
        self.send_message('Bag checked', log=True)

    def catcher(self):
        self.bag_check(60)
        self.try_function(self.send_message, 60, text='!!pokestop')
        time.sleep(3)

        while True:
            self.try_function(self.send_message, 5, text='!!p')
            print('New pokemon')
            time.sleep(3)

            respond = self.driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
            if 'no rolls left' in respond or 'Bot Traffic' in respond:
                self.send_message('No rolls left', log=True)
                break

            for i in range(3):
                flag = True
                retry_count = 0
                while flag and retry_count < 10:
                    try:
                        pokeball = self.driver.find_elements_by_class_name('reactionInner-15NvIl')[-2]
                        pokeball.click()
                        print('Caught')
                        flag = False
                    except Exception as e:
                        time.sleep(0.5)
                        retry_count += 1
                        print(f'Retry {retry_count}, {e}')
                time.sleep(1)
            time.sleep(3)

    def find_last(self):
        text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text.split('\n')
        last = len(text)
        limit = 25
        while last >= limit:
            time.sleep(1)
            next_page = self.driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]
            time.sleep(1)
            next_page.click()
            time.sleep(1)
            next_page.click()
            time.sleep(1)
            text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text.split('\n')
            last = len(text) + limit
            limit += 25

        while 'in team' in text[last - limit + 24]:
            last -= 1
        return last

    def get_name(self):
        flag = 1
        name = ''
        rarity = ''
        CP = 0
        while flag:
            text = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
            m = re.search(r'(.*) \((.*)\) \(CP: (.*)\)', text)
            try:
                name = m.group(1).strip()
                rarity = m.group(2).strip()
                CP = int(m.group(3).strip())
                flag = 0
            except AttributeError:
                print('retry: get name')
                time.sleep(1)
        return name, rarity, CP

    def wondertrade(self):
        max_level = False
        while True:
            if max_level:
                self.try_function(self.send_message, 3, text='!!wondertrade tradelist')
                time.sleep(1)
                self.send_message('1')
                time.sleep(1)
            else:
                self.try_function(self.send_message, 3, text='!!wondertrade')
                time.sleep(0.5)
                self.send_message('1')
                time.sleep(1)

            name, rarity, CP = self.get_name()
            print(name, rarity, CP)

            dream = self.config['trader']['dream'].split(',')
            if rarity == 'Legendary' or name in dream:
                self.send_message(f'!!info {name}')
                os.system('say "Legendary"')
                if max_level:
                    self.send_message(f'!!fortrade remove')
                    time.sleep(1)
                    self.send_message('1')
                return

            elif (rarity == 'Rare' or CP >= int(self.config['trader']['CP'])) and \
                    int(self.config['trader']['show_info']):
                os.system('say "rare"')
                self.try_function(self.send_message, 5, text=f'!!info {name}')
                info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                evolve_into = re.search(r'Evolves into: (.*)', info).group(1).strip()
                evolve = name
                while evolve_into != 'None':
                    evolve = evolve_into
                    self.try_function(self.send_message, 10, text=f'!!info {evolve_into}')
                    info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                    evolve_into = re.search(r'Evolves into: (.*)', info).group(1)

                self.try_function(self.send_message, 5, text=f'!!info mega {evolve}')
                self.try_function(self.send_message, 5, text=f'!!info {evolve} gmax')

                info = self.driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
                max_cp = re.search(r'Max CP: (.*)', info).group(1)
                if int(max_cp) > 2000:
                    countdown = int(self.config['trader']['countdown'])
                    for i in range(countdown):
                        os.system(f'say "{countdown - i}"')
                        time.sleep(1)

            if not max_level:
                if not max_level and int(self.config['trader']['powerup']):
                    self.try_function(self.send_message, 5, text=f'!!powerup {name} max')
                    time.sleep(1)
                    self.send_message(str(self.find_last()))
                    time.sleep(1)
                    respond = self.driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
                    if 'cannot powerup any' in respond:
                        print('Reach Max Level!')
                        max_level = True

                self.try_function(self.send_message, 2, text=f'!!fortrade add {name}')
                time.sleep(1)
                self.send_message(str(self.find_last()))


if __name__ == '__main__':
    autoCatcher = AutoCatcher()
    autoCatcher.wondertrade()
    autoCatcher.driver.quit()
