import pygame as pg
import sys
  
class Button(object):
    def __init__(self,rect,command,**kwargs):
        self.rect = pg.Rect(rect)
        self.command = command
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()
  
    def process_kwargs(self,kwargs):
        settings = {
            "color"             : pg.Color('green'),
            "text"              : None,
            "font"              : None, #pg.font.Font(None,16),
            "call_on_release"   : True,
            "hover_color"       : None,
            "clicked_color"     : None,
            "font_color"        : pg.Color("black"),
            "hover_font_color"  : None,
            "clicked_font_color": None,
            "click_sound"       : None,
            "hover_sound"       : None,
            'border_color'      : pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled'          : False,
            'disabled_color'     : pg.Color('grey'),
            'radius'            : 3,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)
  
    def render_text(self):
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)
  
    def get_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)
  
    def on_click(self,event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()
  
    def on_release(self,event):
        if self.clicked and self.call_on_release:
            #if user is still within button rect upon mouse release
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()
        self.clicked = False
  
    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False
  
    def draw(self,surface):
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color
        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(surface, self.rect , border, rad, 1, color)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text,text_rect)
              
              
    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
        rect = pg.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0,0
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)
  
  
    def _render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pg.draw.circle(image, color, getattr(corners,attribute), rad)
        image.fill(color, rect.inflate(-2*rad,0))
        image.fill(color, rect.inflate(0,-2*rad))
          
    def update(self):
        #for completeness
        pass
   
class Number:
    def __init__(self, screenrect):
        self.timer = 0.0
        self.delay = 1000
        self.screenrect = screenrect
        self.num = 0
        self.new_num()
  
    def inc_num(self):
        self.num += 1
        return str(self.num)
   
    def new_num(self):
        self.image, self.rect = self.make_text(self.inc_num(), (255,0,0), self.screenrect.center, 75, 'Ariel')
   
    def make_text(self,message,color,center,size, fonttype):
        font = pg.font.SysFont(fonttype, size)
        text = font.render(message,True,color)
        rect = text.get_rect(center=center)
        return text,rect
   
    def update(self):
        if pg.time.get_ticks()-self.timer > self.delay:
            self.timer = pg.time.get_ticks()
            self.new_num()
   
    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.btn_settings = {
        "clicked_font_color" : (0,0,0),
        "hover_font_color"   : (205,195, 100),
        'font'               : pg.font.Font(None,16),
        'font_color'         : (0,0,0),
        'border_color'       : (0,0,0),
        }
    def switch_state(self):
        self.done = True
    
class Menu(States):
    def __init__(self, screenrect):
        States.__init__(self)
        self.next = 'game'
        self.btn = Button(rect=(10,10,105,25), command=self.switch_state, text='Unpause', **self.btn_settings)
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        self.btn.get_event(event)
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.btn.draw(screen)
    
class Game(States):
    def __init__(self, screenrect):
        States.__init__(self)
        self.next = 'menu'
        self.num = Number(screenrect)
        self.btn = Button(rect=(10,10,105,25), command=self.switch_state, text='Pause', **self.btn_settings)
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        self.btn.get_event(event)
    def update(self, screen, dt):
        self.draw(screen)
        self.num.update()
    def draw(self, screen):
        screen.fill((0,0,255))
        self.num.draw(screen)
        self.btn.draw(screen)
    
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.state_dict = {
            'menu': Menu(self.screen_rect),
            'game': Game(self.screen_rect)
        }
    def setup_states(self, start_state):
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
    
    
settings = {
    'size':(600,400),
    'fps' :60
}
  
pg.init()
    
app = Control(**settings)
  
app.setup_states('menu')
app.main_game_loop()
pg.quit()
sys.exit()