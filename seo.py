import time
import pickle
import threading
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from picoworkers.picoworker import Picoworker
from picoworkers.job import Job, JobInfo
from selenium.common.exceptions import TimeoutException

#options to optimization
options = Options()
options.set_preference("network.http.pipelining", True)
options.set_preference("network.http.proxy.pipelining", True)
options.set_preference("network.http.pipelining.maxrequests", 8)
options.set_preference("content.notify.interval", 500000)
options.set_preference("content.notify.ontimer", True)
options.set_preference("content.switch.threshold", 250000)
options.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
options.set_preference("browser.startup.homepage", "about:blank")
options.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
options.set_preference("browser.pocket.enabled", False) # Duck pocket too!
options.set_preference("loop.enabled", False)
options.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
options.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
options.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
options.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
options.set_preference("browser.display.use_system_colors", True) # Use system colors.
options.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
options.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temporary files.
options.set_preference("browser.shell.checkDefaultBrowser", False)
options.set_preference("browser.startup.homepage", "about:blank")
options.set_preference("browser.startup.page", 0) # blank
options.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
options.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
options.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
options.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
options.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
options.set_preference("extensions.checkCompatibility", False) # Addon update disabled
options.set_preference("extensions.checkUpdateSecurity", False)
options.set_preference("extensions.update.autoUpdateEnabled", False)
options.set_preference("extensions.update.enabled", False)
options.set_preference("general.startup.browser", False)
options.set_preference("plugin.default_plugin_disabled", False)
options.set_preference("permissions.default.image", 2) # Image load disabled again

driver = webdriver.Firefox(options=options)

CATEGORY = "SEO, Promote Content, Search, Engage"
SUBCATEGORY = "Visit + Engage 1x"

progress = sg.ProgressBar(
    max_value=0,
    orientation='h',
    size=(20, 20),
    expand_x=True
)

table = sg.Table(
    values=[[]],
    headings=[' ID ', 'LEVEL', ' TTR ', ' DONE '],
    num_rows=15,
    expand_x=True,
    expand_y=True,
    enable_events=True,
    key='table'
)

jobInstruction = sg.Text("")

layout = [
    [
        sg.Column([[table], [progress]], expand_y=True),
        sg.Column([[jobInstruction]])
    ]
]

picow = Picoworker(driver)
picow.login()

driver.get("https://sproutgigs.com/jobs.php?category=10&sub_category=1000")

window = sg.Window('Window Title', layout, size=(700, 512))

jobs: list[Job] = []

def get_job_instructions(jobs: list[Job], table:sg.Table, window:sg.Window):
    jobs_items = picow.get_jobs_items(scroll_down=True)
    instructions: list[str] = []

    for i, job in enumerate(jobs_items, start=1):
        try:
            instructions.append(job.get_instructions())
        except TimeoutException:
            print("job not available")
        else:
            jobs.append(job)
        progress.UpdateBar(i, len(jobs_items))
    table.update([job.get_infos([JobInfo.ID, JobInfo.LEVEL, JobInfo.TTR, JobInfo.JOBS_DONE]) for job in jobs])
    pickle.dump(instructions, open("save4.p", "wb"))
    print(instructions)

threading.Thread(target=get_job_instructions, args=(jobs, table, window,), daemon=True).start()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print(event, values)

    if event == 'table':
        jobInstruction.Update(jobs[values['table'][0]].get_instructions())