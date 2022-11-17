import pygame
from pygame.locals import *
from bird import Bird
from pipe import Pipe
from button import Button
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 880
screen_height = 604

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Flappy Bird")

# Images
bg = pygame.image.load("imgs/flappy_bg.png")
ground = pygame.image.load("imgs/ground.png")
ground_img = pygame.transform.scale(ground, (940, 112))

font = pygame.font.SysFont("Bauhaus 93", 40)
white = (255, 255, 255)

# Game Vars
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 80
pipe_frequency = 1250
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, screen_height / 2)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, "imgs/restart.png")

bird_group.add(flappy)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


running = True
while running:

    clock.tick(fps)

    # Draw the background
    screen.blit(bg, (0, 0))

    # Draw the bird
    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    if flappy.rect.bottom >= 504:
        flying = False
        game_over = True

    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground_img, (ground_scroll, 500))

    if len(pipe_group) > 0:
        if (
            bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
            and pass_pipe == False
        ):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if (
        pygame.sprite.groupcollide(
            bird_group,
            pipe_group,
            False,
            False,
        )
        or flappy.rect.top <= -2
    ):
        game_over = True

    if game_over == False and flying == True:

        pipe_group.update(scroll_speed)

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = [150, 200, 250, 300, 350]
            btm_pipe = Pipe(screen_width, random.choice(pipe_height), -1, pipe_gap)
            top_pipe = Pipe(screen_width, btm_pipe.rect.top - pipe_gap, 1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 60:
            ground_scroll = 0

    if game_over == True:
        if button.draw(screen) == True:
            pipe_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = screen_height / 2
            score = 0
            game_over = False
            flying = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and flying == False
            and game_over == False
        ):
            flying = True

    pygame.display.update()


pygame.quit()
