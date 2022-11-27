import time

import flappy_gym


def init_env():
    step = 0
    episode = 1

    env = flappy_gym.make("FlappyBird", render_mode="human")
    env.reset()
    env.action_space.seed(seed=42)

    while episode < 200:

        action = env.action_space.sample()

        _, _, terminated, _, _ = env.step(action)

        step += 1
        print(f"Episode: {episode}\n" f"Action: {action}\n" f"Step: {step}\n")

        time.sleep(1 / 60)

        if terminated:
            env.reset()
            episode += 1
            step = 0

    env.close()


init_env()
