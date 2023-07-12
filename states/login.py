import pygame
from .base import BaseState
from random import randint
from utils import draw_large_text, draw_medium_text, LoadPlayer

class Login(BaseState):
    def __init__(self):
        super(Login, self).__init__()
        self.next_state = "MENU"
        self.time_active = 0
        self.bg_img     = pygame.image.load(self.config['background_image_fpath']).convert_alpha()
        self.login_btn  = pygame.image.load(self.config['login_btn']).convert_alpha()
        self.play_btn   = pygame.image.load(self.config['play_btn']).convert_alpha()
        self.back_btn   = pygame.image.load(self.config['back_btn']).convert_alpha()
        self.frog_img   = pygame.image.load(self.config['frog_image_fpath']).convert_alpha()
        self.bg_rect    = self.bg_img.get_rect()
        self.login_rect = self.login_btn.get_rect()
        self.play_rect  = self.play_btn.get_rect()
        self.back_rect  = self.back_btn.get_rect()
        self.frog_rect  = self.frog_img.get_rect()
        self.bg_colour  = (60, 114, 228)
        self.logged_in  = False
        self.login_clicked = False
        self.play_clicked = False
        self.back_clicked = False
        self.login_action  = False

    def update(self,dt):
        pos = pygame.mouse.get_pos()
        if self.login_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.login_clicked == False:
                self.login_clicked = True
                self.login_action = True
                # Will need to check login, but assume it's okay for now
                self.logged_in = True
                player = self.config['player']
                #print('Player Before',player)
                self.config = LoadPlayer(self.config)
                player = self.config['player']
                #print('Player After',player)
        if self.play_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.login_clicked == False:
                self.play_clicked = True
        if self.back_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.login_clicked == False:
                self.back_clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            if self.play_clicked:
                self.done = True
                self.next_state = 'GAMEPLAY'
                #print('Play Clicked')
            elif self.back_clicked:
                self.done = True
            else:
                self.login_clicked = False

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
        if event.type == pygame.TEXTINPUT:
            if not self.logged_in:
                if self.config['player']['name'] == None:
                    self.config['player']['name'] = ''
                if len(self.config['player']['name']) < self.config['player']['max_name_len']:
                    self.config['player']['name'] += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.config['player']['name'] = self.config['player']['name'][:-1]
    
    def draw(self, surface):
        surface.fill(self.bg_colour)
        self.draw_name(surface)
        if self.logged_in:
            self.draw_history(surface)
            self.draw_next_btn(surface)
        else:
            self.draw_login_btn(surface)

    def draw_login_btn(self,surface):
        player = self.config['player']
        TEXT_COLOUR = (0, 0, 0)
        self.login_rect.x = player['name_box_x'] + 20
        self.login_rect.y = player['name_box_y'] + 40
        surface.blit(self.login_btn, self.login_rect.topleft)

    def draw_next_btn(self,surface):
        player = self.config['player']
        x = player['history_box_x'] + 20
        y = player['history_box_y'] + player['history_box_h'] + 40
        self.play_rect.x = x
        self.play_rect.y = y
        self.back_rect.x = x + 600
        self.back_rect.y = y 
        draw_large_text(surface,'play','green',x,y + 60)
        surface.blit(self.play_btn, self.play_rect.topleft)
        draw_large_text(surface,'back','green',x+600,y + 60)
        surface.blit(self.back_btn, self.back_rect.topleft)
        
    def draw_name(self,surface):
        player = self.config['player']
        TEXT_COLOUR = (0, 0, 0)
        x = player['name_box_x']
        y = player['name_box_y']
        w = player['name_box_w']
        h = player['name_box_h']

        x1 = x - 110
        y1 = y 

        rect = pygame.Rect(x,y,w,h)

        pygame.draw.rect(surface,'white',rect)
        #text_messages = ['LOGIN','Name','Type in name','Press ENTER when done']
        text_messages = ['Name']
        for line_num, line in enumerate(text_messages):
            draw_large_text(surface,line,'cyan',x1,y1 + (line_num * 40))
        draw_large_text(surface,player['name'],TEXT_COLOUR,x + 10,y + 2)

    def draw_history(self,surface):
        if self.logged_in:
            player = self.config['player']
            TEXT_COLOUR = (0, 0, 0)
            x = player['history_box_x']
            y = player['history_box_y']
            w = player['history_box_w']
            h = player['history_box_h']
            rect = pygame.Rect(x,y,w,h)
            pygame.draw.rect(surface,'white',rect)
            n = 0
            runs = player['runs']
            runs.reverse()
            draw_medium_text(surface, 'Start', TEXT_COLOUR, x,  y - 40)
            draw_medium_text(surface, 'End',   TEXT_COLOUR, x + 300,  y - 40)
            draw_medium_text(surface, 'Score', TEXT_COLOUR, x + 600,  y - 40)
            for run in runs[:5]:
                y_coord = 600 + (n * 30) # Only latest 5 runs
                draw_medium_text(surface,f"{run['start']}",TEXT_COLOUR,x,600     + (n * 30))
                draw_medium_text(surface,f"{run['end']}",  TEXT_COLOUR,x+300,600 + (n * 30))
                draw_medium_text(surface,f"{run['score']}",TEXT_COLOUR,x+600,600 + (n * 30))
                n += 1        