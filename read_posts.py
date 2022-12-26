from layout import layout
from console import console
import timeit
from time import sleep
from popup_info import pupup_info
from selenium.webdriver.firefox.webdriver import WebDriver

DELAY_SCROLLING = 0.02


def read_posts(values:dict, driver:WebDriver, links:list[list[str]]):

    formated_links = [link[0] for link in links]

    layout.nextbutton.Update(text=layout.keys.EXECUTING, disabled=True)
    #console(window, "Starting Auto SEO Engagement...")

    for n, link in enumerate(formated_links):
        if values[layout.keys.MULTI_TAB]:
            driver.execute_script(f'''window.open(" ", "_blank");''')
            driver.switch_to.window(window_name=driver.window_handles[-1])
            driver.get(link)
        elif values[layout.keys.SINGLE_TAB]:
            driver.get(link)

        #console(window, f"scrolling page {n}...")

        page_height = driver.execute_script("return document.body.scrollHeight")

        now_time = timeit.default_timer()
        init_time = now_time
        end_time = init_time + int(values[layout.keys.TIME_SCROLLING])

        while now_time < end_time:
            sleep(DELAY_SCROLLING / 2)

            now_time = timeit.default_timer()
            if now_time > end_time:
                break

            scroll_to = int(page_height * (timeit.default_timer() - init_time) / (end_time - init_time))
            driver.execute_script("window.scrollTo(0, " + str(scroll_to) + ")")

            sleep(DELAY_SCROLLING / 2)

    layout.nextbutton.Update(text=layout.keys.OPEN_SITE, disabled=False)