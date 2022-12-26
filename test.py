import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
table = sg.Table([[1,2,3], [4,5,6]], ['Col 1','Col 2','Col 3'], num_rows=2)
layout = [
    [table],
    [sg.Button("salve")]
]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "salve":
        table.update()


window.close()