import PySimpleGUI as sg
from types import SimpleNamespace

LINKS = 3

class layout():
    class keys():
        HOMEPAGE = "homepage"
        TIME_SCROLLING = "time_scroll"
        MULTI_TAB = 'multitab'
        SINGLE_TAB = 'singletab'
        OPEN_SITE = "Open Website"
        EXECUTING = "Executing..."
        READ_POSTS = "Read Posts"
        NEXTBUTTON = "nextbutton"
        ALL_LINKS = 'all_links'
        POSTS_LINK = "postslink"

    homepage = [sg.Text('home:'), sg.Input(key=keys.HOMEPAGE, expand_x=True)]

    inputs = sg.Column([
        [sg.Text('page:'), sg.Input(key=f'address{n}', expand_x=True)] for n in range(1, LINKS + 1)
    ], expand_x=True)

    time_scrolling = sg.Column([[
        sg.Text('time scrolling:'),
        sg.Spin([i for i in range(0, 1000)], initial_value=35, key=keys.TIME_SCROLLING),
        sg.Text("seconds"),
        sg.Text("(for pages that don't increase in size when scrolling)",
                text_color='red', font=('italics', 8))
    ]])

    open_mode = sg.Column([[
        sg.Text("Way to open posts:"),
        sg.Radio('Multi tab', 'openmode', key=keys.MULTI_TAB, default=True),
        sg.Radio('Single tab', 'openmode', key=keys.SINGLE_TAB)
    ]])

    nextbutton = sg.Button(keys.OPEN_SITE, expand_x=True, key=keys.NEXTBUTTON)

    all_links = sg.Column([[]], expand_x=True)
    all_links.table = sg.Table([[]], ["Click on the posts to read"], enable_events=True, key=keys.ALL_LINKS,
                                expand_x=True, justification='left', num_rows=10)
    all_links.layout([
        [all_links.table]
    ])

    postslink = sg.Column([[]], expand_x=True)
    postslink.table = sg.Table([[]], ["Selected posts (click to remove)"], enable_events=True, key=keys.POSTS_LINK,
                                expand_x=True, justification='left', num_rows=5)
    postslink.layout([
        [postslink.table]
    ])

sgConsole = sg.Multiline(size=(60, 5), key='console', background_color="black", text_color="grey", expand_x=True)

window = sg.Window('Window Title', [
                    [layout.homepage],
                    [layout.time_scrolling],
                    [layout.open_mode],
                    [layout.nextbutton],
                    [layout.all_links],
                    [layout.postslink],
                    [sgConsole]
                    ])