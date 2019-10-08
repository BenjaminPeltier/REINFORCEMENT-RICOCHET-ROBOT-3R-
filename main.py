import time
import random as rd
from tkinter import mainloop
import argparse
import _thread
from ricochet_robot.gui.gui import Application
from ricochet_robot.game.ricochet import Ricochet
from agents.dqn import DQN
from agents.qlearn import Qlearn
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

def _model_act(app, model, *grids, nb_episode=500, nb_step=100, max_moves=256, output_path=None, learning=False):
    app.last_log.set("Start !")

    # Pas sûr que le choix aléatoire des grilles soit le plus pertinent
    rico = InterfaceRicochet(grids[0], app=app, not_end_score=-0.05)
    
    for ep in range(nb_episode):
        grid = rd.choice(grids)
        rico.grid_file = grid
        rico.reset()
        rico.render()
        app.last_log.set(f"{grid} loaded !")

        app.last_log.set(f"Starting episode {ep+1}")
        app.last_log.set(f"Learning ...")
        for step in range(nb_step):
            app.last_log.set(f"Step {step+1}")
            rico.reset()

            for moves in range(max_moves):
                action = model.update_state(rico, learning=learning)
                if rico.reward() == 1:
                    app.last_log.set(f"Win in {moves} movements")
                    break

        app.last_log.set(f"Result episode {ep+1}")
        eps = model.exploration_rate
        model.exploration_rate = model.exploration_min
        for _ in range(max_moves):
            action = model.update_state(rico, learning=False)
            rico.render()
            app.last_log.set(f"Action : {rico.readable_translation(action)}")
            time.sleep(0.2)
            if rico.reward() == 1:
                app.last_log.set(f"Win in {moves} movements")
                break
        model.exploration_rate = eps

        if output_path:
            model.save_model(output_path)
            app.last_log.set("Model saved!")

    app.last_log.set("The end")


def show(args):
    grid = args.grid
    rico = Ricochet()
    rico.grid.load_grid(grid)
    app = Application(board=rico.grid, show_grid=True)
    app.last_log.set(f"{grid} loaded !")
    app.mainloop()


def learn(args):
    grid = args.grids[0]
    rico = Ricochet()
    rico.grid.load_grid(grid)
    app = Application(board=rico.grid, show_grid=True)
    if args.deep:
        model = DQN((16, 16), 16, verbose=True)
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
    rico.grid.load_grid(grid)
    app = Application(board=rico.grid, show_grid=True)
    if args.deep:
        model = DQN((16, 16), 16, exploration_rate=0, exploration_decay=0, exploration_min=0)
    else:
        model = Qlearn(exploration_rate=0, exploration_decay=0, exploration_min=0)
    model.load_model(args.model)

    _thread.start_new_thread(
        _model_act, (app, model, *args.grids),
        {"learning":False, "nb_episode":1, "nb_step":0, "max_moves":500}
    )
    app.mainloop()


def demo(args):
    def actions(rico, app):
        app.last_log.set("Start !")
        for step in SEQUENCE:
            print(rico.grid)
            time.sleep(1)
            rico.move(*step)
            print(rico.grid)
            app.board = rico.grid
            app.last_log.set(f"{step[0]} : {step[1]}")
            app.last_log.set(f"Win ? {rico.is_win()}")
        app.last_log.set("The end")
        # rico.grid.save_grid("grids/...")

    rico = Ricochet()
    rico.grid.load_grid("grids/grid1.csv")
    app = Application(board=rico.grid, show_grid=True)

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