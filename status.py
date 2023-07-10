import pygame
from utils import draw_text
from button import Button

def StatusUpdate(config,game):
    screen = game['screen']
    large_text = game['large_text']
    small_text = game['small_text']
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    grid = []
    button_text= [['Status','Number','MinSp','MaxSp'],
                  ['cars',None,None,None],
                  ['logs',None,None,None]
                  ]
    rows = len(button_text)
    cols = len(button_text[0])

    margin = 4
    border_width = 2 * margin
    grid_width = 400
    grid_height = rows * 25

    cell_width  = int(grid_width  / cols)
    cell_height = int(grid_height / rows)

    x1 = config['screen_width'] - grid_width  - border_width
    y1 = config['base_start']   - grid_height + border_width
    x2 = grid_width
    y2 = grid_height

    column_colours = [WHITE,GREEN]
    status_rect = pygame.Rect(x1,y1,x2,y2)
    pygame.draw.rect(screen,RED,status_rect)
    
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            x = x1 + margin + (col * (cell_width - margin))
            y = y1 + margin + (row * (cell_height))
            w = cell_width - border_width
            h = 16
            up_btn = None
            dn_btn = None
            rect = pygame.Rect(x,y,w,h)
            text = button_text[row][col]
            if row > 0:
                up_btn = Button(x+w-12,y,'images/arrow-up.png',1)
                dn_btn = Button(x+w-12,y+6,'images/arrow-down.png',1)
            colour = column_colours[col%2]
            item = {'rect': rect, 'colour': colour, 'up': up_btn, 'dn': dn_btn, 'text': text}
            grid[row].append(item)
    for row in grid:
        for col in row:
            if col['up']: col['up'].draw(screen)
            if col['dn']: col['dn'].draw(screen)
            if col['text']: 
                draw_text(screen,col['text'],small_text, WHITE, col['rect'].x+2,col['rect'].y+2)
