import tempfile
import os
from ricochet_robot.game.Ricochet import Ricochet
import gym
import numpy as np

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
        self.ricochet = Ricochet()
        self.grid_file = grid
        self.reset()
        self.app = app
        self.not_end_score = not_end_score

    def step(self, action):
        self.doAction(action)
        state = self.ricochet.grid.toMat()
        return state, self.reward(), self.ricochet.isWin()

    def reset(self):
        self.ricochet.grid.loadGrid(self.grid_file)

    def render(self):
        if self.app:
            self.app.board = self.ricochet.grid
        else:
            print(self.ricochet.grid)

    def is_terminal(self):
        return self.reward() == 1

    @classmethod
    def listActions(cls):
        return [key for key in cls.action_meaning.keys()]

    @classmethod
    def translation(cls, action):
        return cls.action_meaning[action]

    @classmethod
    def readable_translation(cls, action):
        return f"{cls.action_meaning[action][0]} moves {cls.action_meaning[action][1]}"
    
    def doAction(self, action):
        self.ricochet.move(*self.translation(action))

    def reward(self):
        return 1 if self.ricochet.isWin() else self.not_end_score

    def _save_temp(self):
        fd, file_name = tempfile.mkstemp(suffix=".csv", prefix="grid")
        # print(self.ricochet.grid)
        self.ricochet.grid.saveGrid(file_name)
        # with open(file_name, "r") as csv:
        #     print(csv.read())
        os.close(fd)
        return file_name

    def copy(self):
        file_name = self._save_temp()
        res = InterfaceRicochet(file_name, not_end_score=self.not_end_score, app=self.app)

        os.remove(file_name)
        return res

    def tomat(self):
        return self.ricochet.grid.grid

    def __hash__(self):
        return hash(str(self.ricochet.grid.grid.data))

    def __eq__(self, value):
        if not isinstance(value, InterfaceRicochet):
            return False
        return np.array_equal(self.ricochet.grid.grid, value.ricochet.grid.grid)

    def __str__(self):
        return str(self.ricochet.grid)
