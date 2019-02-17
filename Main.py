import time
from tkinter import mainloop
import _thread
from GUI import Application
from Ricochet import Ricochet

SEQUENCE = [
    ("Blue", "left"),
    ("Blue", "up"),
    ("Green", "left"),
    ("Green", "low"),
    ("Green", "left"),
    ("Green", "up"),
    ("Green", "left"),
    ("Green", "up"),
    ("Red", "left"),
    ("Red", "up"),
    ("Red", "right")
]

def actions(rico, app):
    app.lastLog.set("Start !")
    for step in SEQUENCE:
        # print(rico.grid)
        time.sleep(3)
        rico.move(*step)
        # print(rico.grid)
        app.board = rico.grid
        app.lastLog.set(f"{step[0]} : {step[1]}")
        app.lastLog.set(f"Win ? {rico.isWin()}")

def main():
    rico = Ricochet()
    rico.grid.loadGrid("grids/grid1.csv")
    app = Application(board=rico.grid)

    _thread.start_new_thread( actions, (rico, app) )
    app.mainloop()
    

if __name__ == "__main__":
    main()