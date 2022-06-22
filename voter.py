from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini', 'utf8')

options = Options()
options.add_argument('log-level=3')
# options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path=config['default']['driver_path'], options=options)
driver.get('https://top.gg/bot/707333868713410682/vote')
driver.maximize_window()


def wait_then_click(mode, text):
    button = None
    if mode == 'link':
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, text)))
        except Exception as e:
            print(e)

        button = driver.find_element_by_link_text(text)
    elif mode == 'xpath':
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, text)))
        except Exception as e:
            print(e)

        button = driver.find_element_by_xpath(text)
    button.click()
    time.sleep(2)


wait_then_click('link', 'Login')

recreate_localStorage_script = '''
        const iframe = document.createElement('iframe');
        document.head.append(iframe);
        const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
        iframe.remove();    
        Object.defineProperty(window, 'localStorage', pd);
        '''
token = open('./token.txt', 'r').read()
driver.execute_script(recreate_localStorage_script)
driver.execute_script(f"window.localStorage.setItem('token', '{token}');")
driver.refresh()
driver.execute_script(recreate_localStorage_script)
print('Token login')

# authorize
wait_then_click('xpath', '//*[@id="app-mount"]/div[2]/div/div/div/div/div[2]/button[2]')

# wait_then_click('link', 'No thanks')
# vote
wait_then_click('xpath', '//*[@id="__next"]/div/div[2]/div/div/div[2]/div/div[1]/main/div[1]/div/div[2]/button')

input()
driver.quit()
