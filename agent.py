import tensorflow as tf
import tensorflow.keras
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json, load_model
import random
import numpy as np
from collections import deque
import os
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, Lambda, Input

from hyperparams import HyperParameters
from memory import Memory


class DQN:
    def __init__(self, state_shape: tuple, action_size: int, params: HyperParameters):
        self.state_shape = state_shape
        self.action_size = action_size
        self.params = params
        
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

        self.memory = Memory(priority_percentage=params.priority_percentage)

        self.epsilon = 1.0
        self.tau = 0
    
    def build_model(self):
        
        '''
        encoder = load_model('enc.h5')
        encoder.trainable = False

        inp = Input(shape=self.state_shape)
        lamb1 = Lambda(lambda x: tf.image.rgb_to_grayscale(x))(inp)
        lamb2 = Lambda(lambda x: x / 255)(lamb1)
        enc = encoder(lamb2)
        flatten = Flatten()(enc)
        drp1 = Dropout(0.3)(flatten)
        dense1 = Dense(100, activation='relu')(drp1)
        drp2 = Dropout(0.3)(dense1)
        dense2 = Dense(50, activation='relu')(drp2)
        drp3 = Dropout(0.2)(dense2)
        dense3 = Dense(self.action_size, activation='linear')(drp3)

        model = Model(inputs=inp, outputs=dense3)

        '''

        model = Sequential([
            Input(shape=self.state_shape),
            Lambda(lambda x: tf.image.rgb_to_grayscale(x)),
            Lambda(lambda x: x/255),
            Conv2D(24, (5,5), strides=(2,2), activation='relu'),
            Conv2D(36, (5,5), strides=(2,2), activation='relu'),
            Conv2D(48, (5,5), strides=(2,2), activation='relu'),
            Conv2D(64, (3,3), strides=(1,1), activation='relu'),
            Flatten(),
            Dropout(0.3),
            Dense(100, activation='relu'),
            Dropout(0.3),
            Dense(50, activation='relu'),
            Dropout(0.2),
            Dense(self.action_size, activation='linear')
        ])

        model.compile(loss='mse', optimizer=Adam(lr=self.params.lr))
        return model

    def act(self, state: np.array):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        action = self.model.predict(state)
        return np.argmax(action[0])
    
    def replay(self):
        if self.memory.size() < self.params.batch_size:
            return

        states, actions, rewards, next_states, dones = self.memory.get_distributed_batch(self.params.batch_size)

        stacked_states = np.vstack(states)
        stacked_next_states = np.vstack(next_states)

        predictions, target_predictions = self.get_predictions(stacked_states, stacked_next_states)
        predictions, errors = self.update_predictions(actions, rewards, dones, predictions, target_predictions)

        self.model.fit(stacked_states, predictions, epochs=1, verbose=0)

        predictions, target_predictions = self.get_predictions(stacked_states, stacked_next_states)
        _, errors = self.update_predictions(actions, rewards, dones, predictions, target_predictions)

        batch = (states, actions, rewards, next_states, dones)
        self.memory.append_batch(batch, errors)

        if self.tau >= self.params.max_tau:
            self.update_target_model()
            self.tau = 0
        self.tau += 1
            
        if self.epsilon > self.params.eps_min:
            self.epsilon *= self.params.eps_decay

    def get_predictions(self, states: np.array, next_states: np.array):
        predictions = self.model.predict(states)
        target_predictions = self.target_model.predict(next_states)
        return predictions, target_predictions

    def update_predictions(self, actions, rewards, dones, predictions, target_predictions):
        errors = []
        for index, (action, reward, done) in enumerate(zip(actions, rewards, dones)):
            if not done:
                max_future_q = np.amax(target_predictions[index])
                new_q = reward + self.params.gamma * max_future_q
            else:
                new_q = reward
            old_q = predictions[index][action]
            error = np.abs(old_q - new_q)
            errors.append(error)
            predictions[index][action] = new_q

        return predictions, errors

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def load(self, name):
        self.model.load_weights(name)
        self.update_target_model()

    def save(self, name):
        self.model.save_weights(name)
