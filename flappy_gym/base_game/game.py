import pygame
from pygame.locals import *
from .bird import Bird
from .pipe import Pipe
from .button import Button
import random


class Game:
    def __init__(self):
        pygame.init()

        # Initialise game window
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen_width = 880
        self.screen_height = 604
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        pygame.display.set_caption("Flappy Bird")

        # Images
        self.bg = pygame.image.load("imgs/flappy_bg.png")
        ground = pygame.image.load("imgs/ground.png")
        self.ground_img = pygame.transform.scale(ground, (940, 112))
        self.font = pygame.font.SysFont("Bauhaus 93", 40)
        self.white = (255, 255, 255)

        # Game Vars
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.flying = True
        self.game_over = False
        self.pipe_gap = 80
        self.pipe_frequency = 1250
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
        self.score = 0
        self.pass_pipe = False
        self.dist_top_pipe = 0
        self.dist_btm_pipe = 0

        # Initialise groups
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.flappy = Bird(100, self.screen_height / 2)
        self.bird_group.add(self.flappy)
        self.button = Button(
            self.screen_width // 2 - 50,
            self.screen_height // 2 - 100,
            "imgs/restart.png",
        )

    def reset(self):
        self.pipe_group.empty()
        self.flappy.rect.x = 100
        self.flappy.rect.y = self.screen_height / 2
        self.score = 0
        self.game_over = False
        self.flying = True

    def draw_text(self, text, text_col, x, y):
        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def game_logic(self, action):

        self.clock.tick(self.fps)

        # Draw the background
        self.screen.blit(self.bg, (0, 0))

        # Draw the bird
        self.bird_group.draw(self.screen)
        self.bird_group.update(self.flying, self.game_over, action)
        if self.flappy.rect.bottom >= 504:
            self.flying = False
            self.game_over = True

        self.pipe_group.draw(self.screen)

        # Draw the ground
        self.screen.blit(self.ground_img, (self.ground_scroll, 500))

        if len(self.pipe_group) > 0:
            # Set the distance to the next pipe
            pipe_top_left = self.pipe_group.sprites()[0].rect.topleft
            self.dist_btm_pipe = pygame.math.Vector2(pipe_top_left).distance_to(
                self.flappy.rect.center
            )
            pipe_bottom_left = self.pipe_group.sprites()[1].rect.bottomleft
            self.dist_top_pipe = pygame.math.Vector2(pipe_bottom_left).distance_to(
                self.flappy.rect.center
            )
            # Check if the bird has passed the pipe
            if (
                self.bird_group.sprites()[0].rect.left
                > self.pipe_group.sprites()[0].rect.left
                and self.bird_group.sprites()[0].rect.right
                < self.pipe_group.sprites()[0].rect.right
                and self.pass_pipe == False
            ):
                self.pass_pipe = True
            if self.pass_pipe == True:
                if (
                    self.bird_group.sprites()[0].rect.left
                    > self.pipe_group.sprites()[0].rect.right
                ):
                    self.score += 1
                    self.pass_pipe = False

        self.draw_text(str(self.score), self.white, int(self.screen_width / 2), 20)

        # Checks if the bird has collided with a pipe
        if (
            pygame.sprite.groupcollide(
                self.bird_group,
                self.pipe_group,
                False,
                False,
            )
            or self.flappy.rect.top <= -2
        ):
            self.game_over = True

        if self.game_over == False and self.flying == True:
            self.pipe_group.update(self.scroll_speed)
            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe > self.pipe_frequency:
                pipe_height = [150, 200, 250, 300, 350]
                btm_pipe = Pipe(
                    self.screen_width, random.choice(pipe_height), -1, self.pipe_gap
                )
                top_pipe = Pipe(
                    self.screen_width,
                    btm_pipe.rect.top - self.pipe_gap,
                    1,
                    self.pipe_gap,
                )
                self.pipe_group.add(btm_pipe)
                self.pipe_group.add(top_pipe)
                self.last_pipe = time_now

            self.ground_scroll -= self.scroll_speed
            if abs(self.ground_scroll) > 60:
                self.ground_scroll = 0

        if self.game_over == True:
            if self.button.draw(self.screen) == True:
                self.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and self.flying == False
                and self.game_over == False
            ):
                self.flying = True

        pygame.display.update()


# flappy_bird = Game()
# flappy_bird.game_logic()
