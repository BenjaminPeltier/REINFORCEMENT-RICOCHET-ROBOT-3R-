import time
from tkinter import mainloop
import argparse
import _thread
# from matplotlib import pyplot as plt
from ricochet_robot.GUI.GUI import Application
from ricochet_robot.game.Ricochet import Ricochet
from agents.DQN import DQN
from agents.Qlearn import Qlearn
from ricochet_robot.interface.interface_ricochet import InterfaceRicochet

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
]

def _model_act(app, model, *grids, nb_episode=10, nb_step=20, max_moves=50, output_path=None, learning=False):
    app.lastLog.set("Start !")

    # Pas sûr que l'ordre dans la boucle soit le plus pertinent
    for grid in grids:
        rico = InterfaceRicochet(grid, app=app)
        rico.render()
        app.lastLog.set(f"{grid} loaded !")

        for ep in range(nb_episode):
            app.lastLog.set(f"Starting episode {ep+1}")
            app.lastLog.set(f"Learning ...")
            for step in range(nb_step):
                app.lastLog.set(f"Step {step+1}")
                rico.reset()

                for moves in range(max_moves):
                    action = model.updateState(rico, learning=learning)
                    if rico.reward() == 1:
                        app.lastLog.set(f"Win in {moves} movements")
                        break

            app.lastLog.set(f"Result episode {ep+1}")
            for _ in range(max_moves):
                action = model.updateState(rico, learning=False)
                rico.render()
                app.lastLog.set(f"Action : {rico.readable_translation(action)}")
                time.sleep(0.2)
                if rico.reward() == 1:
                    app.lastLog.set(f"Win in {moves} movements")
                    break

            if output_path:
                model.save_model(output_path)
                app.lastLog.set("Model saved!")

    app.lastLog.set("The end")


def show(args):
    grid = args.grid
    rico = Ricochet()
    rico.grid.loadGrid(grid)
    app = Application(board=rico.grid, showGrid=True)
    app.lastLog.set(f"{grid} loaded !")
    app.mainloop()


def learn(args):
    grid = args.grids[0]
    rico = Ricochet()
    rico.grid.loadGrid(grid)
    app = Application(board=rico.grid, showGrid=True)
    if args.deep:
        model = DQN((16, 16), 16)
    else:
        model = Qlearn()

    if args.input:
        model.load_model(args.input)

    _thread.start_new_thread(
        _model_act, (app, model, *args.grids),
        {"output_path":(args.output if args.output else None), "learning":1}
    )
    app.mainloop()


def play(args): # grid, model
    grid = args.grids[0]
    rico = Ricochet()
    rico.grid.loadGrid(grid)
    app = Application(board=rico.grid, showGrid=True)
    if args.deep:
        model = DQN((16, 16), 16, exploration_rate=0, exploration_decay=0, exploration_min=0)
    else:
        model = Qlearn()
    model.load_model(args.model)

    _thread.start_new_thread(
        _model_act, (app, model, *args.grids),
        {"learning":False, "nb_episode":1, "nb_step":0, "max_moves":500}
    )
    app.mainloop()


def demo(args):
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
        app.lastLog.set("The end")
        # rico.grid.saveGrid("grids/...")

    rico = Ricochet()
    rico.grid.loadGrid("grids/grid1.csv")
    app = Application(board=rico.grid, showGrid=True)

    _thread.start_new_thread( actions, (rico, app) )
    app.mainloop()


def get_args():
    parser = argparse.ArgumentParser(description="Reinforcement Ricochet Robot (3R)")
    parser.set_defaults(func=demo)
    subparsers = parser.add_subparsers(help="Sub-commands you can use")

    # command show
    parser_show = subparsers.add_parser("show", help="Show a grid")
    parser_show.add_argument("grid", help="The grids you want to show")
    parser_show.set_defaults(func=show)

    # command learn
    parser_learn = subparsers.add_parser("learn", help="Learn a model")
    parser_learn.add_argument("-i", "--input", help="A pretrained model")
    parser_learn.add_argument("-o", "--output", help="The output model")
    parser_learn.add_argument("-d", "--deep", action="store_true", help="Use deep Qnetwork or basic qlearning")
    parser_learn.add_argument("grids", nargs="+", help="The grids you want to learn on")
    parser_learn.set_defaults(func=learn)

    # command play
    parser_play = subparsers.add_parser("play", help="Play a model")
    parser_play.add_argument("-d", "--deep", action="store_true", help="Use deep Qnetwork or basic qlearning")
    parser_play.add_argument("model", help="The model you want to use")
    parser_play.add_argument("grids", nargs="+", help="The grids you want to play on")
    parser_play.set_defaults(func=play)

    # command demo
    parser_demo = subparsers.add_parser("demo", help="Play a demo")
    parser_demo.set_defaults(func=demo)

    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    return parser.parse_args()


def main():
    args = get_args()
    args.func(args)
    

if __name__ == "__main__":
    main()