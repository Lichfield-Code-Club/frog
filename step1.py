import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#framerate
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# we set a variable call run to true
# line 22: while run is true the game repeatedly loops through the code
# line 24: looks for events
# line 25: checks to see if it's a quit event 
# the quit event is when the x in the top right of the window is clicked
# line 26: we set the run value to False

run = True
while run: 
  clock.tick(FPS)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

pygame.quit()
