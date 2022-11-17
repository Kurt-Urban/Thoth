import pygame


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
