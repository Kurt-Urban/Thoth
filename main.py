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
    total_scoring_agents = 0
    last_score = 0
    best_agent = {"high_score": 0, "agent": 0}

    alpha = 0.2
    gamma = 0.6
    epsilon_base = 0.01
    epsilon = epsilon_base

    env = flappy_gym.make("FlappyBird", render_mode="human")
    state, _ = env.reset(seed=seed)
    env.action_space.seed(seed=seed)
    check_env(env)

    state_size = env.observation_space.n
    action_size = env.action_space.n

    q_table = np.load("a2g6e01.npy")
    # q_table = np.zeros((state_size, action_size))

    max_episodes = 50
    while episode <= max_episodes:

        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
            epsilon *= 0.8
        else:
            action = np.argmax(q_table[state])

        next_state, reward, terminated, _, info = env.step(action)

        if info["score"] > last_score:
            last_score = info["score"]
            reward += 5

        old_value = q_table[state, action]
        old_state = state
        next_max = np.max(q_table[next_state])

        if step < 50 and next_state < 17:
            next_state = 17

        # Alternate way to calculate new_value
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)

        # new_value = old_value + alpha * (reward + gamma * next_max - old_value)

        if step < 100 and not terminated:
            new_value = 0

        q_table[state, action] = new_value

        state = next_state

        if action == 1:
            flaps += 1
        step += 1
        total_reward += reward

        time.sleep(1 / 70)

        if step >= 10000:
            terminated = True

        if terminated:
            if info["score"] > best_agent["high_score"]:
                best_agent["high_score"] = info["score"]
                best_agent["agent"] = episode

            env.reset(seed=seed)
            print(
                f"Episode: {episode}, Reward: {total_reward + 10}\n"
                f"Steps: {step}\n"
                f"Flaps: {flaps}\n"
                f"Score: {info['score']}\n"
                f"Epsilon: {epsilon}\n"
                f"QTable[{old_state}]: {q_table[old_state]}\n"
            )

            if info["score"] > 0:
                total_scoring_agents += 1
            episode += 1
            step = 0
            flaps = 0
            total_reward = 0
            last_score = 0
            epsilon = epsilon_base

    print("Best agent:", best_agent)

    # TODO: Write exception to exit early but still save progress
    np.save("a2g6e01.npy", q_table)

    print(f"Total Scoring Agents: {total_scoring_agents}\n")

    print(q_table)

    env.close()


init_env()
