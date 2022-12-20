from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Callable, List

from picoworkers.job import Job # type: ignore


#lamba functions that return the Jobs ID (string)
class filter_by():
    
    NOT_ON_HOLD: Callable[[WebDriver], List[str]] = lambda driver: [
        _on_hold.find_element(By.XPATH, "../..").get_attribute("data-job-id")
        for _on_hold in driver.find_elements(By.XPATH, "//span[text()='ON HOLD']")
    ]

    def TTR(ttr:int) -> Callable[[WebDriver], List[str]]: # type: ignore
        __function: Callable[[WebDriver], List[str]] = lambda driver: [
            job.find_element(By.XPATH, "..").get_attribute("data-job-id")
            for job in list(filter(lambda x: int(x.text) != ttr, 
                driver.find_elements(By.XPATH, "//div[@data-tippy-content='Time to Rate.']")
            ))
        ]
        return __function 