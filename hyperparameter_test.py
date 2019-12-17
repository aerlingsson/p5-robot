from hyperparams import HyperParameters
from train import Trainer
from gym_unity.envs import UnityEnv


ENV_PATH = "C:/Users/rasmu/Desktop/ml-agents/notebooks/carenv_speed4/Car"
STATE_SHAPE = (80, 80, 3)
ACTION_SIZE = 9

MAX_EPOCHS = 3000
SAVE_INTERVAL = 25

SAVE_PATH = 'TESTS'

DEFAULT_LR = 0.0001
DEFAULT_DECAY = 0.99995
DEFAULT_MIN = 0.1
DEFAULT_TAU = 1000
DEFAULT_PRIO = 0.3

GAMMA = 0.99
BATCH_SIZE = 32
MEM_SIZE = 100000


if __name__ == '__main__':

    tests = {'lr': [0.001, 0.0001, 0.00001],
                'eps_decay': [0.999, 0.9999, 0.99999],
                'eps_min': [0.2, 0.1, 0.01],
                'max_tau': [100, 1000, 10000],
                'priority_percentage': [0.0, 0.2, 0.4, 0.6],
             }

    test_nr = 0

    for param, options in tests.items():

        for option in options:
            params = HyperParameters(mem_size=MEM_SIZE, lr=DEFAULT_LR, eps_decay=DEFAULT_DECAY, eps_min=DEFAULT_MIN,
                                 max_tau=DEFAULT_TAU, gamma=GAMMA, priority_percentage=DEFAULT_PRIO, batch_size=BATCH_SIZE)

            params.__setattr__(param, option)
            print(f'Test: {test_nr} with {param} = {option}')

            env = UnityEnv(ENV_PATH, worker_id=0, use_visual=True, no_graphics=False, uint8_visual=True)
            trainer = Trainer(env, STATE_SHAPE, ACTION_SIZE, params)
            trainer.run(MAX_EPOCHS, SAVE_INTERVAL, SAVE_PATH, test_nr=test_nr)
            trainer.close()

            del trainer

            test_nr += 1
