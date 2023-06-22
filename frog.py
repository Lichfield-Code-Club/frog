import pygame
import os
import yaml

def ReadConfig(game_name,filename):
    with open(filename,'r') as fr:
        config = yaml.safe_load(fr)
    return config[game_name]
    
def LoadImages(config):
    images = []
    for image in config['images']:
        fpath = image['fpath']
        if not os.path.exists(fpath): 
            print(f'Cannot locate image file: {fpath}')
            return
        else:
            image['surface'] = pygame.image.load(fpath).convert_alpha()
            coords = (image['coord']['x'],image['coord']['y'])
            image['rect'] = image['surface'].get_rect(midbottom=coords)
            images.append(image)
    return images

def InitGame(config):
    screen_width = config['screen_width']
    screen_height = config['screen_height']
    pygame.display.set_caption(config['game_title'])
    config['screen'] = pygame.display.set_mode((screen_width,screen_height))
    config['clock'] = pygame.time.Clock()
    return LoadImages(config)

def Draw(config):
    for image in config['images']:
        config['screen'].blit(image['surface'],(image['coord']['x'],image['coord']['y']))
    pygame.display.update()

def Move(config):
    for image in config['images']:
        if image['gravity'] < 0:
            if config['drop']: 
                image['coord']['y'] += config['drop_rate']
                config['drop'] = False
            if config['jump']: 
                image['coord']['y'] += image['gravity']
                config['jump'] = False
        if image['speed'] > 0 and image['name'] == 'frog':
            if config['left']: 
                image['coord']['x'] -= image['speed']
                config['left'] = False
            if config['right']: 
                image['coord']['x'] += image['speed']
                config['right'] = False
        if image['speed'] > 0 and image['name'] != 'frog':
                image['coord']['x'] -= image['speed']
                if image['coord']['x'] <= 0: image['coord']['x']= config['screen_width']

        if image['coord']['x'] < 0: image['coord']['x'] = 0
        if image['coord']['y'] < 0: image['coord']['y'] = 0
        if image['coord']['x'] > config['screen_width']: image['coord']['x'] = config['screen_width']
        if image['coord']['y'] > image['start']['y']: image['coord']['y'] = image['start']['y']

def Play(config):
    play_game = True
    while play_game:
        config['clock'].tick(config['frame_rate'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: config['jump'] = True
                if event.key == pygame.K_UP: config['jump'] = True
                if event.key == pygame.K_DOWN: config['drop'] = True
                if event.key == pygame.K_LEFT: config['left'] = True
                if event.key == pygame.K_RIGHT: config['right'] = True

        Move(config)
        Draw(config)

game_name = 'frog'
config_file = f'{game_name}_config.yaml'
config = ReadConfig(game_name,config_file)

pygame.init()
if InitGame(config): Play(config)
pygame.quit()
exit()