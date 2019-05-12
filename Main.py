import time
from tkinter import mainloop
import argparse
import _thread
from ricochet_robot.GUI.GUI import Application
from ricochet_robot.game.Ricochet import Ricochet

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
    ("Red", "right"),
    ("Yellow", "right"),
    ("Yellow", "right"),
    ("Red", "low"),
    ("Yellow", "low"),
    ("Yellow", "right"),
    ("Yellow", "up"),
    ("Yellow", "left")
]

def actions(rico, app):
    app.lastLog.set("Start !")
    for step in SEQUENCE:
        print(rico.grid)
        time.sleep(1)
        rico.move(*step)
        print(rico.grid)
        app.board = rico.grid
        app.lastLog.set(f"{step[0]} : {step[1]}")
        app.lastLog.set(f"Win ? {rico.isWin()}")

def show():
    pass

def learn():
    pass

def play():
    pass

def args():
    parser = argparse.ArgumentParser(description="Reinforcement Ricochet Robot (3R)")
    subparsers = parser.add_subparsers(help='Sub-commands you can use')

    # command show
    parser_show = subparsers.add_parser('show', help='Show a grid')
    parser_show.set_defaults(func=show)

    # command learn
    parser_learn = subparsers.add_parser('learn', help='Learn a model')
    parser_learn.add_argument('-i', '--input', help='A pretrained model')
    parser_learn.add_argument('-o', '--output', help='The output model')
    parser_learn.set_defaults(func=learn)

    # command play
    parser_play = subparsers.add_parser('play', help='Play a model')
    parser_play.add_argument('model', help='The model you want to use')
    parser_play.set_defaults(func=play)

    parser.add_argument("grids", nargs="+", help="The grids you want to play on")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    return parser.parse_args()


def main():
    print(args().input)
    # rico = Ricochet()
    # rico.grid.loadGrid("grids/grid1.csv")
    # app = Application(board=rico.grid, showGrid=True)

    # _thread.start_new_thread( actions, (rico, app) )
    # app.mainloop()
    

if __name__ == "__main__":
    main()