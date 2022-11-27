import time

import flappy_gym

from gymnasium.utils.env_checker import check_env


def init_env():
    step = 0
    episode = 1
    seed = 42

    env = flappy_gym.make("FlappyBird", render_mode="human")
    env.reset(seed=seed)
    env.action_space.seed(seed=seed)

    check_env(env)

    while episode < 2000:

        action = env.action_space.sample()

        _, _, terminated, _, _ = env.step(action)

        step += 1
        print(f"Episode: {episode}\n" f"Action: {action}\n" f"Step: {step}\n")

        time.sleep(1 / 60)

        if terminated:
            env.reset(seed=seed)
            episode += 1
            step = 0

    env.close()


init_env()
