import numpy as np
import pygame
from constants import select_boundary_col


def draw_line(scrn, pos1, pos2, size = 1, color = (0,0,0), offset = [0,0], scaler = 1):
    scrn_size = scrn.get_size()

    cx = round(scrn_size[0] / 2)
    cy = round(scrn_size[1] / 2)

    pos1_transformed = [(pos1[0]+offset[0] - cx) * scaler + cx, (pos1[1] + offset[1] - cy) * scaler + cy]
    pos2_transformed = [(pos2[0]+offset[0] - cx) * scaler + cx, (pos2[1] + offset[1] - cy) * scaler + cy]
    pygame.draw.line(scrn, color, pos1_transformed, pos2_transformed, size)

def draw_rect(scrn, min_points, max_points, size=1, color=select_boundary_col):
    x1,y1 = min_points
    x2,y2 = max_points

    draw_line(scrn, (x1, y1), (x2, y1), size, color)
    draw_line(scrn, (x1, y1), (x1, y2), size, color)
    draw_line(scrn, (x2, y2), (x2, y1), size, color)
    draw_line(scrn, (x2, y2), (x1, y2), size, color)

# redo so first 4 arguments are replaced with sketchpad
class Shape:
    def __init__(self, sp, size = 1, color = (0,0,0)):
        self.drawn_offset = sp.global_offset.copy()
        self.drawn_scaler = sp.global_scaler

        self.sp = sp
        self.scrn = sp.scrn
        self.lst = sp.shapes
        self.size = size
        self.color = (0,0,0)
        self.offset = [0,0]
        self.points = np.empty((0,2))

        self.transformed_pointer = self.points.copy()
        self.transformed_offset = self.drawn_offset
        self.transformed_scaler = self.drawn_scaler

        self.action = Action(sp.undo, sp.redo, self.lst, "add", objects=[self])

        self.lst.append(self)



    # wut
    def update(self):
        pass

    def move(self, point):
        self.points[:, 0] += point[0]
        self.points[:, 1] += point[1]

    def erase(self):
        self.lst.remove(self)

    # returns min_x, min_y, max_x, max_y in terms of screen cords (including global offset and scaler)
    def get_boundaries(self):
        scaler = self.sp.global_scaler
        x_off, y_off = self.sp.global_offset

        scrn_size = self.scrn.get_size()
        cx = round(scrn_size[0]/2)
        cy = round(scrn_size[1]/2)

        xmin = (np.min(self.points[:, 0]) - cx + x_off) * scaler + cx
        ymin = (np.min(self.points[:, 1]) - cy + y_off) * scaler + cy

        xmax = (np.max(self.points[:, 0]) - cx + x_off) * scaler + cx
        ymax = (np.max(self.points[:, 1]) - cy + y_off) * scaler + cy

        return xmin, ymin, xmax, ymax

    def draw_boundary(self):
        min_x, min_y, max_x, max_y = self.get_boundaries()


        draw_rect(self.scrn, (min_x, min_y), (max_x, max_y), 1, select_boundary_col)
        return min_x, min_y, max_x, max_y

    def add_point(self, point):
        scrn_size = self.scrn.get_size()
        cx = round(scrn_size[0]/2)
        cy = round(scrn_size[1]/2)
        ofx = self.drawn_offset[0]
        ofy = self.drawn_offset[1]
        scaler = self.drawn_scaler
        

        x, y = point
        x = (x - cx) / scaler - ofx + cx
        y = (y - cy) / scaler - ofy + cy
        
        self.points = np.append(self.points, [[x,y]], axis=0)

class FreeShape(Shape):
    def __init__(self, sp,size=2, color=(0, 0, 0)):
        super().__init__(sp, size, color)
    
    def update(self):
        x_off, y_off = self.sp.global_offset

        scaler = self.sp.global_scaler

        size = np.size(self.points, axis=0)
        if size < 2:
            return

        for i in range(size - 1):
            draw_line(self.scrn, self.points[i], self.points[i+1], self.size, self.color, [x_off, y_off], scaler)


class Line(Shape):
    def __init__(self, sp, size = 1, color = (0,0,0)):
        self.drawn_offset = sp.global_offset.copy()
        self.drawn_scaler = sp.global_scaler

        self.sp = sp
        self.scrn = sp.scrn
        self.lst = sp.shapes
        self.size = size
        self.color = (0,0,0)
        self.offset = [0,0]
        self.points = np.empty((0,2))

        self.transformed_pointer = self.points.copy()
        self.transformed_offset = self.drawn_offset
        self.transformed_scaler = self.drawn_scaler

        self.action = Action(sp.undo, sp.redo, self.lst, "add", objects=[self])

        self.lst.append(self)

    def update(self):
        if np.size(self.points, axis=0) < 2:
            return


        draw_line(self.scrn, self.points[0], self.points[1], self.size, self.color, self.sp.global_offset, self.sp.global_scaler)

    
    def add_point(self, point):
        # if we have two points already, keep origin
        if np.size(self.points, axis=0) == 2:
            self.points = np.delete(self.points, 1)

        super().add_point(point)

# action for class for storing user actions for undo and redo
class Action:
    def __init__(self, undo, redo, shapes, action, objects = [], args = []):
        undo.append(self)
        # max number of actions stored, required so every object is not stored in memory
        self.max_actions = 100
        if len(undo) > self.max_actions:
            undo.pop(0)

        redo.clear()

        self.redo = redo
        self.undo = undo
        self.shapes = shapes

        self.action = action
        self.objects = objects
        self.args = args

    def undo_action(self):
        self.undo.pop()

        self.redo.append(self)
        if len(self.redo) > self.max_actions:
            self.redo.pop(0)


        if self.action == "move":
            x_offset, y_offset = self.args
            for obj in self.objects:
                obj.move([-x_offset, -y_offset])

        elif self.action == "del":
            for obj in self.objects:
                self.shapes.append(obj)
        elif self.action == "add":
            for obj in self.objects:
                self.shapes.remove(obj)

    def redo_action(self):
        self.redo.pop()

        self.undo.append(self)
        if len(self.undo) > self.max_actions:
            self.undo.pop(0)


        if self.action == "move":
            x_offset, y_offset = self.args
            for obj in self.objects:
                obj.move([x_offset, y_offset])

        elif self.action == "del":
            for obj in self.objects:
                self.shapes.remove(obj)
        elif self.action == "add":
            for obj in self.objects:
                self.shapes.append(obj)