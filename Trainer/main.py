import argparse
from hyperparams import HyperParameters
from train import Trainer
from gym_unity.envs import UnityEnv


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    params = HyperParameters(mem_size=args.mem_size, lr=args.lr, eps_decay=args.eps_decay, eps_min=args.eps_min,
                             max_tau=args.max_tau, gamma=args.gamma,
                             priority_percentage=args.priority_percentage, batch_size=args.batch_size)

    env = UnityEnv(args.env_path, worker_id=0, use_visual=True, no_graphics=False, uint8_visual=True)
    trainer = Trainer(env, state_shape=args.state_shape, action_size=args.action_dim, params=params)
    trainer.run(max_epochs=args.max_epochs, save_interval=args.save_interval, save_path=args.save_path, test_nr=0)


def create_arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--env_path',
        default="C:/Users/rasmu/Desktop/ml-agents/notebooks/carenv_speed4/Car",
        help='string value'
    )

    parser.add_argument(
        '--save_path',
        default="DDQN_PER",
        help='string value'
    )

    parser.add_argument(
        '--max_epochs',
        default=3000,
        help='int value, e.g. 1000'
    )

    parser.add_argument(
        '--save_interval',
        default=25,
        help='int value, e.g. 10'
    )

    parser.add_argument(
        '--state_shape',
        default=(80, 80, 3),
        help='e.g. (80, 80, 3)'
    )

    parser.add_argument(
        '--action_dim',
        default=9,
        help='e.g. 9'
    )

    parser.add_argument(
        '--lr',
        default=0.0001,
        help='float value under 1, e.g. 0.003'
    )

    parser.add_argument(
        '--mem_size',
        default=100000,
        help='high inter value, e.g. 10000'
    )

    parser.add_argument(
        '--eps_decay',
        default=0.99995,
        help='float value under 1, e.g. 0.999'
    )

    parser.add_argument(
        '--eps_min',
        default=0.1,
        help='float value under 1, e.g. 0.1'
    )

    parser.add_argument(
        '--max_tau',
        default=100,
        help='int value, e.g. 1000'
    )

    parser.add_argument(
        '--gamma',
        default=0.99,
        help='float value under 1, e.g. 0.99'
    )

    parser.add_argument(
        '--priority_percentage',
        default=0.3,
        help='float value between 0 and 1, e.g. 0.2'
    )

    parser.add_argument(
        '--batch_size',
        default=32,
        help='int value, e.g. 32'
    )

    return parser


if __name__ == '__main__':
    main()

