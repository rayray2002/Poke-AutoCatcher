from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import os
import configparser


class AutoCatcher:
    def __init__(self, path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(path, "utf8")
        # self.textbox_xpath = '//*[@id="app-mount"]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[1]/div/div[3]/div/div[2]'
        self.textbox_xpath = "//div[@role='textbox']"
        self.recreate_localStorage_script = """
        const iframe = document.createElement('iframe');
        document.head.append(iframe);
        const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, 'localStorage');
        iframe.remove();    
        Object.defineProperty(window, 'localStorage', pd);
        """

        options = Options()
        options.add_argument("log-level=3")
        if int(self.config["default"]["headless"]):
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(
            executable_path=self.config["default"]["driver_path"], options=options
        )
        self.driver.get(self.config["default"]["server_url"])
        self.driver.maximize_window()

        if os.path.exists("./token.txt"):
            token = open("./token.txt", "r").read()
            self.driver.execute_script(self.recreate_localStorage_script)
            self.driver.execute_script(
                f"window.localStorage.setItem('token', '{token}');"
            )
            self.driver.refresh()
            self.driver.execute_script(self.recreate_localStorage_script)
            print("Token login")
        elif int(self.config["default"]["auto_login"]):
            self.login_by_txt()
            print("Auto login")
        else:
            img_xpath = '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[3]/div/div/div/div[1]/div[1]/img'
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, img_xpath))
                )
            except Exception as e:
                print(e)

            self.driver.save_screenshot("login.png")
            print("QRcode got")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.textbox_xpath))
            )
        except Exception as e:
            print("login failed")
            img_xpath = "//img[@alt='Scan me!']"
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, img_xpath))
                )
            except Exception as e:
                print(e)

            self.driver.save_screenshot("login.png")
            print("QRcode got")

        WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, self.textbox_xpath))
            )
        print("login")

        time.sleep(1)
        try:
            nitro_ad = self.driver.find_element_by_xpath(
                '//*[@id="app-mount"]/div[5]/div[2]/div'
            )
            nitro_ad.send_keys(Keys.ESCAPE)
            time.sleep(1)
        except Exception as e:
            print("no ads")

        try:
            close = self.driver.find_element_by_class_name("close-relY5R")
            close.click()
            time.sleep(1)
        except Exception as e:
            print("no close button")

        time.sleep(1)
        # channel = self.driver.find_element_by_link_text(
        #     self.config["default"]["channel"]
        # )
        # channel.click()

        print("logged in")

    def login_by_txt(self):
        email = self.config["default"]["email"]
        password = self.config["default"]["password"]

        email_input = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input'
        )
        email_input.send_keys(email)
        time.sleep(2)

        password_input = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input'
        )
        password_input.send_keys(password)
        time.sleep(2)

        confirm_button = self.driver.find_element_by_xpath(
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]'
        )
        confirm_button.click()
        time.sleep(5)

    def wait_bot(self, timeout=10):
        t = time.time()
        time.sleep(1)
        author = self.driver.find_elements_by_class_name("headerText-2z4IhQ")[-1].text
        while "Pok?? Catcher" not in author and time.time() - t < timeout:
            author = self.driver.find_elements_by_class_name("headerText-2z4IhQ")[
                -1
            ].text
            time.sleep(1)
        return "Pok?? Catcher" in author

    def try_function(self, func, timeout, **kwargs):
        # print(f"try_function: {str(func)}")
        func(**kwargs)
        if not self.wait_bot(timeout):
            print("No respond, retrying")
            self.try_function(func, timeout, **kwargs)

    def send_message(self, text, log=False):
        text_box = self.driver.find_element_by_xpath(self.textbox_xpath)
        text_box.send_keys(text)
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)
        if log:
            print(text)

    def send_command(self, text, log=False):
        text_box = self.driver.find_element_by_xpath(self.textbox_xpath)
        text_box.send_keys(text)
        time.sleep(1)
        text_box.send_keys(Keys.ENTER)
        # print("enter1")
        time.sleep(1.5)
        text_box.send_keys(Keys.ENTER)
        # print("enter2")
        # print("sent")
        if log:
            print(text)

    def buy_ball(self, item, amount):
        text_box = self.driver.find_element_by_xpath(self.textbox_xpath)
        text_box.send_keys("/buy")
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)

        text_box.send_keys(item)
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)

        text_box.send_keys(str(amount))
        time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)

    def bag_check(self, timeout):
        print("Start bag check")
        self.try_function(self.send_command, timeout, text="/inventory")
        # print("out")
        time.sleep(2)
        # bag = self.driver.find_elements_by_class_name(
        #     "embedDescription-1DrJxZ embedMargin-2PsaQ4"
        # )
        bag = self.driver.find_elements_by_css_selector('.embedDescription-1DrJxZ.embedMargin-2PsaQ4')
        # print("find")
        bag = bag[-1].text
        # print(bag)
        ball_order = ["Poke", "Great", "Ultra", "Master"]
        for ball in ball_order:
            ball_amount = int(self.config["catcher"][ball])
            match = re.search(rf"x(\d*) {ball}", bag)
            try:
                current = int(match.group(1))
            except AttributeError:
                current = 0
            # print(current)
            if current < ball_amount:
                self.buy_ball(f"{ball} Ball", ball_amount - current)
                time.sleep(1)
        self.send_message("Bag checked", log=True)

    def catcher(self):
        self.bag_check(60)
        self.try_function(self.send_command, 60, text="/pokestop")
        time.sleep(3)

        while True:
            self.try_function(self.send_command, 5, text="/pokemon")
            print("New pokemon")
            time.sleep(3)
            
            response = self.driver.find_elements_by_css_selector(".markup-eYLPri.messageContent-2t3eCI")
            response = response[-1].text
            print(response)
            # respond = self.driver.find_elements_by_class_name("markup-eYLPri")[
            #     -1
            # ].text
            if "no rolls left" in response or "Bot Traffic" in response:
                self.send_message("No rolls left", log=True)
                break

            flag = True
            retry_count = 0
            while flag and retry_count < 10:
                try:
                    pokeball = self.driver.find_elements_by_class_name(
                        "component-ifCTxY"
                    )[-2]
                    pokeball.click()
                    print("Caught")
                    flag = False
                except Exception as e:
                    time.sleep(0.5)
                    retry_count += 1
                    print(f"Retry {retry_count}, {e}")

            time.sleep(5)

    def find_last(self):
        text = self.driver.find_elements_by_class_name("embedDescription-1Cuq9a")[
            -1
        ].text.split("\n")
        last = len(text)
        limit = 25
        while last >= limit:
            time.sleep(0.3)
            next_page = self.driver.find_elements_by_class_name("reactionInner-15NvIl")[
                -1
            ]
            time.sleep(0.3)
            next_page.click()
            time.sleep(0.3)
            next_page.click()
            time.sleep(0.3)
            text = self.driver.find_elements_by_class_name("embedDescription-1Cuq9a")[
                -1
            ].text.split("\n")
            last = len(text) + limit
            limit += 25

        while "in team" in text[last - limit + 24]:
            last -= 1
        return last

    def get_name(self):
        flag = 1
        name = ""
        rarity = ""
        CP = 0
        while flag:
            title = self.driver.find_elements_by_class_name("embedTitle-3OXDkz")[
                -1
            ].text
            text = self.driver.find_elements_by_class_name("embedDescription-1Cuq9a")[
                -1
            ].text
            m_title = re.search(r"received (.*) CP: (.*)!", title)
            m_text = re.search(r"Rarity:(.*)", text)
            try:
                name = m_title.group(1).strip()
                rarity = m_text.group(1).strip()
                CP = int(m_title.group(2).strip())
                flag = 0
            except AttributeError:
                print("retry: get name")
                time.sleep(1)
        return name, rarity, CP

    def wondertrade(self):
        max_level = False if int(self.config["trader"]["powerup"]) else True
        while True:
            self.try_function(self.send_command, 3, text="/wondertrade")
            if max_level:
                time.sleep(2)
            else:
                time.sleep(0.5)

            name, rarity, CP = self.get_name()
            print(name, rarity, CP)

            dream = self.config["trader"]["dream"].split(",")
            if rarity in ["Legendary", "Mythical"] or name in dream:
                # self.send_command(f'/info {name}')
                os.system('say "Legendary"')
                if max_level:
                    self.send_command(f"/fortrade remove")
                    time.sleep(1)
                return

            elif (rarity == "Rare" or CP >= int(self.config["trader"]["CP"])) and int(
                self.config["trader"]["show_info"]
            ):
                os.system('say "rare"')
                self.try_function(self.send_message, 5, text=f"!!info {name}")
                info = self.driver.find_elements_by_class_name(
                    "embedDescription-1Cuq9a"
                )[-1].text
                evolve_into = re.search(r"Evolves into: (.*)", info).group(1).strip()
                evolve = name
                while evolve_into != "None":
                    evolve = evolve_into
                    self.try_function(
                        self.send_message, 10, text=f"!!info {evolve_into}"
                    )
                    info = self.driver.find_elements_by_class_name(
                        "embedDescription-1Cuq9a"
                    )[-1].text
                    evolve_into = re.search(r"Evolves into: (.*)", info).group(1)

                self.try_function(self.send_message, 5, text=f"!!info mega {evolve}")
                self.try_function(self.send_message, 5, text=f"!!info {evolve} gmax")

                info = self.driver.find_elements_by_class_name(
                    "embedDescription-1Cuq9a"
                )[-1].text
                max_cp = re.search(r"Max CP: (.*)", info).group(1)
                if int(max_cp) > 2000:
                    countdown = int(self.config["trader"]["countdown"])
                    for i in range(countdown):
                        os.system(f'say "{countdown - i}"')
                        time.sleep(1)

            if not max_level:
                self.try_function(self.send_message, 5, text=f"!!powerup {name} max")
                time.sleep(1)
                last = str(self.find_last())
                self.send_message(last)
                time.sleep(1)
                respond = self.driver.find_elements_by_class_name("contents-2mQqc9")[
                    -1
                ].text
                if "cannot powerup any" in respond:
                    print("Reach Max Level!")
                    max_level = 1

                self.try_function(self.send_message, 2, text=f"!!fortrade add {name}")
                time.sleep(1)
                self.send_message(last)


if __name__ == "__main__":
    autoCatcher = AutoCatcher()
    autoCatcher.wondertrade()
    autoCatcher.driver.quit()
