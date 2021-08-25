from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os


def open_driver(auto=False):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    try:
        driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
        driver.get("https://discord.com/channels/878300201541062656/878302161749033021")
    except:
        driver = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')
        driver.get('https://discord.com/channels/878300201541062656/879602635194384424')

    if auto:
        login_by_txt(driver)

    try:
        wait = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')))
    except Exception as e:
        print(e)

    print('logged in')
    text_box = driver.find_element_by_xpath(
        '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
    text_box.send_keys('logged in')
    text_box.send_keys(Keys.ENTER)
    return driver


def login_by_txt(driver, path='./credentials.txt'):
    credentials = open(path, 'r').readline()
    email = credentials[0]
    password = credentials[1]

    email_input = driver.find_element_by_xpath(
        '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input')
    email_input.send_keys(email)
    time.sleep(2)

    password_input = driver.find_element_by_xpath(
        '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input')
    password_input.send_keys(password)
    time.sleep(2)

    confirm_button = driver.find_element_by_xpath(
        '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]')
    confirm_button.click()
    time.sleep(5)

    try:
        wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')))
    except Exception as e:
        print(e)


def send_message(driver, text):
    text_box = driver.find_element_by_xpath(
        '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
    text_box.send_keys(text)
    time.sleep(0.5)
    text_box.send_keys(Keys.ENTER)


def bag_check(driver):
    send_message(driver, '!!bag')
    wait_bot(driver)
    time.sleep(2)
    bag = driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
    m = re.findall(r'x(\d*) ', bag)
    if int(m[0]) < 10:
        send_message(driver, '!!buy poke ball 10')
        print('buy poke ball 10')
        wait_bot(driver)

    if int(m[1]) < 10:
        send_message(driver, '!!buy great ball 10')
        print('buy great ball 10')
        wait_bot(driver)

    if int(m[2]) < 10:
        send_message(driver, '!!buy ultra ball 10')
        print('buy ultra ball 10')
        wait_bot(driver)

    if int(m[2]) < 1:
        send_message(driver, '!!buy master ball 1')
        print('buy master ball')
        wait_bot(driver)
    print('bag checked')


def catcher(driver):
    bag_check(driver)
    send_message(driver, '!!pokestop')
    time.sleep(2)

    while True:
        send_message(driver, '!!p')
        wait_bot(driver)
        print('new pokemon')
        time.sleep(5)

        flag = True
        count = 0
        while flag and count < 10:
            try:
                pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-2]
                pokeball.click()
                print('catched')
                flag = False
            except:
                time.sleep(1)
                count += 1
                print(f'retry {count}')

        time.sleep(5)
        respond = driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
        if 'no rolls left' in respond:
            print('no rolls left')
            break


def find_last(driver):
    text = driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
    # print(text.split('\n'))
    return len(text.split('\n'))


def get_name(driver):
    text = driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1].text
    m = re.search(r'(.*) \((.*)\) \(CP: (.*)\)', text)
    name = m.group(1).strip()
    rarity = m.group(2).strip()
    CP = int(m.group(3).strip())
    return name, rarity, CP


def wait_bot(driver):
    time.sleep(1)
    author = driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
    while 'Poké Catcher' not in author:
        author = driver.find_elements_by_class_name('headerText-3Uvj1Y')[-1].text
        time.sleep(1)


def wondertrade(driver):
    max_level = False
    while True:
        send_message(driver, '!!wondertrade')
        wait_bot(driver)
        send_message(driver, '1')
        time.sleep(1)
        name, rarity, CP = get_name(driver)
        print(name, rarity, CP)

        if rarity == 'Legendary':
            send_message(driver, f'!!info {name}')
            os.system('say "catched Legendary"')

            return
        elif rarity == 'Rare' or CP >= 1500:
            os.system('say "catched rare"')
            send_message(driver, f'!!info {name}')
            time.sleep(10)

        while True and not max_level:
            send_message(driver, f'!!powerup {name}')
            wait_bot(driver)
            last = find_last(driver)
            while last >= 25:
                next = driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]
                time.sleep(3)
                next.click()
                time.sleep(2)
                last = find_last(driver)

            send_message(driver, str(last))
            wait_bot(driver)
            respond = driver.find_elements_by_class_name('contents-2mQqc9')[-1].text
            if 'you do not have enough candy' in respond:
                break
            elif 'cannot powerup any' in respond:
                max_level = True
                break

        send_message(driver, f'!!fortrade add {name}')
        time.sleep(1)
        wait_bot(driver)
        send_message(driver, str(find_last(driver)))


if __name__ == '__main__':
    driver = open_driver()

    wondertrade(driver)
    driver.quit()
