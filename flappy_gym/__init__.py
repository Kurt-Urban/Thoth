from gymnasium.envs.registration import register

from .envs.flappy_env import FlappyBirdEnv

from gymnasium import make

register(
    id="FlappyBird",
    entry_point="flappy_gym.envs:FlappyBirdEnv",
)

__all__ = [
    make.__name__,
    FlappyBirdEnv.__name__,
]
