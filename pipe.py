import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, gap):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/pipe.png")
        self.image = pygame.transform.scale(self.image, (60, 400))
        self.rect = self.image.get_rect()
        self.position = position
        self.left_corner = 0

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - gap]
            self.left_corner = self.rect.bottomleft
        if position == -1:
            self.rect.topleft = [x, y + gap]
            self.left_corner = self.rect.topleft

    def update(self, scroll_speed):
        if self.position == 1:
            self.left_corner = self.rect.bottomleft
        if self.position == -1:
            self.left_corner = self.rect.topleft

        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
