import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_walk1.png'), 0, 0.6).convert_alpha()
        walk2 = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_walk2.png'), 0, 0.6).convert_alpha()
        duck1 = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_duck1.png'), 0, 0.6).convert_alpha()
        duck2 = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_duck2.png'), 0, 0.6).convert_alpha()
        self.jump = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_jump.png'), 0, 0.6).convert_alpha()
        self.dead = pygame.transform.rotozoom(pygame.image.load('graphics/dino/dino_dead.png'), 0, 0.6).convert_alpha()

        self.jump_sound = pygame.mixer.Sound('sound/jump.wav')
        self.dead_sound = pygame.mixer.Sound('sound/die.wav')

        self.walk = [walk1, walk2]
        self.duck = [duck1, duck2]
        self.frame = 0
        self.gravity = 0

        self.image = self.walk[self.frame]
        self.rect = self.image.get_rect(bottomleft=(50, 325))
        self.is_dead = False

    def input_check(self, decision):
        if decision == 0 and self.gravity > 16:
            self.gravity = -13
            self.jump_sound.play()
            self.ducking = False
        if decision == 1:
            if self.rect.bottom >= 325:
                self.ducking = True
            else:
                self.gravity += 1.2
        else:
            self.ducking = False

    def animate(self):
        self.rect.y += self.gravity
        self.gravity += 0.8
        if self.rect.bottom >= 325:
            self.rect.bottom = 325
        
        self.frame += 0.1
        if self.frame >= 2:
            self.frame = 0
        if self.rect.bottom >= 325:
            if not self.ducking:
                self.image = self.walk[int(self.frame)]
                self.rect = self.image.get_rect(bottomleft=(50, 325)) 
            else:
                self.image = self.duck[int(self.frame)]
                self.rect = self.image.get_rect(bottomleft=(50, 325))
        else:
            self.image = self.jump 

    def update(self, decision):
        self.input_check(decision)
        self.animate()