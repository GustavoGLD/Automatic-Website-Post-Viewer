from static_vars import  static_vars
from layout import window, layout
from console import console
from selenium.webdriver.firefox.webdriver import WebDriver
import timeit
import PySimpleGUI as sg
from time import sleep

DELAY_SCROLLING = 0.02


@static_vars(window=window)
def read_posts(values:dict, driver:WebDriver, links:list[list[str]]):
    read_posts.window: sg.Window

    formated_links = [link[0] for link in links]

    layout.nextbutton.Update(text=layout.keys.EXECUTING, disabled=True)
    console("Starting Auto SEO Engagement...")

    try:
        for n, link in enumerate(formated_links):
            if n == 0:
                driver.get(link)
            elif values[layout.keys.MULTI_TAB]:
                driver.execute_script(f'''window.open(" ", "_blank");''')
                driver.switch_to.window(window_name=driver.window_handles[-1])
                driver.get(link)
            elif values[layout.keys.SINGLE_TAB]:
                driver.get(link)

            console(f"scrolling page {n}...")

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
            console(f"page {n} totally scrolled")

    except Exception as e:
        console(str(e), error=True)
        threading.Thread(target=driver.quit, daemon=True).start()
        console("closing browser")

    layout.nextbutton.Update(text=layout.keys.OPEN_SITE, disabled=False)