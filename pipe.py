import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, gap):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/pipe.png")
        self.image = pygame.transform.scale(self.image, (60, 400))
        self.rect = self.image.get_rect()
        self.position = position

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - gap]
        if position == -1:
            self.rect.topleft = [x, y + gap]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
