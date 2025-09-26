
from drawings import FreeShape, Action, draw_rect, Line, Rectangle, Circle
from toolbar import Toolbar
from constants import select_rect_col
import pygame

# keeps track of drawing, moving and updating shapes
class Sketchpad:
    def __init__(self, scrn):
        self.scrn = scrn

        self.tool_bar = Toolbar(scrn, self)
        self.tool = None
        # shape selected when creating shapes
        self.shape = None

        self.pointer = Pointer(self.tool_bar)

        self.keys = {}

        self.shapes = []
        self.undo   = []
        self.redo   = []
        self.new_shape = True
        self.new_select = True
        self.moving_select = False
        self.select_anchor = None
        self.selected_objects = []

        self.global_offset = [0,0]
        self.global_scaler = 1

        


    def update(self):
        self.pointer.update()
        self.update_mover()

        if self.tool == 0:
            self.update_select()
        elif self.tool == 1:
            self.update_pen()
        elif self.tool == 2:
            self.update_shape()

        for s in self.shapes:
            s.update()

        self.tool_bar.update()
    
    def update_input(self, lst):
        self.keys = lst
        self.tool_bar.update_input(lst)

    # call me an italian the way i write spaghetti fr fr
    def update_select(self):
        

        move_offset = [0,0]

        min_x, min_y, max_x, max_y = [],[],[],[]
        for obj in self.selected_objects:
            x1, y1, x2, y2 = obj.get_boundaries()
            min_x.append(x1)
            max_x.append(x2)
            min_y.append(y1)
            max_y.append(y2)


        x1, y1, x2, y2 = 0,0,0,0
        if len(self.selected_objects) > 1:
            x1, y1, x2, y2 = min(min_x), min(min_y), max(max_x), max(max_y)

        keys = self.keys
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.pointer.pos != None:
            if self.new_select:
                self.moving_select = False
                self.select_anchor = self.pointer.pos
                # check if are selecting our previous block
                if len(self.selected_objects) > 1:
                    if self.pointer.pos[0] > x1 and self.pointer.pos[0] < x2:
                        if self.pointer.pos[1] > y1 and self.pointer.pos[1] < y2:
                            self.moving_select = True

                else:

                    # check if we are selecting an object
                    for s in self.shapes:
                        x_min, y_min, x_max, y_max = s.get_boundaries()
                        if self.pointer.pos[0] > x_min and self.pointer.pos[0] < x_max:
                            if self.pointer.pos[1] > y_min and self.pointer.pos[1] < y_max:
                            # if the object is already selected, keep current selection. Otherwise clear
                                if s not in self.selected_objects:
                                    
                                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                                        self.selected_objects.append(s)
                                    else:
                                        self.selected_objects = [s]
                                self.moving_select = True

                if not self.moving_select:
                    self.selected_objects.clear()


                self.new_select = False
            # we are moving seected objects
            elif self.moving_select:
                try:
                    move_offset = [(self.pointer.pos[0] - self.pointer.old_pos[0]) / self.global_scaler, (self.pointer.pos[1] - self.pointer.old_pos[1])/ self.global_scaler]
                except:
                    move_offset = [0,0]

                for obj in self.selected_objects:
                    obj.move(move_offset)


            # we are creating a boundary to select objects
            else:
                max_x = max([self.pointer.pos[0], self.select_anchor[0]])
                min_x = min([self.pointer.pos[0], self.select_anchor[0]])
                
                max_y = max([self.pointer.pos[1], self.select_anchor[1]])
                min_y = min([self.pointer.pos[1], self.select_anchor[1]])

                pygame.draw.rect(self.scrn, select_rect_col, pygame.Rect(min_x, min_y, max_x-min_x, max_y-min_y))  
                draw_rect(self.scrn, self.select_anchor, self.pointer.pos)

                # FIX ME
                # this rectangle collision algorithm is flawed
                for obj in self.shapes:
                    selected = False
                    x1c,y1c,x2c,y2c = obj.get_boundaries()

                    corners = [[x1c,y1c], [x2c,y1c], [x1c,y2c], [x2c,y2c]]
                    for c in corners:
                        x,y = c
            

                        if x > min_x and x < max_x:
                            if y > min_y and y < max_y:
                                if obj not in self.selected_objects:
                                    self.selected_objects.append(obj)
                                selected = True
                                continue
                    
                    if not selected and obj in self.selected_objects:
                        self.selected_objects.remove(obj)


        else:
            # add undo
            if self.moving_select and len(self.selected_objects) > 0 and not self.new_select:
                offset = [self.pointer.pos[0] - self.select_anchor[0], self.pointer.pos[1] - self.select_anchor[1]]
                Action(self.undo, self.redo, self.shapes, "move", self.selected_objects.copy(), offset)

            self.new_select= True
        
        if keys[pygame.K_DELETE] and len(self.selected_objects) > 0:
            for obj in self.selected_objects:
                self.shapes.remove(obj)
            Action(self.undo, self.redo, self.shapes, "del", self.selected_objects.copy())
            self.selected_objects.clear()
        



        if len(self.selected_objects) > 1:
            x1 += move_offset[0] * self.global_scaler
            y1 += move_offset[1] * self.global_scaler

            x2 += move_offset[0] * self.global_scaler
            y2 += move_offset[1] * self.global_scaler

            draw_rect(self.scrn, (x1, y1), (x2, y2))

        for obj in self.selected_objects:
            obj.draw_boundary()
        
        

    def update_pen(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.pointer.pos != None:
            if self.new_shape:
                shape = FreeShape(self)
                self.new_shape = False
            
            self.shapes[-1].add_point(self.pointer.pos)
            
        else:
            self.new_shape = True
    
    def update_shape(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.pointer.pos != None:
            print(self.new_shape)
            if self.new_shape:
                if self.shape == 0:
                    shape = Line(self)
                elif self.shape == 1:
                    shape = Rectangle(self)
                elif self.shape == 2:
                    shape = Circle(self)

                self.new_shape = False
            
            self.shapes[-1].add_point(self.pointer.pos)
            
        else:
            self.new_shape = True
    
    def update_mover(self):

        # offset
        buttons = pygame.mouse.get_pressed()

        if not buttons[0] and buttons[2] and self.pointer.pos != None and self.pointer.old_pos != None:
            #print(self.global_offset)
            self.global_offset[0] += (self.pointer.pos[0] - self.pointer.old_pos[0]) / self.global_scaler
            self.global_offset[1] += (self.pointer.pos[1] - self.pointer.old_pos[1]) / self.global_scaler

    def scale_canvas(self, direction):
        scaler_change_per_scroll = 0.05


        self.global_scaler += scaler_change_per_scroll*direction
        if self.global_scaler <= 0:
            self.global_scaler = scaler_change_per_scroll
            
    def change_tool(self, tool):
        self.selected_objects.clear()
        self.tool = tool
    
    def change_shape(self, shape):
        self.selected_objects.clear()
        self.shape = shape
    
    def undo_action(self):
        if len(self.undo) > 0:
            self.undo[-1].undo_action()
    
    def redo_action(self):
        if len(self.redo) > 0:
            self.redo[-1].redo_action()
    
# handles mouse position for the sketchpad
class Pointer:
    def __init__(self, tool_bar):
        self.tool_bar = tool_bar
        self.active = True
        self.pos = None
        self.old_pos = None

        self.button_press = False
    
    def update(self):
        if self.tool_bar.mouse_in_toolbar():
            if self.pos != None:
                self.old_pos = self.pos
            self.pos = None
            self.button_press = True
        elif not self.button_press:
            self.old_pos = self.pos
            self.pos = pygame.mouse.get_pos()
        else:
            buttons = pygame.mouse.get_pressed()
            if not buttons[0]:
                self.button_press = False
        
        

        # check for button shit

       #print(self.pos)
    


