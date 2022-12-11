from threading import Thread
from time import sleep

val = [True] # list object
def change():
    val[0] = False  # list address stays the same, update attribute

def start():
    t = Thread(target=change)
    t.start()
    sleep(1)

    print(val[0])  # False

start()