import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/bird.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.y_value = y

    def update(self, flying, game_over, action):
        self.y_value = self.rect.y

        img = pygame.transform.scale(pygame.image.load("imgs/bird.png"), (40, 40))

        if flying == True:
            # Gravity
            if flying == True:
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 504:
                    self.rect.y += int(self.vel)
        if game_over == False:
            # Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10

            if pygame.mouse.get_pressed()[0] == 0 or action == 0:
                self.clicked = False

            if action == 1:
                self.vel = -10

            # Rotate
            self.image = pygame.transform.rotate(img, self.vel * -2)
        else:
            self.image = pygame.transform.rotate(img, -90)
