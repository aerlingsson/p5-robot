from agent import DQN
import tensorflow as tf
import numpy as np
import cv2
from csvSaver import Saver
from hyperparams import HyperParameters


class Trainer:
    def __init__(self, env, state_shape, action_size, params):
        self.state_shape = state_shape
        self.action_size = action_size
        self.params = params
        self.env = env
        self.agent = DQN(state_shape, action_size, self.params)

    def preprocess(self, img: np.array):
        img = img.astype(np.float32)
        img += np.random.normal(0.0, 0.15, self.state_shape).astype(np.float32)
        img = np.clip(img, 0, 255)
        img = np.expand_dims(img, axis=0)
        return img

    def close(self):
        self.env.close()

    def run(self, max_epochs, save_interval, save_path, test_nr, verbosity=True):
        saver = Saver(save_path, test_nr, 'test.h5', save_interval, max_epochs, self.params)

        times = 0
        scores = 0

        for episode in range(max_epochs):
            total_reward = 0

            state = self.env.reset()
            state = self.preprocess(state)

            for time in range(5000):
                action = self.agent.act(state)

                next_state, reward, done, _ = self.env.step(action)

                total_reward += reward

                next_state = self.preprocess(next_state)
                self.agent.remember(state, action, reward, next_state, done)
                state = next_state

                self.agent.replay()

                if done:
                    scores += total_reward
                    times += time
                    break

            if episode % save_interval == 0:
                score_avg = scores / save_interval
                time_avg = times / save_interval
                scores, times = 0, 0
                saver.write_to_file(episode, time_avg, score_avg, self.agent.epsilon, self.agent.memory.size())
                if verbosity:
                    print("episode: {}/{}, time: {}, average scores: {}, e: {:.2}, memory: {} " \
                          .format(episode, max_epochs, time_avg, score_avg, self.agent.epsilon, self.agent.memory.size()))
