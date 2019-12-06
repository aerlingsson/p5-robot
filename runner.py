from agent import DQN
import tensorflow as tf
from gym_unity.envs import UnityEnv
import numpy as np
import cv2
from csvSaver import Saver

ENV_PATH = "C:/Users/Simon/Desktop/p5-robot-UnityCar/env/Car"
FILENAME = "DDQN_PER"
TESTNR = "1"


STATE_SHAPE = (80, 80, 3)
ACTION_SIZE = 9
N_EPISODES = 5000
BATCH_SIZE = 32
VERBOSITY_STEP = 25
PRIORITY = 0.7


def preprocess(img):
    img = img.astype(np.float32)
    img += np.random.normal(0.0, 0.15, STATE_SHAPE).astype(np.float32)
    img = np.clip(img, 0, 255)
    img = np.expand_dims(img, axis=0)
    return img


def main():
    # Name of the Unity environment binary to launch
    env = UnityEnv(ENV_PATH, worker_id=0, use_visual=True, no_graphics=False, uint8_visual=True)
    agent = DQN(STATE_SHAPE, ACTION_SIZE, eps_decay=0.99996, eps_min=0.2, max_tau=1000, lr=0.003)
    saver = Saver(FILENAME, TESTNR, 'test.h5', VERBOSITY_STEP, N_EPISODES, 0, agent.lr, agent.epsilon_decay, agent.epsilon_min, agent.max_tau)

    scores = []
    times = []

    for episode in range(N_EPISODES):
        total_reward = 0

        state = env.reset()
        state = preprocess(state)

        for time in range(5000):
            action = agent.act(state)

            next_state, reward, done, _ = env.step(action)

            total_reward += reward

            next_state = preprocess(next_state)
            if time >= 10:
                agent.remember(state, action, reward, next_state, done)
            state = next_state

            if agent.memory.size() > BATCH_SIZE:
                agent.replay(BATCH_SIZE, PRIORITY)

            if done:
                break

        scores.append(total_reward)
        times.append(time)
        if episode % VERBOSITY_STEP == 0:
            score_avg = sum(scores) / VERBOSITY_STEP
            time_avg = sum(times) / VERBOSITY_STEP
            scores = []
            times = []
            saver.write_to_file(episode, time_avg, score_avg, agent.epsilon, agent.memory.size())
            print("episode: {}/{}, time: {}, average scores: {}, e: {:.2}, memory: {} " \
                  .format(episode, N_EPISODES, time_avg, score_avg, agent.epsilon, agent.memory.size()))


main()