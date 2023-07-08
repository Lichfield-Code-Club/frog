import pygame
import yaml
import properties

pygame.font.init()
large_text = pygame.font.SysFont(properties.LARGE_TEXT_FONT,properties.LARGE_TEXT_SIZE)
small_text = pygame.font.SysFont(properties.SMALL_TEXT_FONT,properties.SMALL_TEXT_SIZE)

def GameIntro(game):
    screen = game['screen']
    WHITE = (255,255,255)
    pygame.display.set_caption("Game Into")
    pygame.mixer.music.fadeout(3000)
    msg = 'PRESS SPACE TO START GAME'
    draw_text(screen,msg,large_text, WHITE, 1000, 880)

def GameOver(game):
    screen = game['screen']
    WHITE = (255,255,255)
    pygame.mixer.music.fadeout(3000)
    score = 0 # config['score']['current']
    msg = f'GAME OVER! {score}'
    draw_text(screen,msg,large_text, WHITE, 1000, 880)
    msg = f'SCORE: {score}'
    draw_text(screen,msg,large_text, WHITE, 1000, 910)
    msg = 'PRESS RETURN TO PLAY AGAIN'
    draw_text(screen,msg,large_text, WHITE, 1000, 940)

def GameWon(frogs):
    success = False
    for frog in frogs:
        if frog.rect.y < frog.rect.height + 20:
            success = True
    return success

def ReadConfig(filename):
    with open(filename,'r') as fr:
        return yaml.safe_load(fr)

def draw_text(screen,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_line(screen, prefix,start,end):
    msg = f"{prefix}: start: {start} ---------------------------------------------------"
    draw_text(screen,msg,large_text, 'white', 40, start)
    msg = f"{prefix}   end: {end} ---------------------------------------------------"
    draw_text(screen,msg,large_text, 'white', 40, end)

def draw_zones(screen):
    draw_line(screen,'base',properties.BASE_START,properties.BASE_END)
    draw_line(screen,'road',properties.ROAD_START,properties.ROAD_END)
    draw_line(screen,'water',properties.WATER_START,properties.WATER_END)
    #pygame.mixer.music.load(config['road_noise_fpath'])
    #pygame.mixer.music.set_volume(config['road_noise_volume'])
    #pygame.mixer.music.play(-1,config['road_noise_volume'])    


def boundary_checks(rect,initial_rect):
     if rect.y < 0: rect.y = initial_rect.height
     if rect.y > properties.SCREEN_HEIGHT - rect.height: rect.y = properties.SCREEN_HEIGHT - rect.height
     if rect.x < 0: rect.x = properties.SCREEN_WIDTH
     if rect.x > properties.SCREEN_WIDTH: rect.x = 0
     return rect

def SaveConfig(config,fpath):
    config['clock'] = None
    with open(fpath,'w') as fw:
        yaml.dump(config['cars'],fw)

def car_hit(config,frogs,cars):
    for frog in frogs:
        if frog.rect.y >= config['road_end'] and frog.rect.y <= config['road_start']:
            if pygame.sprite.spritecollide(frog, cars, False):
                return True
    return False

def log_miss(config,frogs,logs):
    miss = False
    for frog in frogs:
        if frog.rect.y > config['water_end'] and frog.rect.y < config['water_start'] - frog.rect.height:
            miss = not pygame.sprite.spritecollide(frog, logs, False)
            print('log miss', miss)
    return miss
