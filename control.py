import pygame
from random import randint

class Control(pygame.sprite.Sprite):
    def __init__(self,screen,btn):
        super().__init__()

        self.screen   = screen
        self.name     = btn['name']
        self.image    = btn['image']
        self.x        = btn['x']
        self.y        = btn['y']
        self.btn      = pygame.image.load(self.image).convert_alpha()
        self.img_rect = self.btn.get_rect()
        self.img_rect.x = self.x
        self.img_rect.y = self.y
        self.clicked = False
        self.action  = False

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.img_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        self.screen.blit(self.btn, (self.img_rect.x, self.img_rect.y))
