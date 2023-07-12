import pygame
from .base import BaseState
from utils import SavePlayer

class GameOver(BaseState):
    def __init__(self):
        super(GameOver, self).__init__()
        self.title = self.font.render("Game Over", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("Press space to start again, or enter to go to the menu", True, pygame.Color("white"))
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] +  50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
            SavePlayer(self.config)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.next_state = "MENU"
                self.done = True
                player = self.config['player']
                #print('Game Over: Menu Before ',player)
                SavePlayer(self.config)
                player = self.config['player']
                #print('Game Over: Menu After ',player)
            elif event.key == pygame.K_SPACE:
                self.next_state = "GAMEPLAY"
                self.done = True
                SavePlayer(self.config)
            elif event.key == pygame.K_ESCAPE:
                self.quit = True
                SavePlayer(self.config)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)
