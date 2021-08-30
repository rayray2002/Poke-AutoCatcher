from main import *

try:
    autoCatcher = AutoCatcher()
    autoCatcher.wondertrade()
    autoCatcher.driver.quit()
except Exception as e:
    print(e)
    try:
        autoCatcher.driver.quit()
    except:
        pass
exit()

