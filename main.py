import pygame
from frogs import Frog
from cars import Car
from logs import Log
from backgrounds import Background
from utils import GameOver, SavePlayer,LoadPlayer, car_hit, log_miss, GameWon, tstamp
from login import login
from control import Control

def InitGame(config):
    pygame.display.set_caption(config['game_title'])

    game = {
            'backgrounds': pygame.sprite.Group(),
            'frogs': pygame.sprite.Group(),
            'cars': pygame.sprite.Group(),
            'logs': pygame.sprite.Group(),
            'controls': pygame.sprite.Group(),
            'buttons': pygame.sprite.Group(),
            'screen':  pygame.display.set_mode((config['screen_width'],config['screen_height'])),
            'clock':   pygame.time.Clock(),
            'large_text': pygame.font.SysFont(config['large_text_font'],config['large_text_size']),
            'small_text': pygame.font.SysFont(config['small_text_font'],config['small_text_size'])
             }
    
    [game['backgrounds'].add(Background(config,game['screen'],id)) for id in range(config['num_backgrounds'])]
    [game['frogs'].add(Frog(config,game['screen'],id)) for id in range(config['num_frogs'])]
    [game['cars'].add(Car(config,game['screen'],id)) for id in range(config['num_cars'])]
    [game['logs'].add(Log(config,game['screen'],id)) for id in range(config['num_logs'])]
    [game['buttons'].add(Control(game['screen'],btn)) for btn in config['buttons'] ]
    return game

def GameUpdate(config,game):
    game['backgrounds'].update()
    game['cars'].update()
    game['logs'].update()
    #StatusUpdate(config,game)
    game['frogs'].update()

def PlayGame(config,game):
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

        if game_won:
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
    player_config = login(config,game)
    start = tstamp()

    if player_config['player']['valid']:
        PlayGame(player_config,game)
        session = {'end': tstamp(), 'start': start, 'score': None}
        player_config['player']['runs'].append(session)
        SavePlayer(player_config)
    else:
        print('Invalid Login')
    return player_config

if __name__ == '__main__':
    config_file = 'game_config.yaml'
    config = LoadPlayer(config_file)
    config['player']['valid'] = False
    pygame.init()
    main(config)
    pygame.quit()
    exit() 
