import pygame

class Panel:
    def __init__(self, scrn, pos, dimension, color = (255, 255, 255)):
        self.scrn = scrn
        self.active = True
        self.color = color
        self.buttons = []
        self.text = [] 

        self.rect = pygame.Rect(pos + dimension)
    
    def show(self, val = True):
        self.active = val

    def hide(self, val = True):
        self.active = not val
    
    def shown(self):
        return self.active

    def update(self):
        if not self.active:
            return

        pygame.draw.rect(self.scrn, self.color,self.rect)

        for b in self.buttons:
            b.update()
        
        for t in self.text:
            t.update()
    
    def change_rect(self, new_rect):
        self.rect = pygame.Rect(new_rect)
        
    def add_button(self, button):
        self.buttons.append(button)

    def add_text(self, txt):
        self.text.append(txt)
    
    def get_buttons(self):
        return self.buttons


class Button:
    def __init__(self, scrn,  pos, dimensions):
        self.image = None
        self.scrn = scrn
        self.pos = pos
        self.dimensions = dimensions

        self.background = None
        self.hovered_bg = None

        self.action = None

        self.clicked = False

    def update(self):
        # check mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = False
        back_ground_col = self.background

        if (mouse_x > self.pos[0] and mouse_x < self.pos[0] + self.dimensions[0]):
            if (mouse_y > self.pos[1] and mouse_y < self.pos[1] + self.dimensions[1]):
                hovered = True
        
        if hovered:
            back_ground_col = self.hovered_bg
        
        # check select
        buttons = pygame.mouse.get_pressed()

        if buttons[0]:
            if not self.clicked and hovered:
                self.clicked = True
                if self.action != None:
                    self.action()
                
        else:
            self.clicked = False

        
        # render
        if back_ground_col != None:
            pygame.draw.rect(self.scrn, back_ground_col, pygame.Rect(*(self.pos + self.dimensions)))

        if self.image != None:
            self.scrn.blit(self.image, (self.image_pos))
        
    # add components
    def add_background(self, background):
        self.background = background
    
    def add_hovered_background(self, hovered_bg):
        self.hovered_bg = hovered_bg

    def add_graphic(self, file):
        self.image = pygame.image.load(file)

        width, height = self.image.get_size()

        image_x_pos = self.pos[0] + (self.dimensions[0] - width)/2
        image_y_pos = self.pos[1] + (self.dimensions[1] - height)/2

        self.image_pos = [image_x_pos, image_y_pos]
    
    def add_text(self):
        pass

    def add_action(self, action):
        self.action = action

    # change components
    def move(self, offset) :
        self.pos[0] += offset[0] 
        self.pos[1] += offset[1]

        self.image_pos[0] += offset[0]
        self.image_pos[1] += offset[1]

    def replace_image_color(self ,old_col, new_col):
        if self.image == None:
            return
        
        var = pygame.PixelArray(self.image)
        var.replace(old_col, new_col)
        del var

class Text:
    def __init__(self, scrn, pos, txt, color = (0,0,0)):
        pass

    def update(self):
        pass

    