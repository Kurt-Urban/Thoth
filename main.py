import time
import random
import numpy as np
import flappy_gym

from gymnasium.utils.env_checker import check_env


def init_env():
    step = 0
    episode = 1
    seed = 42
    flaps = 0
    total_reward = 0
    exploration_total = 0

    alpha = 0.9
    gamma = 0.8
    epsilon = 0.1

    env = flappy_gym.make("FlappyBird", render_mode="human")
    state, _ = env.reset(seed=seed)
    env.action_space.seed(seed=seed)

    state_size = 1999999999
    action_size = env.action_space.n

    # q_table = np.loadtxt("q_table.txt", dtype=int, unpack=True)

    q_table = np.zeros([state_size, action_size])

    check_env(env)

    max_episodes = 20
    while episode <= max_episodes:
        if type(state) == np.ndarray:
            state = (state[0] * 1000000) + (state[1] * 1000) + state[2]

        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
            exploration_total += 1
        else:
            action = np.argmax(q_table[state])

        next_state, reward, terminated, _, _ = env.step(action)

        if type(next_state) == np.ndarray:
            next_state = (
                (next_state[0] * 1000000) + (next_state[1] * 1000) + next_state[2]
            )

        old_value = q_table[state][action]
        next_max = np.max(q_table[next_state])

        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # q_table[state][action] = new_value

        q_table[state][action] = old_value + alpha * (
            reward + gamma * np.max(next_max) - q_table[state][action]
        )

        state = next_state

        if action == 1:
            flaps += 1
        step += 1
        total_reward += reward

        time.sleep(1 / 70)

        if terminated:
            env.reset(seed=seed)
            print(
                f"Episode: {episode}, Reward: {total_reward}\n"
                f"Steps: {step}\n"
                f"Flaps: {flaps}\n"
                f"No Action: {step - flaps}\n"
                f"Exploration: {exploration_total}\n"
            )
            episode += 1
            step = 0
            flaps = 0
            total_reward = 0
            exploration_total = 0

    # np.save("q_table.txt", q_table, fmt="%d")

    env.close()


init_env()
