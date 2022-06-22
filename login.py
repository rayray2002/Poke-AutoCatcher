from selenium import webdriver
from selenium.webdriver.chrome.options import Options

token = '"NTQwMTQ5MTE2Mzc0NjE0MDE2.YKsVYQ.mklxABDSVXbHEI1taXmWhYrYgnQ"'
recreate_localStorage_script = '''
    const iframe = document.createElement('iframe');
    document.head.append(iframe);
    const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
    iframe.remove();    
    Object.defineProperty(window, 'localStorage', pd);
    '''

options = Options()
# options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.get('https://discord.com/login')

try:
    driver.execute_script(recreate_localStorage_script)
    driver.execute_script(f"window.localStorage.setItem('token', '{token}');")
    driver.refresh()

    driver.execute_script(recreate_localStorage_script)
    print('get token:', driver.execute_script(f"return window.localStorage.getItem('token');"))
except Exception as ex:
    print('[Exception]', ex)

input()
driver.quit()
