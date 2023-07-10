# http://www.codingwithruss.com/pygame/getting-multi-line-text-input-in-pygame/
import pygame
import os
from utils import draw_large_text,draw_small_text, draw_medium_text, LoadPlayer

def login(config,game):
    screen = game['screen']
    BG_COLOUR = (60, 114, 228)
    done = False
    btn_clicked = None

    while not config['player']['valid'] and not done:
        screen.fill(BG_COLOUR)
        game['buttons'].update()
        new_config = get_name(config,game)
        if new_config['player']['valid']:
            config = new_config
            played_games(config,game)
        draw_name(config,game)
        pygame.display.flip()
        btn_clicked = login_done(config,game)
        if btn_clicked:
            done = True
    return config
    
def get_name(config,game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.TEXTINPUT:
            if config['player']['name'] == None:
                config['player']['name'] = ''
            if len(config['player']['name']) < config['player']['max_name_len']:
                config['player']['name'] += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                config['player']['name'] = config['player']['name'][:-1]
            #elif event.key == pygame.K_RETURN:
            #    config = valid_login(config)

    for btn in game['buttons']:
        if btn.clicked and btn.action and len(config['player']['name']) > 0:
            config = valid_login(config)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        return

    return config

def draw_name(config,game):
    PROMPT_COLOUR = (246, 247, 246)
    TEXT_COLOUR = (0, 0, 0)
    screen = game['screen']
    name = config['player']['name']
    x = config['player']['name_box_x']
    y = config['player']['name_box_y']
    w = config['player']['name_box_w']
    h = config['player']['name_box_h']
    rect = pygame.Rect(x,y,w,h)

    prompt = 'Name'
    pygame.draw.rect(screen,'white',rect)
    draw_large_text(screen,prompt,PROMPT_COLOUR,x-80,y)
    draw_large_text(screen,name,TEXT_COLOUR,x+80,y)

def valid_login(config):
    player = config['player']['name']
    fpath = f'players/{player}.yaml'
    if os.path.exists(fpath):
        config = LoadPlayer(fpath)
    config['player']['fpath'] = fpath
    config['player']['valid'] = True
    return config

def login_done(config,game):
    for btn in game['buttons']:
        if btn.action:
            if btn.name == 'exit':
                config['player']['valid'] = False
            return btn.name

def played_games(config,game):
    TEXT_COLOUR = (0, 0, 0)
    screen = game['screen']
    x = config['player']['history_box_x']
    y = config['player']['history_box_y']
    w = config['player']['history_box_w']
    h = config['player']['history_box_h']
    rect = pygame.Rect(x,y,w,h)

    pygame.draw.rect(screen,'white',rect)
    n = 0
    runs = config['player']['runs']
    runs.reverse()
    print('fpath', config['player']['fpath'])
    print('type', type(runs))
    print('len runs', len(runs))
    draw_medium_text(screen, 'start end score', TEXT_COLOUR, x + 100, y - 40)
    for run in runs[:5]:
        y_coord = 600 + (n * 30)
        print(n,y_coord,run)
        draw_medium_text(screen,f"{run['start']}",TEXT_COLOUR,x,600 + (n * 30))
        draw_medium_text(screen,f"{run['end']}",TEXT_COLOUR,x+300,600 + (n * 30))
        draw_medium_text(screen,f"{run['score']}",TEXT_COLOUR,x+600,600 + ( n * 30))
        n += 1
