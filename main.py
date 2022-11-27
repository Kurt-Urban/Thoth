import time

import numpy as np
import flappy_gym

from gymnasium.utils.env_checker import check_env


def init_env():
    step = 0
    episode = 1
    seed = 42
    flaps = 0

    env = flappy_gym.make("FlappyBird", render_mode="human")
    env.action_space.seed(seed=seed)

    state = env.reset(seed=seed)
    new_state = (0.7486497533073, 0.7486497533073, 166.7486497533073)

    state_size = 3
    action_size = 2

    learning_rate = 0.9
    discount_rate = 0.8

    qtable = np.zeros((state_size, action_size))

    check_env(env)

    while episode < 200:

        action = np.argmax(qtable[state, :])

        # Qlearning algorithm: Q(s,a) := Q(s,a) + learning_rate * (reward + discount_rate * max Q(s',a') - Q(s,a))
        qtable[state, action] += learning_rate * (
            reward
            + discount_rate * np.max(qtable[new_state, :])
            - qtable[state, action]
        )

        if action == 1:
            flaps += 1

        obs, reward, terminated, _, _ = env.step(action)
        new_state = obs
        step += 1
        # print(
        #     f"Episode: {episode}\n"
        #     f"Obs: {int(obs[0])} {int(obs[1])} {int(obs[2])}\n"
        #     f"Action: {action}\n"
        #     f"Step: {step}\n"
        # )

        time.sleep(1 / 60)

        if terminated:
            env.reset(seed=seed)
            print(
                f"Episode: {episode}\n"
                f"Steps: {step}\n"
                f"Flaps: {flaps}\n"
                f"No Action: {step - flaps}\n"
            )
            episode += 1
            step = 0
            flaps = 0

    env.close()


init_env()
