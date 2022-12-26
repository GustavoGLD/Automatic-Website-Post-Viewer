import PySimpleGUI as sg

LINKS = 3

sg.theme('Topanga')

class Layout():
    class Keys():
        def __init__(self):
            self.HOMEPAGE = "homepage"
            self.TIME_SCROLLING = "time_scroll"
            self.MULTI_TAB = 'multitab'
            self.SINGLE_TAB = 'singletab'
            self.OPEN_SITE = "Open Website"
            self.EXECUTING = "Executing..."
            self.READ_POSTS = "Read Posts"
            self.NEXTBUTTON = "nextbutton"
            self.ALL_LINKS = 'all_links'
            self.POSTS_LINK = "postslink"

    def __init__(self):
        self.keys = Layout.Keys()
        self.homepage = [sg.Text('home:'), sg.Input(key=self.keys.HOMEPAGE, expand_x=True)]
        self.inputs = sg.Column([
            [sg.Text('page:'), sg.Input(key=f'address{n}', expand_x=True)] for n in range(1, LINKS + 1)
        ], expand_x=True)
        self.time_scrolling = sg.Column([[
            sg.Text('time scrolling:'),
            sg.Spin([i for i in range(0, 1000)], initial_value=35, key=self.keys.TIME_SCROLLING),
            sg.Text("seconds"),
            sg.Text("(for pages that don't increase in size when scrolling)",
                    text_color='red', font=('italics', 8))
        ]])
        self.open_mode = sg.Column([[
            sg.Text("Way to open posts:"),
            sg.Radio('Multi tab', 'openmode', key=self.keys.MULTI_TAB, default=True),
            sg.Radio('Single tab', 'openmode', key=self.keys.SINGLE_TAB)
        ]])
        self.nextbutton = sg.Button(self.keys.OPEN_SITE, expand_x=True, key=self.keys.NEXTBUTTON)
        self.all_links = sg.Column([[]], expand_x=True)
        self.all_links.table = sg.Table([[]], ["Click on the posts to read"], enable_events=True, key=self.keys.ALL_LINKS,
                                    expand_x=True, justification='left', num_rows=10)
        self.all_links.layout([
            [self.all_links.table]
        ])
        self.postslink = sg.Column([[]], expand_x=True)
        self.postslink.table = sg.Table([[]], ["Selected posts (click to remove)"], enable_events=True, key=self.keys.POSTS_LINK,
                                    expand_x=True, justification='left', num_rows=5)
        self.postslink.layout([
            [self.postslink.table]
        ])
        self.statusbar = sg.StatusBar('...', size=(50, 2), expand_x=True)

layout = Layout()

sgConsole = sg.Multiline(size=(60, 5), key='console', background_color="black", text_color="grey", expand_x=True)
