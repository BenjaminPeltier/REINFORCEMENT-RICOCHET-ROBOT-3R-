from ricochet_robot.game.Ricochet import Ricochet
import gym

class InterfaceRicochet(gym.Env):
    action_meaning = {
        0: ["Red", "left"],
        1: ["Red", "right"],
        2: ["Red", "up"],
        3: ["Red", "low"],
        4: ["Yellow", "left"],
        5: ["Yellow", "right"],
        6: ["Yellow", "up"],
        7: ["Yellow", "low"],
        8: ["Green", "left"],
        9: ["Green", "right"],
        10: ["Green", "up"],
        11: ["Green", "low"],
        12: ["Blue", "left"],
        13: ["Blue", "right"],
        14: ["Blue", "up"],
        15: ["Blue", "low"],
    }

    def __init__(self, grid, not_end_score=0, app=None):
        self.grid_file = grid
        self.ricochet = Ricochet()
        self.reset()
        self.app = app
        self.not_end_score = not_end_score

    def step(self, action):
        self.doAction(action)
        state = self.ricochet.grid.toMat()
        return state, self.reward(), self.ricochet.isWin()

    def reset(self):
        self.ricochet.grid.loadGrid(grid_file)

    def render(self):
        if self.app:
            app.board = self.ricochet.grid
        else:
            print(self.ricochet.grid)

    @staticmethod
    def listActions():
        return [f"Moves {val[0]} robot {val[1]}" for val in action_meaning.values()]
    
    def doAction(self, action):
        self.ricochet.move(*action_meaning[action])

    def reward(self):
        return 1 if self.ricochet.isWin() else self.not_end_score
