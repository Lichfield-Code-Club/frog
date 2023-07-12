import pygame
from random import randint

class Car(pygame.sprite.Sprite):
    def __init__(self,config,screen,id):
        super().__init__()

        self.id = id
        self.screen  = screen
        self.config = config
        self.fpath = self.config['car_image_fpath']
        self.surface = pygame.image.load(self.fpath).convert_alpha()
        self.rect    = self.surface.get_rect()
        self.mask    = pygame.mask.from_surface(self.surface)
        self.max_x   = self.config['screen_width']
        self.min_y   = self.config['road_end']
        self.max_y   = self.config['road_start']
        self.max_speed = self.config['car_max_speed']
        self.min_speed = self.config['car_min_speed']
        self.speed   = randint(self.min_speed, self.max_speed)
        self.rect.x, self.rect.y = self.init_coords()
        self.initial_rect = self.rect
        self.crashed = False
        self.crash_fpath = self.config['car_crash_fpath']
        self.crash_surface = pygame.image.load(self.crash_fpath).convert_alpha()
        self.crash_rect = self.crash_surface.get_rect()
        self.crash_fx = pygame.mixer.Sound(self.config['car_crash_sound'])
        self.crash_fx.set_volume(config['car_crash_volume'])

    def init_coords(self):
        x = randint(0,self.max_x)
        y = randint(self.min_y, self.max_y - self.rect.width)
        return x,y

    def update(self):
        self.draw()
        self.move()

    def draw(self):
        if self.crashed: 
            self.screen.blit(self.crash_surface,(self.crash_rect.x, self.crash_rect.y))
        else: 
            self.screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self):
        self.rect.x -= self.speed
        #self.rect  = boundary_checks(self.rect,self.initial_rect)

