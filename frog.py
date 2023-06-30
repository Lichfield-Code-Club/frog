import pygame
import os
import yaml
from random import randint
from copy import deepcopy

def ReadConfig(game_name,filename):
    with open(filename,'r') as fr:
        config = yaml.safe_load(fr)
    return config[game_name]

def LoadImages(config):
    images = []
    background = [x for x in config['images'] if x['name'] == 'background'][0]
    num_logs = 0
    for image in config['images']:
        fpath = image['fpath']
        if not os.path.exists(fpath): 
            print(f'Cannot locate image file: {fpath}')
            return
        else:
            image['surface'] = pygame.image.load(fpath).convert_alpha()
            image['rect'] = image['surface'].get_rect()
            image['rect'].x = image['start']['x']
            image['rect'].y = image['start']['y']
            if image['sound']['fpath']: 
                image['sound']['fx'] = pygame.mixer.Sound(image['sound']['fpath'])
                image['sound']['fx'].set_volume(image['sound']['volume'])
            if image['name'].startswith('car'): 
                image['speed'] = randint(config['min_car_speed'],config['max_car_speed'])
                image['rect'].y = randint(background['road']['end'],background['road']['start'])
            if image['name'].startswith('log'): 
                image['speed'] = randint(config['min_log_speed'],config['max_log_speed'])
                image['rect'].y = randint(background['water']['end'],background['water']['start'])
                image['rect'].y = background['water']['end'] + (num_logs * image['rect'].height)
                num_logs += 1
            images.append(image)
    return images

def InitGame(config):
    screen_width = config['screen_width']
    screen_height = config['screen_height']
    pygame.display.set_caption(config['game_title'])
    config['screen'] = pygame.display.set_mode((screen_width,screen_height))
    config['clock'] = pygame.time.Clock()
    pygame.mixer.music.load(config['road_noise_fpath'])
    pygame.mixer.music.set_volume(config['road_noise_volume'])
    config['large_text']['font'] = pygame.font.SysFont(config['large_text']['style'],config['large_text']['size'])
    config['small_text']['font'] = pygame.font.SysFont(config['small_text']['style'],config['small_text']['size'])
    return LoadImages(config)

def draw_zones(config):
    backgrounds = [x for x in config['images'] if x['name'] == 'background']
    for bg in backgrounds:
        for zone in ['base','road','water']:
            start = bg[zone]['start']
            end = bg[zone]['end']
            msg = f"{zone} start: {start} ---------------------------------------------------"
            draw_text(config['screen'],msg,config['large_text']['font'], 'white', 40, start)
            msg = f"{zone} end: {end} ---------------------------------------------------"
            draw_text(config['screen'],msg,config['large_text']['font'], 'white', 40, end)

def draw_text(screen,text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def Draw(config):
    for image in config['images']:
        if image['visible'] and not image['name'].startswith('frog'):
            config['screen'].blit(image['surface'],(image['rect'].x,image['rect'].y))
    for image in config['images']:
        if image['visible'] and image['name'].startswith('frog'):
            config['screen'].blit(image['surface'],(image['rect'].x,image['rect'].y))
    draw_zones(config)
    pygame.display.update()

def Move(config):
    ignore = ['background','ouch']
    for image in config['images']:
        if not image['name'] in ignore:
            if config['back']: 
                image['rect'].y += image['jump_size'] * -1
                config['back'] = False
            if config['jump']: 
                image['rect'].y += image['jump_size']
                if image['sound']['fpath']: image['sound']['fx'].play()
                config['jump'] = False
            if image['speed'] > 0 and image['name'] == 'frog':
                if config['left']: 
                    image['rect'].x -= image['speed']
                    config['left'] = False
                if config['right']: 
                    image['rect'].x += image['speed']
                    config['right'] = False
            if image['speed'] > 0 and image['name'] != 'frog':
                    image['rect'].x -= image['speed']
                    if image['rect'].x <= 0: image['rect'].x= config['screen_width']
            
            if image['rect'].x < 0: image['rect'].x = 0
            if image['rect'].y < 0: image['rect'].y = 0

            if image['rect'].x > config['screen_width']: image['rect'].x = config['screen_width']
            if image['rect'].y > config['screen_height']: image['rect'].y = config['screen_height']
    return True

def Collision(config):
    frog = [x for x in config['images'] if x['name'] == 'frog'][0]
    ouch = [x for x in config['images'] if x['name'] == 'ouch'][0]
    background = [x for x in config['images'] if x['name'] == 'background'][0]
    logs = [x for x in config['images'] if x['name'].startswith('log')]
    cars = [x for x in config['images'] if x['name'].startswith('car')]
    config['hits'] = []
    has_collision = False
    car_hits = []
    log_miss = []

    if frog['rect'].y < background['road']['start'] and frog['rect'].y > background['road']['end']:
        car_hits = [car for car in cars if frog['rect'].colliderect(car['rect'])]
        if len(car_hits) > 0:
            for car in car_hits: 
                car['rect'].x = frog['rect'].x
                car['sound']['fx'].play()
                ouch['rect'] = car['rect']
        
    if frog['rect'].y < background['road']['end'] and frog['rect'].y > background['water']['end']:
        log_hits = [log for log in logs if frog['rect'].colliderect(log['rect'])]
        if len(log_hits):
            frog['rect'].y =  log_hits[0]['rect'].y
            frog['rect'].x =  log_hits[0]['rect'].x
        
    #if frog['rect'].y < background['water']['start'] and frog['rect'].y > background['water']['end']:
    #    log_miss = [log for log in logs if not frog['rect'].colliderect(log['rect'])]
    #    if len(log_hits):
    #        for miss in log_miss:
    #            print('Missed',log_miss)
    #            miss['sound']['fx'].play()
    #            ouch['rect'] = miss['rect']

    if len(car_hits) > 0 : config['score']['status'] = 'COLLISION With Car'
    if len(log_miss) > 0 : config['score']['status'] = 'Missed a log!'

    has_collision = len(car_hits) + len(log_miss) > 0
    return has_collision

def Reset(config):
    pygame.mixer.music.play()
    return LoadImages(config)

def Success(config):
    frog = [x for x in config['images'] if x['name'] == 'frog'][0]
    background = [x for x in config['images'] if x['name'] == 'background'][0]
    success = frog['rect'].y < background['water']['end'] - 10
    if success: 
        config['score']['status'] = 'SUCCESS'
        config['score']['current'] += 1
    return success

def GameOver(config):
    WHITE = (255,255,255)

    pygame.mixer.music.fadeout(3000)
    score = config['score']['current']
    #if score > config['score']['highest']: config['score']['highest'] = score
    draw_text(config['screen'],f"GAME OVER! {config['score']['status']}", config['large_text']['font'], WHITE, 1000, 890)
    draw_text(config['screen'],f'SCORE: {score}', config['large_text']['font'], WHITE, 1000, 910)
    draw_text(config['screen'],'PRESS RETURN TO PLAY AGAIN',config['large_text']['font'], WHITE, 1000, 930)
    config = Reset(config)

def Play(config):
    pygame.mixer.music.play(-1,config['road_noise_volume'])    
    game_over = False
    run = True
    while run:
        config['clock'].tick(config['frame_rate'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: config['jump'] = True
                if event.key == pygame.K_UP: config['jump'] = True
                if event.key == pygame.K_DOWN: config['back'] = True
                if event.key == pygame.K_LEFT: config['left'] = True
                if event.key == pygame.K_RIGHT: config['right'] = True
                if event.key == pygame.K_RETURN: game_over = False

        if game_over == False:
            if run:
                game_over = Collision(config)
                Move(config)
                Draw(config)
                if not game_over:
                    game_over = Success(config)
        else:
            GameOver(config)
        pygame.display.update()

game_name = 'frog'
config_file = f'{game_name}_config.yaml'
config = ReadConfig(game_name,config_file)

pygame.init()
if InitGame(config): 
    Play(config)
pygame.quit()
exit() 