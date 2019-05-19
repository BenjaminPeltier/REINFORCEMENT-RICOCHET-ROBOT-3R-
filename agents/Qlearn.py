import pickle as pkl
import random as rd
import numpy as np

class Qlearn:
    def __init__(self, learning_rate = 0.01, discount_factor = 0.009, exploration_rate = 0.95, exploration_decay=0.99, exploration_min=0.01):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_min = exploration_min
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def __str__(self):
        res = ""
        for key, dico in self.q_table.items():
            res += f"{key} :\n"
            for direction, val in dico.items():
                res += f"   {direction} : {val}\n"
        return res

    def choose_action(self, state):
        if self.exploration_rate > rd.random():
            action = rd.choice(state.listActions())
        else:
            _, action = self.maxQ(state)
        return action

    def maxQ(self, state):
        bestVal = - np.inf
        bestAction = ""
        for newAction in state.listActions():
            tempPos = state.copy()
            tempPos.doAction(newAction)
            if tempPos in self.q_table.keys():
                q_value = max(self.q_table[tempPos].values())
            else:
                q_value = 0
                self.q_table[tempPos] = {action: 0 for action in state.listActions()}
            if q_value > bestVal :
                bestVal = q_value
                bestAction = newAction
        return bestVal, bestAction

    def updateExplorationRate(self):
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(self.exploration_min, self.exploration_rate)

    def learn(self, state, action):
        state2 = state.copy()
        state2.doAction(action)
        bestNextVal, _ = self.maxQ(state2)
        if state != state2:
            learned_value = state2.reward() + self.discount_factor * bestNextVal
        else:
            learned_value = -0.5 + self.discount_factor * bestNextVal
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * learned_value

    def updateState(self, state, learning=True):
        action = self.choose_action(state)
        if learning:
            self.learn(state, action)
        state.doAction(action)
        return action

    def save_model(self, filename):
        if filename.split(".")[-1] != "mod":
            filename += ".mod"
        with open(filename, "wb") as save_file:
            pkl.dump(self, save_file)

    def load_model(self, filename):
        if filename.split(".")[-1] != "mod":
            filename += ".mod"
        with open(filename, "rb") as loading_file:
            temp = pkl.load(loading_file)
        self.learning_rate = temp.learning_rate
        self.discount_factor = temp.discount_factor
        self.exploration_rate = temp.exploration_rate
        self.q_table = temp.q_table
