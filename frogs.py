import pygame
from random import randint

class Frog(pygame.sprite.Sprite):
    def __init__(self,config,screen,id):
        super().__init__()

        self.id      = id
        self.screen  = screen
        self.config  = config
        self.fpath   = self.config['frog_image_fpath']
        self.surface = pygame.image.load(self.fpath).convert_alpha()
        self.rect    = self.surface.get_rect()
        self.mask    = pygame.mask.from_surface(self.surface)
        self.rect.x, self.rect.y = self.init_coords()
        self.min_y   = 0
        self.max_y   = self.config['screen_height'] - self.rect.height
        self.min_x   = 0
        self.max_x   = self.config['screen_width'] - self.rect.width
        self.initial_rect = self.rect
        self.speed   = randint(self.config['frog_min_speed'], self.config['frog_max_speed'])
        self.jump_fx = self.config['frog_jump_sound']
        self.jump_speed   = self.config['frog_jump_speed']

    def init_coords(self):
        x = randint(self.rect.width,self.config['screen_width'] - self.rect.width)
        y = randint(self.config['base_end'], self.config['base_start'] - self.rect.height)
        return x,y
    
    def update(self):
        self.draw()
        self.move()

    def draw(self):
        self.screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and keys[pygame.K_LSHIFT]:
            jump = 2 * self.jump_speed
            if self.rect.y - jump > self.min_y: self.rect.y -= jump
        else:
            jump = self.speed
            if self.rect.y - jump > self.min_y and keys[pygame.K_UP]: self.rect.y -= jump
            if self.rect.y + jump < self.max_y and keys[pygame.K_DOWN]: self.rect.y += jump
            if self.rect.x - jump > self.min_x and keys[pygame.K_LEFT]: self.rect.x -= jump
            if self.rect.x + jump < self.max_x and keys[pygame.K_RIGHT]: self.rect.x += jump    