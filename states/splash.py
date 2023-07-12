import pygame
from .base import BaseState
from random import randint


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.title = self.font.render(self.config['game_title'], True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "LOGIN"
        self.time_active = 0
        self.bg_img = pygame.image.load(self.config['background_image_fpath']).convert_alpha()
        self.bg_rect = self.bg_img.get_rect()
        self.frog_img = pygame.image.load(self.config['frog_image_fpath']).convert_alpha()
        self.frog_rect = self.frog_img.get_rect()

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 5000:
            self.done = True

    def draw(self, surface):
        surface.blit(self.bg_img,self.bg_rect)
        if self.time_active % 50 == 0:
            self.frog_rect.x = randint(100,1280)
            self.frog_rect.y = randint(100,900)
        self.title_rect.x = self.frog_rect.x 
        self.title_rect.y = self.frog_rect.y + self.title_rect.height + 30
        surface.blit(self.frog_img,self.frog_rect)
        surface.blit(self.title, self.title_rect)

