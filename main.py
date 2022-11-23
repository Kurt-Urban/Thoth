import time

import flappy_gym


def init_env():
    env = flappy_gym.make("FlappyBird")
    env.reset()
    score = 0

    while True:
        env.render()

        action = env.action_space.sample()

        if env.game.flying == False and env.game.game_over == False:
            action = 1

        obs, reward, terminated, _, _ = env.step(action)

        score += reward
        print(f"Obs: {obs}\n" f"Action: {action}\n" f"Score: {score}\n")

        time.sleep(1 / 30)

        if terminated:
            env.render()
            time.sleep(0.5)
            break


init_env()
