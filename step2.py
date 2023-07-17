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
# find it's rectangle, which is x,y,w,h
#   x = x coordinate
#   y = y coordinate
#   w = width of rectangle
#   h = height of rectangle
bg_rect = bg_img.get_rect()
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
# line 44: while run is true the game repeatedly loops through the code
# line 46: looks for events
# line 47: checks to see if it's a quit event 
# the quit event is when the x in the top right of the window is clicked
# line 48: we set the run value to False
# If it's not a quit
# line 50: we move the image to the 'display' using blit, BLock Image Transfer
# line 51: and then update what we see

run = True
while run: 
   clock.tick(FPS)
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
       run = False
    else:
        screen.blit(bg_img, (bg_rect.x,bg_rect.y))
        pygame.display.update()
pygame.quit()
