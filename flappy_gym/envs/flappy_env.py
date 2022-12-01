import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

from flappy_gym.base_game import Game


class FlappyBirdEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode="human"):
        self.window_size = (880, 604)

        self.action_space = spaces.Discrete(2, start=0)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(2,), dtype=np.int64
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
        self.game = Game()

    def _get_obs(self):
        player = self.game.flappy
        player_height = int(500 - player.rect.bottom)

        dist_btm_pipe = int(self.game.dist_btm_pipe)
        return np.array([dist_btm_pipe, player_height])

    def step(self, action):
        self.game.game_logic(action)

        obs = self._get_obs()

        terminated = self.game.game_over

        reward = 0.05

        if int(obs[1]) < 75 or int(obs[1]) > 425:
            reward = -0.5

        if terminated:
            reward = -10

        info = {"score": self.game.score}

        return obs, reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()

        obs = self._get_obs()
        info = {"score": self.game.score}

        return obs, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        return None

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
