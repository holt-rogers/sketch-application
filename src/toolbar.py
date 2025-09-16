from ui_elements import Panel, Button, Text
import pygame


# Main UI for the application
class Toolbar:
    def __init__(self, scrn, sketchpad):
        self.scrn = scrn
        self.sketchpad = sketchpad

        self.scrn_width, self.scrn_height = scrn.get_size()
    
    
        side_border = 2
        top_border = 10
        button_padding = 40
        button_count = 7
        

        self.height = top_border*2 + button_padding*(button_count-1) + 28
        self.width = 32

        self.pos_x = 4
        self.pos_y = abs((self.scrn_height - self.height) / 2)

        self.main_menu = Panel(scrn, (self.pos_x,self.pos_y), (self.width, self.height))

        self.select_image = (63,138,238)
        self.black = (0,0,0)

        self.hovered_grey = 240

        self.keys = {}

    

        select_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border], [28, 28])
        select_button.add_graphic("icons/cursor.png")
        select_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        select_button.add_action(self.select_select)
        self.main_menu.add_button(select_button)

        pen_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding], [28, 28])
        pen_button.add_graphic("icons/pen.png")
        pen_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        pen_button.add_action(self.pen_select)
        self.main_menu.add_button(pen_button)

        shapes_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding*2], [28, 28])
        shapes_button.add_graphic("icons/shapes.png")
        shapes_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        shapes_button.add_action(self.shape_select)
        self.main_menu.add_button(shapes_button)

        file_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding*3], [28, 28])
        file_button.add_graphic("icons/file.png")
        file_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        file_button.add_action(self.file_select)
        self.main_menu.add_button(file_button)

        setting_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding*4], [28, 28])
        setting_button.add_graphic("icons/settings.png")
        setting_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        setting_button.add_action(self.settings_select)
        self.main_menu.add_button(setting_button)

        undo_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding*5], [28, 28])
        undo_button.add_graphic("icons/undo.png")
        undo_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        undo_button.add_action(self.sketchpad.undo_action)
        self.main_menu.add_button(undo_button)

        redo_button = Button(scrn, [self.pos_x + side_border, self.pos_y + top_border + button_padding*6], [28, 28])
        redo_button.add_graphic("icons/redo.png")
        redo_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        redo_button.add_action(self.sketchpad.redo_action)
        self.main_menu.add_button(redo_button)

        # other menu panels
        side_padding = 10
        self.side_panels = []
        
        sub_menu_x = self.pos_x + self.width + side_padding

        # TODO: Create color selection panel

        # create  tool panel
        tool_y = self.pos_y + button_padding*2
        self.shape_selection = Panel(scrn, (sub_menu_x,tool_y), (self.width, top_border + button_padding*3))
        self.side_panels.append(self.shape_selection)

        line_button = Button(scrn, [sub_menu_x + side_border, tool_y + top_border], [28, 28])
        line_button.add_graphic("icons/line.png")
        line_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        line_button.add_action(self.line_select)
        self.shape_selection.add_button(line_button)

        rect_button = Button(scrn, [sub_menu_x + side_border, tool_y + top_border + button_padding], [28, 28])
        rect_button.add_graphic("icons/rect.png")
        rect_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        rect_button.add_action(self.rect_select)
        self.shape_selection.add_button(rect_button)


        circle_button = Button(scrn, [sub_menu_x + side_border, tool_y + top_border + button_padding*2], [28, 28])
        circle_button.add_graphic("icons/circle.png")
        circle_button.add_hovered_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))
        circle_button.add_action(self.circle_select)
        self.shape_selection.add_button(circle_button)
        self.shape_selection.hide()



        # shortcuts
        self.old_keys = pygame.key.get_pressed()
        self.shortcuts = [
            [[pygame.K_s], self.select_select],
            [[pygame.K_p], self.pen_select],
            [[pygame.K_LCTRL, pygame.K_z], self.sketchpad.undo_action],
            [[pygame.K_LCTRL, pygame.K_y], self.sketchpad.redo_action],
            [[pygame.K_l], self.line_select],
            [[pygame.K_r], self.rect_select],
            [[pygame.K_c], self.circle_select]
        ]


    def update(self):
        new_width, new_height = self.scrn.get_size()
        if new_height != self.scrn_height:
            self.scrn_height = new_height
            pos_y = abs((self.scrn_height - self.height) / 2)
            diff = pos_y-self.pos_y

            for b in self.main_menu.get_buttons():
                b.move([0, diff])

            self.pos_y = pos_y
            self.main_menu.change_rect((self.pos_x, self.pos_y, self.width, self.height))

        self.main_menu.update()
        for panel in self.side_panels:
            panel.update()

        keys = self.keys
        # shortcuts
        for s in self.shortcuts:
            buttons, action = s

            pushed_down = False
            shortcut_fufilled = True
            for b in buttons:
                if not keys[b]:
                    shortcut_fufilled = False
                    break

                if keys[b] and not self.old_keys[b]:
                    pushed_down = True
            
            if pushed_down and shortcut_fufilled:
                action()
        

        self.old_keys = keys 


    def update_input(self, keys):
        self.keys = keys

    def select_tool(self, tool):
        for panel in self.side_panels:
            panel.hide()

        if self.sketchpad.tool == tool:
            return
        
        if self.sketchpad.tool != None:
            self.main_menu.buttons[self.sketchpad.tool].replace_image_color(self.select_image, self.black)
            self.main_menu.buttons[self.sketchpad.tool].add_background(None)

        self.main_menu.buttons[tool].replace_image_color(self.black, self.select_image)
        self.main_menu.buttons[tool].add_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))


        self.sketchpad.change_tool(tool)
    
    def select_shape(self, shape):
        if self.sketchpad.shape == shape:
            return
        
        if self.sketchpad.shape != None:
            self.shape_selection.buttons[self.sketchpad.shape].replace_image_color(self.select_image, self.black)
            self.shape_selection.buttons[self.sketchpad.shape].add_background(None)

        self.shape_selection.buttons[shape].replace_image_color(self.black, self.select_image)
        self.shape_selection.buttons[shape].add_background((self.hovered_grey, self.hovered_grey, self.hovered_grey))


        self.sketchpad.change_shape(shape)


    def select_select(self):
        self.select_tool(0)

    def pen_select(self):
        self.select_tool(1)

    def shape_select(self):
        shown = self.shape_selection.shown()
        self.select_tool(2)

        self.shape_selection.hide(shown)

    def file_select(self):
        self.select_tool(3)

    def settings_select(self):
        self.select_tool(4)
    
    def line_select(self):
        self.select_tool(2)
        self.select_shape(0)

    def rect_select(self):
        self.select_tool(2)
        self.select_shape(1)

    def circle_select(self):
        self.select_tool(2)
        self.select_shape(2)