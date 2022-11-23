import gymnasium as gym
from gymnasium import spaces
import numpy as np

from flappy_gym.base_game import Game


class FlappyBirdEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode="human"):
        self.window_size = (880, 604)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(3,), dtype=np.float64
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
        self.game = None

    def _get_obs(self):
        player = self.game.flappy
        player_height = float(500 - player.rect.bottom)

        dist_top_pipe = float(self.game.dist_top_pipe)
        dist_btm_pipe = float(self.game.dist_btm_pipe)
        return np.array([dist_top_pipe, dist_btm_pipe, player_height])

    def step(self, action):
        obs = self._get_obs()
        print(obs)

        alive = self.game.update(action)

        reward = 1
        terminated = alive
        info = {"score": self.game.score}

        return obs, reward, terminated, False, info

    def reset(self):
        self.game = Game()

        if self.game.game_over:
            self.game.reset()

        observation = self._get_obs()
        info = {"score": self.game.score}

        return observation, info

    def render(self, mode="human"):
        if mode == "human":
            self.game.game_logic()
        elif mode == "rgb_array":
            return self.game.game_logic()
