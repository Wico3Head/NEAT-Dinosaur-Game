from msilib.schema import Class
import pygame, random

class Obstacle(pygame.sprite.Sprite):
    small_obs1 = pygame.transform.rotozoom(pygame.image.load('graphics/obs/small_obs1.png'), 0, 0.6)
    small_obs2 = pygame.transform.rotozoom( pygame.image.load('graphics/obs/small_obs2.png'), 0, 0.6)
    small_obs3 = pygame.transform.rotozoom(pygame.image.load('graphics/obs/small_obs3.png'), 0, 0.6)
    big_obs1 = pygame.transform.rotozoom(pygame.image.load('graphics/obs/big_obs1.png'), 0, 0.6)
    big_obs2 = pygame.transform.rotozoom(pygame.image.load('graphics/obs/big_obs2.png'), 0, 0.6)
    big_obs3 = pygame.transform.rotozoom(pygame.image.load('graphics/obs/big_obs3.png'), 0, 0.6)
    bird1 = pygame.transform.rotozoom(pygame.image.load('graphics/bird/bird1.png'), 0, 0.6)
    bird2 = pygame.transform.rotozoom(pygame.image.load('graphics/bird/bird2.png'), 0, 0.6)

    small_obs = [small_obs1, small_obs2, small_obs3]
    big_obs = [big_obs1, big_obs2, big_obs3]

    def __init__(self, type):
        super().__init__()
        self.type = type

        if self.type == 'bird':
            self.animation = [self.bird1, self.bird2]
            self.frame = 0
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect(bottomleft=(1000, random.choice((250, 285, 320))))
        elif self.type == 'small_obs':
            self.size = random.randint(1, 3)
            self.image = self.small_obs[self.size-1]
            self.rect = self.image.get_rect(bottomleft=(1000, 328))
        elif self.type == 'big_obs':
            self.size = random.randint(1, 3)
            self.image = self.big_obs[self.size-1]
            self.rect = self.image.get_rect(bottomleft=(1000, 328))

    def animate(self):
        self.frame += 0.07
        if self.frame >= 2:
            self.frame = 0
        self.image = self.animation[int(self.frame)]

    def update(self):
        self.rect.x -= 8
        if self.type == 'bird':
            self.animate()
        if self.rect.right <= 0:
            self.kill()