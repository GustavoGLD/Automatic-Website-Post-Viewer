from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver

import PySimpleGUI as sg
import threading

from layout import layout, window
from open_site import open_site
from read_posts import read_posts

FONT_SIZE = 12
DELAY_SCROLLING = 0.02

all_links = list[list[str]]()
post_links = list[list[str]]()
driver: WebDriver = None
last_event = ''

while True:

    event, values = tuple[str, dict](window.read())

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    elif layout.nextbutton.key in event:
        if window[layout.keys.NEXTBUTTON].get_text() == layout.keys.OPEN_SITE:
            driver = webdriver.Firefox()
            threading.Thread(target=open_site, args=(values, driver, all_links, post_links,), daemon=True).start()
            print(all_links)
        elif window[layout.keys.NEXTBUTTON].get_text() == layout.keys.READ_POSTS:
            threading.Thread(target=read_posts, args=(values, driver, post_links,), daemon=True).start()

    elif layout.keys.ALL_LINKS in event and values[layout.keys.ALL_LINKS]:
        post_links += [all_links.pop(values[layout.keys.ALL_LINKS][0])]

        window[layout.keys.ALL_LINKS].update(all_links)
        window[layout.keys.POSTS_LINK].update(post_links)

    elif layout.keys.POSTS_LINK in event and values[layout.keys.POSTS_LINK]:
        all_links += [post_links.pop(values[layout.keys.POSTS_LINK][0])]

        window[layout.keys.ALL_LINKS].update(all_links)
        window[layout.keys.POSTS_LINK].update(post_links)