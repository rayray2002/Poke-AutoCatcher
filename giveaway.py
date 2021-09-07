import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


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
text_box = driver.find_element_by_xpath(textbox_xpath)
giveaway = []
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    messages = soup.select('div.message-2qnXI6')
    for m in messages[-5:]:
        if 'given away' in m.text and m['id'] not in giveaway:
            giveaway.append(m['id'])
            print('new giveaway!!')
            print(m['id'])

            retry_count = 0
            count = 0
            while retry_count < 5 and count < 3:
                try:
                    pokeball = driver.find_elements_by_class_name('reactionInner-15NvIl')[-1]
                    if 'pokeball' in pokeball.get_attribute(
                            'aria-label'):
                        time.sleep(0.1)
                        ActionChains(driver).move_to_element(pokeball).click(pokeball).perform()
                        print('clicked')
                        count += 1
                except Exception as e:
                    time.sleep(0.5)
                    retry_count += 1
                    print(f'Retry {retry_count}, {e}')

    print(giveaway)
    for i in giveaway:
        give = soup.find('div', id=i)
        if f'taken in by {name}' in give.text:
            print('win')
            try:
                text_box = driver.find_element_by_xpath(textbox_xpath)
                text_box.send_keys(random.choice(thank_words))
                time.sleep(0.5)
                text_box.send_keys(Keys.ENTER)
                print('=====================')
                print('      Thanked')
                print('=====================')
            except Exception as e:
                print(e)
        elif 'taken in by' in give.text:
            giveaway.remove(i)
            print(f'{i} removed')

    try:
        driver.execute_script("window.scrollTo(0, 1000);")
        text_box.send_keys(Keys.PAGE_DOWN)
    finally:
        time.sleep(0.1)
