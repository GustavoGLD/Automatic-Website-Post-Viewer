from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
import PySimpleGUI as sg
import threading
import timeit
from time import sleep

FONT_SIZE = 12
DELAY_SCROLLING = 0.02
LINKS = 3

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

class _layout():
    inputs = list[list[sg.Text | sg.Input]]()
    for n in range(1, LINKS + 1):
        inputs += ([[sg.Text('link:'), sg.Input(key=f'address{n}', expand_x=True)]])

    time_scrolling = [sg.Text('time scrolling:'),
                      sg.Spin([i for i in range(0, 1000)], initial_value=35, key='time_scroll'),
                      sg.Text("seconds"),
                      sg.Text("(for pages that don't increase in size when scrolling)",
                        text_color='red', font=('italics', 8))]

    open_mode = [sg.Text("Way to open posts:"),
                 sg.Radio('Multi tab', 'openmode', key='multitab', default=True),
                 sg.Radio('Single tab', 'openmode', key='singletab')]

__console__ = sg.Multiline(size=(60, 10), key='console', background_color="black", text_color="grey", expand_x=True)

layout = [_layout.inputs,
          _layout.time_scrolling,
          _layout.open_mode,
          [sg.Button("read site", expand_x=True, key='openwebd')],
          [__console__]]

window = sg.Window('Window Title', layout)


@static_vars(console=__console__, window=window)
def console(output: str, error: bool = False):
    console.console: sg.Multiline
    console.window: sg.Window

    if error:
        console.console.print(str(output), text_color="red")
    else:
        console.console.print(str(output))
    console.window.refresh()

@static_vars(window=window)
def read_site(event:str, values:dict):
    read_site.window: sg.Window

    read_site.window['openwebd'].Update(text="executing", disabled=True)
    console("opening browser...")

    driver: WebDriver = webdriver.Firefox()
    console("loading address...")

    try:
        for n in range(1, LINKS + 1):
            if n == 1:
                driver.get(values[f'address{n}'])
            elif values['multitab']:
                driver.execute_script(f'''window.open(" ", "_blank");''')
                driver.switch_to.window(window_name=driver.window_handles[-1])
                driver.get(values[f'address{n}'])
            elif values['singletab']:
                driver.get(values[f'address{n}'])

            console(f"scrolling page {n}...")

            page_height = driver.execute_script("return document.body.scrollHeight")

            now_time = timeit.default_timer()
            init_time = now_time
            end_time = init_time + int(values['time_scroll'])

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

    console.window['openwebd'].Update(text="read site", disabled=False)

while True:

    event, values = tuple[str, dict](window.read())

    print(values)

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    elif "openwebd" in event:
        threading.Thread(target=read_site, args=(event, values,), daemon=True).start()
