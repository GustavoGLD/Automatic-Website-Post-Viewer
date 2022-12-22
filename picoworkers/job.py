from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from enum import Enum, auto
import subprocess
import time

class JobInfo(Enum):
    INTERNATIONALITY = 0
    NAME = auto()
    LEVEL = auto()
    PAYMENT = auto()
    TTR = auto()
    JOBS_DONE = auto()
    SUCCESS = auto()
    ID = auto()

class Job():
    def __init__(self, driver: WebDriver, web_element: WebElement) -> None:
        self.driver = driver
        self.web_element = web_element
        self.job_id = web_element.get_attribute("data-job-id")
        self.link = "https://sproutgigs.com/jobs/submit-task.php?Id=" + self.job_id
        self.text = web_element.text
        self.__instructions__ = ''

        self.__infos__ = web_element.text.split('\n')
        if 'FEATURED' in self.__infos__: self.__infos__.remove('FEATURED')
        if len(self.__infos__) != 7: raise Exception("the job info list is out of expected")
        self.__infos__.append(self.job_id)

    def get_infos(self, infos:list[JobInfo]) -> list[str]:
        return [self.__infos__[info.value] for info in infos]

    #open job page
    def open(self):
        if f"Id={self.job_id}" not in self.driver.current_url: self.driver.get(self.link)

    def set_instructions(self):
        #if instructions already defined
        if self.__instructions__ != '': return

        self.open()

        self.__instructions__ = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.ID, "job-instructions"))
        ).text

    def get_instructions(self) -> str:
        self.set_instructions()
        return self.__instructions__

    def hold_job(self, print_info=False, cancel_hold=False) -> None:

        #if not on the job page, go there
        if f"Id={self.job_id}" not in self.driver.current_url:
            self.open()


        #click on "hold job"
        self.driver.find_element(By.ID, "hold-job").click()

        #cancel to hold job (for test purpose)
        if cancel_hold:
            self.driver.find_element(By.CSS_SELECTOR, ".swal2-cancel").click()
        else:
            #accept to hold job
            self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()

            time.sleep(0.5)

            #"ok" button
            self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()

        if print_info:
            print(self.driver.find_element(By.ID, "swal2-html-container").text)


    def hide_job(self) -> None:

        #if not on the job page, go there
        if f"Id={self.job_id}" not in self.driver.current_url:
            self.open()

        hide_job_button = self.driver.find_element(By.CSS_SELECTOR, ".hide-job")
        self.driver.execute_script("arguments[0].click();", hide_job_button)


    #open job page in a browser by os.system()
    def open_in_other_browser(self, path: str = "chrome.exe") -> None:
        subprocess.Popen([path, self.link])


    def open_in_other_tab(self, switch_=False) -> None:
        self.driver.execute_script(f'window.open("{self.link}", "_blank");')
        print(self.driver.window_handles)
        if not switch_:
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            self.driver.switch_to.window(self.driver.window_handles[-1])