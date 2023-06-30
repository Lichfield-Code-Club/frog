import pygame
import os
from glob import glob
from random import randint

def configure_background(bg):
    for zone in ['base','road','water']:
        bg[zone]['sound']['fx'] = pygame.mixer.Sound(bg[zone]['sound']['fpath'])
        bg[zone]['sound']['fx'].set_volume(bg[zone]['sound']['volume'])

def configure_random(config,background,category):
    for image in config['objects'][category]:
        min_name = f'min_{category}_speed'
        max_name = f'max_{category}_speed'
        min = config[min_name]
        max = config[max_name]
        image['speed']  = randint(min,max)

    if category == 'frogs':
        min = background['base']['end']
        max = background['base']['start']
        for image in config['objects']['frogs']:image['rect'].y = randint(min,max)

    if category == 'cars':
        min = background['road']['end']
        max = background['road']['start']
        for car in config['objects']['cars']:
            car['crash']['sound']['fx'] = pygame.mixer.Sound(car['crash']['sound']['fpath'])
            car['crash']['sound']['fx'].set_volume(car['crash']['sound']['volume'])
            car['crash']['image']['surface'] = pygame.image.load(car['crash']['image']['fpath']).convert_alpha()
            car['crash']['image']['rect'] = car['crash']['image']['surface'].get_rect()
            car['rect'].y = randint(min,max)

    if category == 'logs':
        min = background['water']['end']
        max = background['water']['start']
        for log in config['objects']['logs']:
            log['miss']['sound']['fx'] = pygame.mixer.Sound(log['miss']['sound']['fpath'])
            log['miss']['sound']['fx'].set_volume(log['miss']['sound']['volume'])
            log['miss']['image']['surface'] = pygame.image.load(log['miss']['image']['fpath']).convert_alpha()
            log['miss']['image']['rect'] = log['miss']['image']['surface'].get_rect()
            log['rect'].y = randint(min,max)
            #print('Log',log['filename'],log['rect'])

def configure_object(config,category):
    if category == 'backgrounds': [configure_background(bg) for bg in config['objects'][category]]
    else:
        background = config['objects']['backgrounds'][0]
        configure_random(config,background,category)

def LoadImages(config):
    for category in config['objects'].keys():
        images = []
        image_files = glob(config[category]['fpath'])
        print(image_files)
        for img_file in image_files:
            print('Processing',img_file)
            img = config[category]
            img['filename'] = img_file
            print('Assigned', img['filename'])
            img['name'] = os.path.basename(img_file).split('.')[0]
            img['surface'] = pygame.image.load(img_file).convert_alpha()
            img['rect'] = img['surface'].get_rect()
            img['sound']['fx'] = pygame.mixer.Sound(img['sound']['fpath'])
            img['sound']['fx'].set_volume(img['sound']['volume'])
            images.append(img)
        config['objects'][category] = images
        print('Here 1',config['objects'][category])
    for category in config['objects'].keys():
        for obj in config['objects'][category]:
            print('obj',obj['filename'])
        configure_object(config,category)
        print(f"Number of {category}: {len(config['objects'][category])}")
    return config['objects']
