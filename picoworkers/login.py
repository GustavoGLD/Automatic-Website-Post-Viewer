import time
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class Login():

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def __make_login__(self, login_email: str, login_password: str) -> None:

        self.driver.implicitly_wait(1)

        #write email in label
        self.driver.find_element(By.ID, "loginEmailPhone").send_keys(login_email)

        #write password in label
        self.driver.find_element(By.ID, "loginPassword").send_keys(login_password)

        #mark "remember me" button
        self.driver.find_element(By.CSS_SELECTOR, ".custom-control-label").click()

        #accept cookies
        self.driver.find_element(By.CSS_SELECTOR, ".cookie-bar__btn").click()

        #enter login
        self.driver.find_element(By.CSS_SELECTOR, ".btn-lg").click()

        #wait the page load by identifying if there is the categories seach element
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "dropdownMainCategory")))
        
        #delay
        time.sleep(3)



    def login(self):
        self.driver.get("https://picoworkers.com/login.php")

        print("~~~~~~ Picoworkers Login ~~~~~~")
        login_email = "gustavogld.picoworker@gmail.com"
        login_password = "757584175Gu_"
        self.__make_login__(login_email, login_password)