from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

import PySimpleGUI as sg
import threading

from layout import layout
from open_site import open_site
from read_posts import read_posts

from dataclasses import dataclass
from popup_info import pupup_info

FONT_SIZE = 12
DELAY_SCROLLING = 0.02


def pop_up(driver:WebDriver):
    window_layout = [
        [layout.homepage],
        [layout.time_scrolling],
        [layout.open_mode],
        [layout.nextbutton],
        [layout.all_links],
        [layout.postslink],
        [layout.statusbar],
    ]

    popup_window = sg.Window('Window Title', window_layout)

    all_links = list[list[str]]()
    post_links = list[list[str]]()

    while True:

        event, values = tuple[str, dict](popup_window.read())

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        elif layout.nextbutton.key in event:
            if popup_window[layout.keys.NEXTBUTTON].get_text() == layout.keys.OPEN_SITE:
                threading.Thread(target=open_site, args=(values, driver, popup_window, all_links,), daemon=True).start()

            elif popup_window[layout.keys.NEXTBUTTON].get_text() == layout.keys.READ_POSTS:
                threading.Thread(target=read_posts, args=(values, driver, post_links), daemon=True).start()
                popup_window.close()

        elif layout.keys.ALL_LINKS in event and values[layout.keys.ALL_LINKS]:
            post_links += [all_links.pop(values[layout.keys.ALL_LINKS][0])]

            popup_window[layout.keys.ALL_LINKS].update(all_links)
            popup_window[layout.keys.POSTS_LINK].update(post_links)
            layout.statusbar.update(f'{len(all_links)} available links; {len(post_links)} selected links')

        elif layout.keys.POSTS_LINK in event and values[layout.keys.POSTS_LINK]:
            all_links += [post_links.pop(values[layout.keys.POSTS_LINK][0])]

            popup_window[layout.keys.ALL_LINKS].update(all_links)
            popup_window[layout.keys.POSTS_LINK].update(post_links)
            layout.statusbar.update(f'{len(all_links)} available links; {len(post_links)} selected links')

#driver = webdriver.Firefox()
#pop_up(driver)