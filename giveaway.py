import random

from main import *

thank_words = ['Ty', 'tysm', 'tyy', 'Tyy']

print('Input display name:')
name = input()

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://discord.com/channels/723691206332252240/821900041924902912')
driver.maximize_window()

textbox_xpath = '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div[1]/' \
                'div/div/div[1]/div/div[1]/div[2]'

try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, textbox_xpath)))
except Exception as e:
    print(e)

print('logged in')
time.sleep(3)
claimed = None
while True:
    text_raw = driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1]
    text = text_raw.text

    if claimed is None:
        claimed = text_raw

    if 'given away' in text:
        print('new giveaway!!')
        time.sleep(1)
        pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]

        flag = True
        retry_count = 0
        while flag and retry_count < 5:
            try:
                pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]
                if pokeball.get_attribute('aria-pressed') != 'true':
                    pokeball.click()
                    print('clicked')
                    flag = False
            except Exception as e:
                time.sleep(0.5)
                retry_count += 1
                print(f'Retry {retry_count}, {e}')

    if f'taken in by {name}' in text and claimed != text_raw:
        print('win')
        flag = True
        retry_count = 0
        while flag and retry_count < 5:
            try:
                text_box = driver.find_element_by_xpath(textbox_xpath)
                text_box.send_keys(random.choice(thank_words))
                time.sleep(0.5)
                text_box.send_keys(Keys.ENTER)
                print('=====================')
                print('      Thanked')
                print('=====================')
                flag = False
            except Exception as e:
                print('retry', e)
                retry_count += 1
                break
        driver.refresh()
        claimed = text_raw
    time.sleep(30)
