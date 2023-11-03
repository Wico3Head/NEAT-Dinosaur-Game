import pygame, random

class Background(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.image.load('graphics/background.png')
        self.rect = self.image.get_rect(topleft=(position, 0))

    def update(self):
        self.rect.x -= 8
        if self.rect.right <= 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    cloud_coord = []
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/cloud.png'), 0, 0.7)
        self.rect = self.image.get_rect()
        if self.mode == 1:
            self.cloud_coord = []
            self.rect.topleft = (1000, random.randint(50, 120))
        else:
            x = random.randint(50, 950)
            y = random.randint(50, 120)
            self.cloud_coord.append((x, y))
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 1
        if self.rect.right <= 0:
            self.kill()