from drawings import draw_line
from constants import grid_lines_col, bg_color

class GridLines:
    def __init__(self, sp):
        self.sp = sp
        self.scrn = sp.scrn
        self.max_space = 200
        self.min_space = 10
        self.spacing = 40

    def update(self):
        # create big lines
        size = self.scrn.get_size()

        max_x = size[0]
        max_y = size[1]

        line_space = self.spacing * self.sp.global_scaler
        cell_space = line_space * 4

        scaler = self.max_space / self.min_space
        while line_space < self.min_space:
            line_space *= scaler
        
        while line_space > self.max_space:
            line_space /= scaler
        
        cell_space = line_space

        if (line_space - self.min_space) < (self.max_space - self.min_space) / 2:
            cell_space *= 4
        else:
            line_space /= 4

        self.line_col = ()
        self.cell_col = ()

        real_min = min((self.max_space + (self.max_space - self.min_space)/2) * 4, self.min_space)
        real_max = max((self.max_space + (self.max_space - self.min_space)/2) * 4, self.max_space)

        for i in range(3):
            self.line_col += (grid_lines_col[i] - (grid_lines_col[i] - bg_color[i]) * (real_max - line_space)/(real_max - self.min_space),)
            self.cell_col += (grid_lines_col[i] - (grid_lines_col[i] - bg_color[i]) * (real_max - cell_space)/(real_max - self.min_space),)
    

        # draw y lines
        offset_y = (max_y/2) % line_space + (self.sp.global_offset[1] * self.sp.global_scaler) % line_space
        offset_x = (max_x/2) % line_space + (self.sp.global_offset[0] * self.sp.global_scaler) % line_space
        for i in range(int(max_y / line_space)):
            draw_line(self.scrn, (0,line_space*i + offset_y), (max_x,line_space*i + offset_y), 1, self.line_col)

        # draw x lines
        for i in range(int(max_x / line_space)):
            draw_line(self.scrn, (line_space*i + offset_x,0), (line_space*i + offset_x,max_y), 1, self.line_col)

        offset_y = (max_y/2) % cell_space + (self.sp.global_offset[1] * self.sp.global_scaler) % cell_space
        offset_x = (max_x/2) % cell_space + (self.sp.global_offset[0] * self.sp.global_scaler) % cell_space
        # draw y lines
        for i in range(int(max_y / cell_space)):
            draw_line(self.scrn, (0,cell_space*i + offset_y), (max_x,cell_space*i + offset_y), 1, self.cell_col)

        # draw x lines
        for i in range(int(max_x / cell_space)):
            draw_line(self.scrn, (cell_space*i + offset_x,0), (cell_space*i + offset_x,max_y), 1, self.cell_col)