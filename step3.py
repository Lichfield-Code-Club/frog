import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load an image for the background
bg_img = pygame.image.load('images/background.png').convert_alpha()
# load an image for the background
frog_img = pygame.image.load('images/frog.png').convert_alpha()
# find it's rectangle, which is x,y,w,h
#   x = x coordinate
#   y = y coordinate
#   w = width of rectangle
#   h = height of rectangle
bg_rect = bg_img.get_rect()
frog_rect = frog_img.get_rect()
# for debug purpose display the rectangle details
print('Background Image Rectangle', bg_rect)
print('Background Image x coordinate', bg_rect.x)
print('Background Image y coordinate', bg_rect.y)
print('Background Image width', bg_rect.width)
print('Background Image height', bg_rect.height)

# We can control where the image is displayed by
# changing the x and y coordinates
# for backgrounds it's usually 0,0, which is top left corner

# we set a variable call run to true
# line 47: while run is true the game repeatedly loops through the code
# line 49: looks for events
# line 50: checks to see if it's a quit event 
# the quit event is when the x in the top right of the window is clicked
# line 51: we set the run value to False
# If it's not a quit
# line 53: we move the background image to the 'display' using blit, BLock Image Transfer
# line 54: we move the frog image to the 'display' using blit, BLock Image Transfer
# line 51: and then update what we see

run = True
while run: 
   clock.tick(FPS)
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
       run = False
    else:
        screen.blit(bg_img, (bg_rect.x,bg_rect.y))
        screen.blit(frog_img, (frog_rect.x,frog_rect.y))
        pygame.display.update()
pygame.quit()
