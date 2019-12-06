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
from memory import Memory


class DQN:
    def __init__(self, state_shape, action_size, lr=0.001, gamma=0.99, eps_decay=0.999, eps_min=0.01, max_tau=50):
        self.state_shape = state_shape
        self.action_size = action_size
        self.lr = lr
        
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()
        self.memory = Memory()
        
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_decay = eps_decay
        self.epsilon_min = eps_min
        self.max_tau = max_tau
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

        model.compile(loss='mse', optimizer=Adam(lr=self.lr))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        action = self.model.predict(state)
        return np.argmax(action[0])
    
    def replay(self, batch_size, priority):
        states, actions, rewards, next_states, dones = self.memory.get_distributed_batch(batch_size, priority)

        stacked_states = np.vstack(states)
        stacked_next_states = np.vstack(next_states)

        predictions, target_predictions = self.get_predictions(stacked_states, stacked_next_states)
        predictions, errors = self.update_predictions(actions, rewards, dones, predictions, target_predictions)

        self.model.fit(stacked_states, predictions, epochs=1, verbose=0) #epochs = batch_size?

        predictions, target_predictions = self.get_predictions(stacked_states, stacked_next_states)
        _, errors = self.update_predictions(actions, rewards, dones, predictions, target_predictions)

        batch = (states, actions, rewards, next_states, dones)
        self.memory.append_batch(batch, errors)

        if self.tau >= self.max_tau:
            self.update_target_model()
            self.tau = 0
        self.tau += 1
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_predictions(self, states, next_states):
        predictions = self.model.predict(states)
        target_predictions = self.target_model.predict(next_states)
        return predictions, target_predictions

    def update_predictions(self, actions, rewards, dones, predictions, target_predictions):
        errors = []
        for index, (action, reward, done) in enumerate(zip(actions, rewards, dones)):
            if not done:
                max_future_q = np.amax(target_predictions[index])
                new_q = reward + self.gamma * max_future_q
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
