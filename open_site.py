from static_vars import  static_vars
from layout import window, layout
from console import console
from selenium.webdriver.firefox.webdriver import WebDriver


@static_vars(window=window)
def open_site(values:dict, driver:WebDriver, all_links:list[list[str]], post_links:list[list[str]]):

    layout.nextbutton.Update(text=layout.keys.EXECUTING, disabled=True)
    console("Opening Browser...")

    try:
        console("Opening Homepage...")
        driver.get(values[layout.keys.HOMEPAGE])
        print(hex(id(driver)))

        links = [[link] for link in list(set(link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME,   'a')))]
        all_links.clear()
        all_links += links
        print(all_links)

        window[layout.keys.ALL_LINKS].update(all_links)

    except Exception as e:
        console(str(e), error=True)

    layout.nextbutton.Update(text=layout.keys.READ_POSTS, disabled=False)
    console("Homepage opened.")