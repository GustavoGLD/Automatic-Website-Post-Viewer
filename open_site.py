from layout import layout
from console import console
import PySimpleGUI as sg

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

def open_site(values:dict, driver:WebDriver, window:sg.Window, all_links:list[list[str]]):

    layout.nextbutton.Update(text=layout.keys.EXECUTING, disabled=True)

    #console(window, "Opening Homepage...")
    driver.get(values[layout.keys.HOMEPAGE])

    __links = list(set(link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME,   'a')))
    __links.sort()
    links = [[link] for link in __links]
    all_links.clear()
    all_links += links

    layout.statusbar.update(f'{len(links)} available links, possible posts to scroll')

    window[layout.keys.ALL_LINKS].update(all_links)


    layout.nextbutton.Update(text=layout.keys.READ_POSTS, disabled=False)
    #console(window, "Homepage opened.")
