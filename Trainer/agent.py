import random
import numpy as np
from tensorflow.keras.optimizers import Adam
from model import build_model
from hyperparams import HyperParameters
from memory import Memory


class DQN:
    def __init__(self, state_shape: tuple, action_size: int, params: HyperParameters):
        self.state_shape = state_shape
        self.action_size = action_size
        self.params = params
        
        self.model = build_model(state_shape, action_size)
        self.model.compile(loss='mse', optimizer=Adam(lr=self.params.lr))
        self.target_model = build_model(state_shape, action_size)
        self.update_target_model()

        self.memory = Memory(max_size=params.mem_size, priority_percentage=params.priority_percentage)

        self.epsilon = 1.0
        self.tau = 0

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
