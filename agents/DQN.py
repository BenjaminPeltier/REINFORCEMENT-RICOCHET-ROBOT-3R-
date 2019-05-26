from collections import deque
import time
import random as rd
import numpy as np
from agents.Qlearn import Qlearn
from keras.callbacks import TensorBoard
from keras.layers import Dense, Flatten, Conv2D, Reshape, Input, MaxPool2D, Conv1D, MaxPool1D
from keras import Sequential
from keras.optimizers import Adam, SGD # SGD : plus d'epochs

class DQN(Qlearn):

    def __init__(self, state_size, action_size, model_path=None, name=None, learning_rate=0.01, discount_factor=0.009, exploration_rate=0.95, exploration_decay=0.99, exploration_min=0.01, epochs=10, batch_size=64, memory_size=1000000, fixed_period=64, verbose=0):
        super().__init__(
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            exploration_rate=exploration_rate,
            exploration_decay=exploration_decay,
            exploration_min=exploration_min
        )
        self.state_size = state_size
        self.action_size = action_size
        self.epochs = epochs
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.fixed_period = fixed_period
        self.last_update = 0
        self.name = time.time() if not name else name
        self.tb = TensorBoard(
            log_dir=f'./logs/{self.name}',
            histogram_freq=0, batch_size=self.batch_size, write_graph=True, write_grads=False,
            write_images=False, embeddings_freq=0, embeddings_layer_names=None,
            embeddings_metadata=None, embeddings_data=None, update_freq='batch'
        )
        self.model = self._build_model() if not model_path else self.load_model(model_path)
        self.verbose = verbose

    def _build_model(self):
        model = Sequential()
        if not isinstance(self.state_size, int) and len(self.state_size) == 2:
            model.add(Reshape((16, 16, 1), input_shape=self.state_size))
            model.add(Conv2D(8, (3, 3), activation="relu"))
            model.add(MaxPool2D((4, 4)))
            model.add(Flatten())
            model.add(Dense(8, activation='relu'))
        else:
            model.add(Dense(16, input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.action_size, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        model.summary()
        return model

    def remember(self, state, action):
        next_state = state.copy()
        next_state.doAction(action)
        reward = next_state.reward()
        done = next_state.is_terminal()
        self.memory.append((state, action, reward, next_state, done))

    def learn(self):
        if len(self.memory) >= self.batch_size:
            batch = rd.sample(self.memory, self.batch_size)
            positions = []
            targets = []

            for state, action, reward, state_next, terminal in batch:
                if state != state_next:
                    q_update = reward
                else:
                    q_update = -1

                if not terminal:
                    q_update += self.discount_factor * np.amax(
                        self.model.predict(state_next.tomat())[0]
                    )

                q_values = self.model.predict(state_next.tomat())
                q_values[0][state.listActions().index(action)] = q_update
                positions.append(state_next.tomat())
                targets.append(q_values.tolist()[0])
            print(np.array(positions).shape)
            print(np.array(targets).shape)
            self.model.fit(
                np.array(positions), np.array(targets),
                batch_size=self.batch_size, epochs=self.epochs, verbose=self.verbose,
                callbacks=[self.tb]
            )
            self.updateExplorationRate()

    def maxQ(self, state):
        bestVal = - np.inf
        bestAction = ""
        for newActions in state.listActions():
            tempPos = state.copy()
            tempPos.doAction(newActions)

            q_value = np.max(self.model.predict(self._add_dim(tempPos.tomat())))

            if q_value > bestVal :
                bestVal = q_value
                bestAction = newActions

        return bestVal, bestAction

    def _add_dim(self, mat):
        mat2 = np.zeros((1, *self.state_size))
        mat2[0, :, :] = mat
        return mat2

    def updateState(self, state, learning=True):
        action = self.choose_action(state)
        if learning:
            self.remember(state, action)

            if self.last_update >= self.fixed_period:
                self.learn()
                self.last_update = 0
            else:
                self.last_update += 1

        state.doAction(action)
        return action

    def save_model(self, filename):
        self.model.save(filename)

    def load_model(self, filename):
        self.model.load(filename)

    def __str__(self):
        return ""
