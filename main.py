from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def open_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
    driver.get("https://discord.com/channels/878300201541062656/878302161749033021")

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


def catcher(driver, count):
    send_message(driver, '!!pokestop')
    time.sleep(2)

    for i in range(count):
        send_message(driver, '!!p')
        time.sleep(3)

        pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-2]
        t = time.time()
        while pokeball.get_attribute("aria-pressed") == 'true' and time.time() - t < 10:
            pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-2]
        time.sleep(3)

        pokeball.click()
        time.sleep(3)


if __name__ == '__main__':
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
