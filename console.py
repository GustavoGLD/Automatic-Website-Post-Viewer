from static_vars import static_vars
from layout import sgConsole, window
import PySimpleGUI as sg

@static_vars(console=sgConsole, window=window)
def console(output: str, error: bool = False):
    console.console: sg.Multiline
    console.window: sg.Window

    if error:
        console.console.print(str(output), text_color="red")
    else:
        console.console.print(str(output))
    console.window.refresh()
