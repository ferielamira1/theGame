from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import statistics
import collections


params = dict()
# Neural Network
params['epsilon_decay_linear'] = 1/75
params['learning_rate'] = 0.0005
params['first_layer_size'] = 50   # neurons in the first layer
params['second_layer_size'] = 300   # neurons in the second layer
params['third_layer_size'] = 50    # neurons in the third layer
params['episodes'] = 150
params['memory_size'] = 2500
params['batch_size'] = 1000
# Settings
params['weights_path'] = 'weights/weights3.hdf5'
params['load_weights'] = False
params['train'] = True
params['plot_score'] = True

# In our case player
class DQNAgent(object):
    def __init__(self):
        self.reward = 0
        self.gamma = 0.9 # WHY 0.9
        #self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1 # ?
        self.agent_predict = 0 # ?
        self.learning_rate = params['learning_rate']
        self.epsilon = 1
        self.actual = [] # ?


        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']

        self.memory = collections.deque(maxlen=params['memory_size'])
        self.weights = params['weights_path'] # ?
        self.load_weights = params['load_weights'] # ?
        self.model = self.network()

    def network(self):
        model = Sequential()
        model.add(Dense(self.first_layer, activation='relu'))
        model.add(Dense(self.second_layer, activation='relu'))
        model.add(Dense(self.third_layer, activation='relu'))
        model.add(Dense(4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)
        return model

    def get_state(self,hand, upPile1, upPile2, downPile1, downPile2):
        state = np.zeros((1, len(hand) + 4))
        state[0][:len(hand)] = hand
        state[0][len(hand)] = upPile1
        state[0][len(hand) + 1] = upPile2
        state[0][len(hand) + 2] = downPile1
        state[0][len(hand) + 3] = downPile2
        state= state.flatten()
        return state

    def set_reward(self, played):
        self.reward = 0
        if played:
            self.reward = 1
        if not played:
            self.reward = -1
        return self.reward

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
                target = reward + self.gamma * np.amax(self.model.predict(next_state))
            target_f = self.model.predict(state)
            target_f[0][np.argmax(action)] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state))
        target_f = self.model.predict(state)

        target_f[0][np.argmax(action)] = target

        self.model.fit(state, target_f, epochs=1, verbose=0)
