import random

from main import *

thank_words = ['Ty', 'tysm', 'tyy', 'Tyy']
url = 'https://discord.com/channels/723691206332252240/821900041924902912'

print('Input display name:')
name = input()

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.get(url)
driver.maximize_window()

textbox_xpath = '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div[1]/' \
                'div/div/div[1]/div/div[1]/div[2]'
recreate_localStorage_script = '''
        const iframe = document.createElement('iframe');
        document.head.append(iframe);
        const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
        iframe.remove();    
        Object.defineProperty(window, 'localStorage', pd);
        '''

if os.path.exists('./token.txt'):
    token = open('./token.txt', 'r').read()
    driver.execute_script(recreate_localStorage_script)
    driver.execute_script(f"window.localStorage.setItem('token', '{token}');")
    driver.refresh()
    driver.execute_script(recreate_localStorage_script)
    print('Token login')
else:
    img_xpath = '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[3]/div/div/div/div[1]/div[1]/img'
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, img_xpath)))
    except Exception as e:
        print(e)

    driver.save_screenshot('login.png')
    print('QRcode got')

try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, textbox_xpath)))
except Exception as e:
    print(e)

print('logged in')
time.sleep(3)
claimed = None
text_box = driver.find_element_by_xpath(textbox_xpath)
while True:
    try:
        text_raw = driver.find_elements_by_class_name('embedDescription-1Cuq9a')[-1]
        text = text_raw.text
        driver.execute_script("window.scrollTo(0, 1000);")
        text_box.send_keys(Keys.PAGE_DOWN)
    except:
        continue

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
                if pokeball.get_attribute('aria-pressed') != 'true' and 'pokeball' in pokeball.get_attribute(
                        'aria-label'):
                    pokeball.click()
                    print('clicked')
                    flag = False
            except Exception as e:
                time.sleep(0.5)
                retry_count += 1
                print(f'Retry {retry_count}, {e}')

    if f'taken in by {name}' in text and claimed != text_raw:
        print('win')
        try:
            text_box = driver.find_element_by_xpath(textbox_xpath)
            text_box.send_keys(random.choice(thank_words))
            time.sleep(0.5)
            text_box.send_keys(Keys.ENTER)
            print('=====================')
            print('      Thanked')
            print('=====================')
            claimed = text_raw
        except Exception as e:
            print(e)
    time.sleep(0.1)
