import pygame
from sketchpad import Sketchpad

width = 800
height = 600
bg_color = (202, 202, 202)
 
scrn = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('PySketch')   

clock = pygame.time.Clock()
fps_limit = 60
 
# initialize modules
sp = Sketchpad(scrn)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEWHEEL:
            print(event.x, event.y)
            sp.scale_canvas(event.y)

    scrn.fill(bg_color)
    sp.update_input(pygame.key.get_pressed())
    sp.update()
    

    pygame.display.update()
    clock.tick(fps_limit)

# quit pygame after closing window
pygame.quit()