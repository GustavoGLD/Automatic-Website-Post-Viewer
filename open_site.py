from static_vars import  static_vars
from layout import window, layout
from console import console
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By


@static_vars(window=window)
def open_site(values:dict, driver:WebDriver, all_links:list[list[str]], post_links:list[list[str]]):

    layout.nextbutton.Update(text=layout.keys.EXECUTING, disabled=True)
    console("Opening Browser...")

    try:
        console("Opening Homepage...")
        driver.get(values[layout.keys.HOMEPAGE])

        __links = list(set(link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME,   'a')))
        __links.sort()
        links = [[link] for link in __links]
        all_links.clear()
        all_links += links

        layout.statusbar.update(f'{len(links)} available links, possible posts to scroll')

        window[layout.keys.ALL_LINKS].update(all_links)

    except Exception as e:
        console(str(e), error=True)

    layout.nextbutton.Update(text=layout.keys.READ_POSTS, disabled=False)
    console("Homepage opened.")
