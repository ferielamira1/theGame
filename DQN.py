from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import EarlyStopping

import random
import numpy as np
import collections

# In our case player
class DQNAgent(object):
    def __init__(self):
        self.epsilon_decay= 0.995
        self.state_size = 12
        self.action_size = 32
        self.gamma = 0.99 # Adjusting the value of gamma will diminish (bigger gamma) or increase (smaller gamma)the contribution of future rewards.
        self.train = True
        self.short_memory = np.array([])
        self.learning_rate = 0.0001#(lower bound 10^-6)
        self.epsilon = 1
        self.actual = [] # ?
        self.second_layer = 20
        self.memory = collections.deque(maxlen=2000)
        self.weights = 'weights/weights.hdf5'
        self.load_weights = False
        self.model = self.network()
        self.batch_size = 32

    def network(self):
        model = Sequential()

        model.add(Dense(12,input_dim=12, activation='relu',name="layer1")) #Here, the input layer would expect a one-dimensional array with 12 elements for input. It would produce 12 outputs in return.
        model.add(Dense(24 ,activation='tanh',name="layer2"))
        model.add(Dense(self.action_size, activation='softmax',name="layer3"))
        model.compile(loss='mse', optimizer=Adam(self.learning_rate))

        return model


    def encode_state(self,hand,upPiles,downPiles):
        '''
        # Hot encoding of the cards in hand:

        state = np.zeros((102))
        for index in hand:
            if index != -1:
                state[index] = 1

        state[98] = upPiles[0]
        state[99] = upPiles[1]
        state[100] = downPiles[0]
        state[101] = downPiles[1]
        '''

        state = np.zeros(8+4)
        sorted_hand= np.sort(hand)

        state[:8]= sorted_hand

        state[8:10] = upPiles
        state[10:12] = downPiles
        print(state)
        state = state.flatten()
        return state


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][action] = target

            reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2,
                                          patience=5, min_lr=0.001)


            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0,callbacks=[reduce_lr])


    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
           target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 12)))[0])

        target_f = self.model.predict(state.reshape((1,12)))

        target_f[0][action] = target
        print("TARGET_F {}".format(target_f))
        self.model.fit(state.reshape((1, 12)), target_f, epochs=1, verbose=0)
        return




