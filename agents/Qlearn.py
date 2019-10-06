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
            _, action = self.max_q(state)
        return action

    def max_q(self, state):
        best_val = - np.inf
        best_action = ""
        for new_action in state.listActions():
            temp_pos = state.copy()
            temp_pos.do_action(new_action)
            if temp_pos in self.q_table.keys():
                q_value = max(self.q_table[temp_pos].values())
            else:
                q_value = 0
                self.q_table[temp_pos] = {action: 0 for action in state.listActions()}
            if q_value > best_val or (q_value == best_val and rd.random() >= 0.5):
                best_val = q_value
                best_action = new_action
        return best_val, best_action

    def update_exploration(self):
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(self.exploration_min, self.exploration_rate)

    def learn(self, state, action):
        state2 = state.copy()
        state2.do_action(action)
        best_next_val, _ = self.max_q(state2)
        if state != state2:
            learned_value = state2.reward() + self.discount_factor * best_next_val
        else:
            learned_value = -0.5 + self.discount_factor * best_next_val

        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in state.listActions()}

        self.q_table[state][action] *= (1 - self.learning_rate)
        self.q_table[state][action] += self.learning_rate * learned_value

    def update_state(self, state, learning=True):
        action = self.choose_action(state)
        if learning:
            self.learn(state, action)
        state.do_action(action)
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
