from main import *

try:
    autoCatcher = AutoCatcher()
    autoCatcher.wondertrade()
    autoCatcher.driver.quit()
except:
    try:
        autoCatcher.driver.quit()
    except:
        pass
exit()

