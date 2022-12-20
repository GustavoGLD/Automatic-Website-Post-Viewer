from logging import exception
import time
from typing import Callable, List
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from picoworkers.job import Job # type: ignore
from picoworkers.filter_by import filter_by # type: ignore


class Category():

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def available_categories(self) -> List[str]:

        #if not in job search page, go there
        if "jobs.php" not in self.driver.current_url:
            self.driver.find_element(By.CSS_SELECTOR, ".navbar-brand").click()

        #open categories searcher
        self.driver.find_element(By.ID, "dropdownMainCategory").click()

        #time for categories searcher to be scrollable
        time.sleep(0.2)

        #get inputs with class "category"
        categories_input: List[WebElement] = self.driver.find_elements(By.NAME, "category")

        #get webelement parents
        page_filter__options: List[WebElement] = [page_filter__option.find_element(By.XPATH, "..") 
                                                    for page_filter__option in categories_input]

        categories = list[str]()

        for page_filter__option in page_filter__options:

            #get category name
            _category: str = page_filter__option.find_element(By.CLASS_NAME, "custom-control-label").text 

            if _category != "":
                categories.append(_category)

        #close categories searcher
        self.driver.find_element(By.ID, "dropdownMainCategory").click()

        return categories


    def filter_by_category(self, category_name: str, subcategory_name:str = "") -> None:
        
        #if not in job search page, go there
        if "jobs.php" not in self.driver.current_url:
            self.driver.find_element(By.CSS_SELECTOR, ".navbar-brand").click()

        #try to scroll categories searcher
        while True:
            try:
                #open categories searcher
                self.driver.find_element(By.ID, "dropdownMainCategory").click()

                #time for categories searcher to be scrollable
                time.sleep(0.2)

                #select category
                self.driver.find_element(By.XPATH, f"//label[contains(.,\'{category_name}\')]").click()

                #confirm and search
                self.driver.find_element(By.CSS_SELECTOR, ".show > .page-filter__menu-footer > .btn-primary").click()

                #open subcategory and made the same process above
                if subcategory_name:
                    self.driver.find_element(By.ID, "dropdownSubCategory").click()
                    time.sleep(0.2)
                    self.driver.find_element(By.XPATH, f"//label[contains(.,\'{subcategory_name}\')]").click()
                    self.driver.find_element(By.CSS_SELECTOR, "div.show:nth-child(2) > div:nth-child(2) > button:nth-child(2)").click()

                break

            except (ElementNotInteractableException, NoSuchElementException):
                print(f"back to browser to main tab ({exception})")

        #wait for the elements to load
        while len(self.driver.find_elements(By.CLASS_NAME, "is-loading")) != 0:
            time.sleep(0.1)


    def __scroll_results_down__(self):
        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                self.driver.find_element(By.CSS_SELECTOR, ".load-more").click()
                time.sleep(0.1)
            except (ElementNotInteractableException, NoSuchElementException):
                pass

            #wait for the elements to load
            while True:
                try:
                    self.driver.find_element(By.CLASS_NAME, "is-loading")
                except Exception:
                    break
                time.sleep(0.1)

            if not self.driver.find_element(By.CSS_SELECTOR, ".load-more").is_displayed():
                break


    def get_jobs_items(self, category_name:str="", subcategory_name:str="", scroll_down:bool = False, filters:List[Callable[[WebDriver], List[str]]] = []) -> List[Job]:

        if category_name:
            self.filter_by_category(category_name, subcategory_name)

        if scroll_down:
            self.__scroll_results_down__()

        jobs = dict[WebElement, str]({
            webelement: webelement.get_attribute("data-job-id") 
            for webelement in self.driver.find_elements(By.CLASS_NAME, "jobs__item--client-starter")
        })

        if filters:
            ids_to_remove = list[str]()
            for _filter in filters:
                ids_to_remove.extend(_filter(self.driver))

            for job_elem, job_id in jobs.copy().items(): 
                if job_id in ids_to_remove:
                    del jobs[job_elem]
        

        return [Job(self.driver, job) for job in list(jobs.keys())]

