import pygame
import yaml
from glob import glob
from images import LoadImages

def ReadConfig(game_name,filename):
    with open(filename,'r') as fr:
        config = yaml.safe_load(fr)
    return config[game_name]

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

def draw_text(screen,text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_images(config,category):
    for image in config['objects'][category]:
        if image['visible']:
            config['screen'].blit(image['surface'],(image['rect'].x,image['rect'].y))

def Draw(config):
    for category in config['objects'].keys():
        draw_images(config,category)
    for bg in config['objects']['backgrounds']:
        for zone in ['base','road','water']:
            start = bg[zone]['start']
            end = bg[zone]['end']
            msg = f"{zone} start: {start} ---------------------------------------------------"
            draw_text(config['screen'],msg,config['large_text']['font'], 'white', 40, start)
            msg = f"{zone} end: {end} ---------------------------------------------------"
            draw_text(config['screen'],msg,config['large_text']['font'], 'white', 40, end)
    pygame.display.update()

def boundary_check(config,image):
    rect = image['rect']
    if rect.x < 0: rect.x = config['screen_width']
    if rect.x > config['screen_width']: rect.x = 0 # wrap around
    if rect.y < 0: rect.y = config['screen_height']
    if rect.y > config['screen_height']: rect.y = 0 # wrap around
    return rect

def move_frog(config):
    for frog in config['objects']['frogs']: 
        if config['back']: 
            frog['rect'].y += frog['speed']
            config['back'] = False

        if config['jump']: 
            frog['rect'].y -= frog['jump']
            frog['sound']['fx'].play()
            config['jump'] = False
            
        if config['up']: 
            frog['rect'].x -= frog['speed']
            config['up'] = False

        if config['left']: 
            frog['rect'].x -= frog['speed']
            config['left'] = False

        if config['right']: 
            frog['rect'].x += frog['speed']
            config['right'] = False

def Move(config):
    move_frog(config)
    for category in ['cars','logs']:
        for image in config['objects'][category]: image['rect'].x -= image['speed']
    for category in ['cars','logs','frogs']:
        for image in config['objects'][category]: image['rect'] = boundary_check(config,image)
    return True

def Collision(config):
    frogs = config['objects']['frogs']
    cars = config['objects']['cars']
    logs = config['objects']['logs']
    backgrounds = config['objects']['backgrounds']

    road_start  = backgrounds[0]['road']['end']
    road_end    = backgrounds[0]['road']['start']
    water_start = backgrounds[0]['water']['end']
    water_end   = backgrounds[0]['water']['start']

    config['hits'] = []
    has_collision = False
    car_hits = []
    log_miss = []

    for frog in frogs:
        rect = frog['rect']

        if rect.y < road_end and rect.y > road_start:
            car_hits = [car for car in cars if rect.colliderect(car['rect'])]
            if len(car_hits) > 0:
                for car in car_hits: 
                    car['rect'].x = frog['rect'].x
                    car['sound']['fx'].play()
                    car['crash']['rect'] = car['rect']
            
        if rect.y < water_start and rect.y > water_end:
            log_miss = [log for log in logs if not rect.colliderect(log['rect'])]
            if len(log_miss): 
                for miss in log_miss:
                    miss['sound']['fx'].play()
                    #log['miss']['rect'] = miss['rect']

        if len(car_hits) > 0 : config['score']['status'] = 'COLLISION With Car'
        if len(log_miss) > 0 : config['score']['status'] = 'Missed a log!'

        has_collision = len(car_hits) + len(log_miss) > 0
        if has_collision: 
            pygame.mixer.music.fadeout(1000)

    return has_collision

def Reset(config):
    pygame.mixer.music.play()
    return LoadImages(config)

def Success(config):
    water_end = config['objects']['backgrounds'][0]['water']['end']
    for frog in config['objects']['frogs']:
        success = frog['rect'].y < water_end - 10
        if success: 
            config['score']['status'] = 'SUCCESS'
            config['score']['current'] += 1
            return success
    return False

def GameOver(config):
    WHITE = (255,255,255)
    pygame.mixer.music.fadeout(3000)
    score = config['score']['current']
    draw_text(config['screen'],f"GAME OVER! {config['score']['status']}", config['large_text']['font'], WHITE, 1000, 880)
    draw_text(config['screen'],f'SCORE: {score}', config['large_text']['font'], WHITE, 1000, 900)
    draw_text(config['screen'],'PRESS RETURN TO PLAY AGAIN',config['large_text']['font'], WHITE, 1000, 920)
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
                if event.key == pygame.K_UP: config['up'] = True
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