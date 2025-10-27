import pygame
from sketchpad import Sketchpad
from constants import *

icon_image = pygame.image.load(path + "icons/icon.png") 
 
scrn = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption(title)   
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()
 
# initialize modules
sp = Sketchpad(scrn)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEWHEEL:
            sp.scale_canvas(event.y)

    scrn.fill(bg_color)
    sp.update_input(pygame.key.get_pressed())
    sp.update()
    

    pygame.display.update()
    clock.tick(fps_limit)

# quit pygame after closing window
pygame.quit()