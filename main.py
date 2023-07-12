import sys
import pygame
from states.menu import Menu
from states.gameplay import Gameplay
from states.game_over import GameOver
from states.splash import Splash
from states.login import Login
from game import Game
from utils import BasePlayer

pygame.init()
screen = pygame.display.set_mode((1280,960))
states = {
    "MENU": Menu(),
    "LOGIN": Login(),
    "SPLASH": Splash(),
    "GAMEPLAY": Gameplay(),
    "GAME_OVER": GameOver(),
}

config_file = 'game_config.yaml'
config = BasePlayer(config_file)

game = Game(screen,config, states, "SPLASH")
game.run()
pygame.quit()
sys.exit()
