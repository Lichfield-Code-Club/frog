import pygame
from frogs import Frog
from cars import Car
from logs import Log
from backgrounds import Background
from utils import GameOver, ReadConfig, car_hit, log_miss, GameWon, GameIntro
from status import StatusUpdate

def InitGame(config):
    pygame.display.set_caption(config['game_title'])

    game = {
            'backgrounds': pygame.sprite.Group(),
            'frogs': pygame.sprite.Group(),
            'cars': pygame.sprite.Group(),
            'logs': pygame.sprite.Group(),
            'screen':  pygame.display.set_mode((config['screen_width'],config['screen_height'])),
            'clock':   pygame.time.Clock(),
            'large_text': pygame.font.SysFont(config['large_text_font'],config['large_text_size']),
            'small_text': pygame.font.SysFont(config['small_text_font'],config['small_text_size'])
             }
    
    [game['backgrounds'].add(Background(config,game['screen'],id)) for id in range(config['num_backgrounds'])]
    [game['frogs'].add(Frog(config,game['screen'],id)) for id in range(config['num_frogs'])]
    [game['cars'].add(Car(config,game['screen'],id)) for id in range(config['num_cars'])]
    [game['logs'].add(Log(config,game['screen'],id)) for id in range(config['num_logs'])]

    return game

def GameUpdate(config,game):
    game['backgrounds'].update()
    game['cars'].update()
    game['logs'].update()
    StatusUpdate(config,game)
    game['frogs'].update()

def PlayGame(config,game):
    game_paused = True
    game_over = False
    game_won = False
    run = True
    while run:
        game['clock'].tick(config['frame_rate'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            game_paused = False
        if keys[pygame.K_RETURN]: 
            game = InitGame(config)
            game_over = False
        if keys[pygame.K_ESCAPE]: run = False

        if game_paused:
            GameIntro(game)
        elif game_won:
            print('Winner')
        elif game_over:
            GameOver(game)
        else:
            GameUpdate(config,game)
            game_over = car_hit(config,game['frogs'], game['cars'])
            if not game_over:
                game_over = log_miss(config,game['frogs'],game['logs'])
            if not game_over:
                game_won = GameWon(game['frogs'])

        pygame.display.update()

def main(config):
    game = InitGame(config)
    PlayGame(config,game)

if __name__ == '__main__':
    config_file = 'game_config.yaml'
    config = ReadConfig(config_file)
    pygame.init()
    main(config)
    pygame.quit()
    exit() 
