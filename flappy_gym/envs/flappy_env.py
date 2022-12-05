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
        self.observation_space = spaces.Discrete(49, start=0)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
        self.game = Game()

    def _get_obs(self):
        player = self.game.flappy
        player_height = int((500 - player.rect.bottom) / 100)

        btm_pipe_height = int(self.game.btm_pipe_height / 100)
        rel_player_height = player_height - btm_pipe_height

        dist_btm_pipe = int(self.game.dist_btm_pipe / 100)

        obs = (rel_player_height * 10) + dist_btm_pipe
        return obs

    def step(self, action):
        self.game.game_logic(action)

        obs = self._get_obs()

        terminated = self.game.game_over

        reward = 1

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
