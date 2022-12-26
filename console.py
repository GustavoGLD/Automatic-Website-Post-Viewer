from static_vars import static_vars
from layout import sgConsole
import PySimpleGUI as sg

@static_vars(console=sgConsole)
def console(window:sg.Window, output: str, error: bool = False):
    console.console: sg.Multiline

    if error:
        console.console.print(str(output), text_color="red")
    else:
        console.console.print(str(output))
    window.refresh()
