from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


class HarFileLoader:
    def __init__(self, id, password, driver_path='./chromedriver', baseUrl='https://www.instagram.com/') -> None:
        self.driver_path = driver_path
        self.baseUrl = baseUrl
        self.id = id
        self.password = password

    # [(By.CSS_SELECTOR, value)]
    def busy_waiting(self, by_value_list, message="Page is not loaded yet ..."):
        values = [None] * len(by_value_list)

        while not any(values):
            try:
                for idx, (by, value) in enumerate(by_value_list):
                    values[idx] = self.browser.find_element(by, value)
            except NoSuchElementException:
                print(message)
                time.sleep(1)
                continue

        return values

    def set_options(self, options: Options):
        options.add_experimental_option("detach", True)
        options.add_argument("disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--auto-open-devtools-for-tabs")

    def load_har(self, username):
        posting_num = 0
        # Arguments
        chrome_options = Options()
        service = Service(executable_path=self.driver_path)
        self.set_options(chrome_options)

        self.browser = webdriver.Chrome(
            self.driver_path, options=chrome_options, service=service)

        self.browser.execute_cdp_cmd('Network.enable', {})

        self.browser.get(self.baseUrl)

        username_input, password_input = self.busy_waiting(
            [(By.CSS_SELECTOR, "input[name='username']"),
             (By.CSS_SELECTOR, "input[name='password']")], "Login page is not loaded yet ...")

        username_input.send_keys(self.id)
        password_input.send_keys(self.password)

        login_button = self.browser.find_element(
            by=By.XPATH, value="//button[@type='submit']")
        login_button.click()

        self.busy_waiting(
            [(By.XPATH, f'//div[contains(text(), "검색")]')], "Feed page is not loaded yet ...")

        # Move to user profile
        self.browser.get(f'{self.baseUrl}{username}')

        # Loading profile
        self.busy_waiting([
            (By.XPATH, f'//h2[contains(text(), "{username}")]')], "Profile page is not loaded yet ...")

        # Get total posting number
        posting_num = int(self.browser.find_element(
            By.CSS_SELECTOR, value="li > span._ac2a").text)

        first_post = self.busy_waiting(
            [(By.CSS_SELECTOR, "article > div > div > div:nth-child(1) > div > a")], "Profile page is not loaded yet ...")

        first_post[0].click()

        for _ in range(posting_num-1):
            # Loading post detail modal
            self.busy_waiting([(By.XPATH, '//article[@role="presentation"]')],
                              "Post detail modal is not loaded yet ...")
            try:
                next_pic = self.browser.find_element(
                    By.XPATH, "//button[@aria-label='다음']")
                while next_pic:
                    next_pic.click()
                    time.sleep(0.5)
                    next_pic = self.browser.find_element(
                        By.XPATH, "//button[@aria-label='다음']")
            except:
                pass
            next_post = self.busy_waiting(
                [(By.XPATH, "//div[@class=' _aaqg _aaqh']/button")])
            next_post[0].click()
