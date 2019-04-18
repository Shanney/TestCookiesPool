import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class DbzdbCookies():

    def __init__(self, username, password, browser):
        self.url = 'http://www.dbzdb.com/WebManagement'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'j_username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        submit = self.wait.until(EC.element_to_be_clickable((By.NAME, 'imgsubmit')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(1)
        submit.click()

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert()
            if alert.text.find('错误'):
                return True
        # text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误')
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'header'))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

if __name__ == '__main__':
    result = DbzdbCookies('admin', '!QAZ2wsx',
    webdriver.Chrome(
        executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')).main()
    print(result)
