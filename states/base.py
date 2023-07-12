import pygame
from utils import BasePlayer, GameAssets
from frogs import Frog
from cars import Car
from logs import Log
from backgrounds import Background

class BaseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)
        self.config = None
        self.assets = None
        self.game_init()

    def startup(self, persistent):
        self.persist = persistent

    def game_init(self):
        if self.config == None:
            self.config = BasePlayer('game_config.yaml')
        if self.assets == None:
            self.assets = GameAssets(self.config)

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

