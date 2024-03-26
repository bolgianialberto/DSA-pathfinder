from controllers.instance_generator import instance_generator
from controllers.grid_generator import grid_generator
from algorithm.reach_goal import reach_goal
from views.grid_visualization import print_gui_grid
from views.path_visualization import print_gui_paths, print_gui_path
from views.checkbox import Checkbox
from models.path import Path
import pygame
from tkinter import messagebox

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (211, 211, 211)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230) 

WIDTH = 1000
HEIGHT = 700

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
PADDING_LEFT = 40
PADDING_TOP = 40

BUTTON_SURFACE_WIDTH = 200

CUSTOM_FONT = 'Lato-Regular.ttf'

BOX_WIDTH = 50
BOX_HEIGHT = 20

class Gui():
    
    def __init__(self):
        self.grid = None
        self.instance = None
        self.new_path = None
    
    def run(self, rows, cols, traversability, cluster_factor, n_agents, cell_size):
        global generate_button_clicked
        global add_agents_button_clicked

        generate_button_clicked = False
        add_agents_button_clicked = False

        rows_input_value = ''
        cols_input_value = ''
        fcr_input_value = ''
        agglo_input_value = ''
        na_input_value = ''

        rows_active = False
        cols_active = False
        fcr_active = False
        agglo_active = False
        na_active = False

        rows_input_box_rect = pygame.Rect(PADDING_LEFT + 100, PADDING_TOP, BOX_WIDTH, BOX_HEIGHT)
        cols_input_box_rect = pygame.Rect(PADDING_LEFT + 100, PADDING_TOP + 30, BOX_WIDTH, BOX_HEIGHT)
        fcr_input_box_rect = pygame.Rect(PADDING_LEFT + 100, PADDING_TOP + 60, BOX_WIDTH, BOX_HEIGHT)
        agglo_input_box_rect = pygame.Rect(PADDING_LEFT + 100, PADDING_TOP + 90, BOX_WIDTH, BOX_HEIGHT)
        na_input_box_rect = pygame.Rect(PADDING_LEFT + 100, PADDING_TOP + 210, BOX_WIDTH, BOX_HEIGHT)
    
        # Initialize pygame
        pygame.init()

        # Set up the display
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Path Finder")
        screen.fill(WHITE)

        button_surface = pygame.Surface((BUTTON_SURFACE_WIDTH, HEIGHT))
        button_surface.fill(WHITE)
        grid_surface = pygame.Surface((WIDTH - BUTTON_SURFACE_WIDTH, HEIGHT))
        grid_surface.fill(WHITE)

        # Font
        font = pygame.font.Font(CUSTOM_FONT, 15)

        # generate button
        generate_button_rect = pygame.Rect(PADDING_LEFT, PADDING_TOP + 120, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(button_surface, BLUE, generate_button_rect)
        text = font.render("Generate", True, WHITE)
        text_rect = text.get_rect(center=generate_button_rect.center)
        button_surface.blit(text, text_rect)

        # add agents button
        add_agents_button_rect = pygame.Rect(PADDING_LEFT, PADDING_TOP + 240, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(button_surface, BLUE, add_agents_button_rect)
        text = font.render("Add Agents", True, WHITE)
        text_rect = text.get_rect(center=add_agents_button_rect.center)
        button_surface.blit(text, text_rect)

        checkbox_rg = Checkbox(button_surface, 140, 220, label="use reach goal")

        # add new button
        add_new_button_rect = pygame.Rect(PADDING_LEFT, PADDING_TOP + 360, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(button_surface, BLUE, add_new_button_rect)
        text = font.render("Add New", True, WHITE)
        text_rect = text.get_rect(center=add_new_button_rect.center)
        button_surface.blit(text, text_rect)

        # Main loop
        while True:
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                checkbox_rg.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if rows_input_box_rect.collidepoint(x, y):
                        rows_active = True
                        cols_active = False
                        fcr_active = False
                        agglo_active = False
                        na_active = False
                    
                    if cols_input_box_rect.collidepoint(x, y):
                        cols_active = True
                        rows_active = False
                        fcr_active = False
                        agglo_active = False
                        na_active = False
                    
                    if fcr_input_box_rect.collidepoint(x, y):
                        fcr_active = True
                        cols_active = False
                        rows_active = False
                        agglo_active = False
                        na_active = False

                    if agglo_input_box_rect.collidepoint(x, y):
                        agglo_active = True
                        fcr_active = False
                        cols_active = False
                        rows_active = False
                        na_active = False

                    if na_input_box_rect.collidepoint(x, y):
                        na_active = True
                        fcr_active = False
                        cols_active = False
                        rows_active = False
                        agglo_active = False

                    if generate_button_rect.collidepoint(x, y):
                        generate_button_clicked = True
                        add_agents_button_clicked = False

                        rows_I = int(rows_input_value) if rows_input_value else rows
                        cols_I = int(cols_input_value) if cols_input_value else cols
                        traversability_I = float(fcr_input_value) if fcr_input_value else traversability
                        cluster_factor_I = float(agglo_input_value) if agglo_input_value else cluster_factor
                    
                        self.grid = grid_generator(rows_I, cols_I, traversability_I, cluster_factor_I)
                        print_gui_grid(self.grid, grid_surface, cell_size, PADDING_LEFT, PADDING_TOP)

                    if add_agents_button_rect.collidepoint(x, y) and generate_button_clicked and not add_agents_button_clicked:
                        add_agents_button_clicked = True
                        use_reach_goal = checkbox_rg.checked

                        n_agents_I = int(na_input_value) if na_input_value else n_agents

                        self.instance = instance_generator(self.grid, n_agents_I, use_reach_goal)
                        paths = self.instance.get_paths()
                        if not paths:
                            messagebox.showinfo("Attention!", "No paths found! Please generate a new grid.")

                        print_gui_paths(paths, grid_surface, cell_size, PADDING_LEFT, PADDING_TOP)

                    if add_new_button_rect.collidepoint(x, y) and add_agents_button_clicked:
                        self.new_path = reach_goal(self.instance.get_graph(), self.instance.get_init(), self.instance.get_goal(), self.instance.get_paths(), Path.get_goal_last_instant(), self.instance.get_max())

                        if self.new_path:
                            print_gui_path(self.new_path, grid_surface, cell_size, PADDING_LEFT, PADDING_TOP)
                        else:
                            messagebox.showinfo("Error", "Impossible to find a path!")
                    
                if event.type == pygame.KEYDOWN:
                    if rows_active:
                        if event.key == pygame.K_BACKSPACE:
                            rows_input_value = rows_input_value[:-1]
                        else:
                            rows_input_value += event.unicode

                    if cols_active:
                        if event.key == pygame.K_BACKSPACE:
                            cols_input_value = cols_input_value[:-1]
                        else:
                            cols_input_value += event.unicode

                    if fcr_active:
                        if event.key == pygame.K_BACKSPACE:
                            fcr_input_value = fcr_input_value[:-1]
                        else:
                            fcr_input_value += event.unicode

                    if agglo_active:
                        if event.key == pygame.K_BACKSPACE:
                            agglo_input_value = agglo_input_value[:-1]
                        else:
                            agglo_input_value += event.unicode
                    
                    if na_active:
                        if event.key == pygame.K_BACKSPACE:
                            na_input_value = na_input_value[:-1]
                        else:
                            na_input_value += event.unicode
            
            color = LIGHT_BLUE if rows_active else LIGHT_GREY
            draw_text("rows:", font, button_surface, PADDING_LEFT, PADDING_TOP)
            draw_input_box(button_surface, color, font, rows_input_value, rows_input_box_rect)
            
            color = LIGHT_BLUE if cols_active else LIGHT_GREY
            draw_text("cols:", font, button_surface, PADDING_LEFT, PADDING_TOP + 30)
            draw_input_box(button_surface, color, font, cols_input_value, cols_input_box_rect) 

            color = LIGHT_BLUE if fcr_active else LIGHT_GREY
            draw_text("free cell ratio:", font, button_surface, PADDING_LEFT, PADDING_TOP + 60)
            draw_input_box(button_surface, color, font, fcr_input_value, fcr_input_box_rect)  

            color = LIGHT_BLUE if agglo_active else LIGHT_GREY
            draw_text("cluster factor:", font, button_surface, PADDING_LEFT, PADDING_TOP + 90)
            draw_input_box(button_surface, color, font, agglo_input_value, agglo_input_box_rect)

            color = LIGHT_BLUE if na_active else LIGHT_GREY
            draw_text("n° of agents:", font, button_surface, PADDING_LEFT, PADDING_TOP + 210)
            draw_input_box(button_surface, color, font, na_input_value, na_input_box_rect)

            screen.blit(button_surface, (0, 0))  # Posiziona la superficie dei bottoni a sinistra
            screen.blit(grid_surface, (BUTTON_SURFACE_WIDTH, 0))

            checkbox_rg.draw()

            pygame.display.flip()
                        
def draw_input_box(layout, color, font, input_value, input_rect):
    pygame.draw.rect(layout, color, input_rect)
    text_surface = font.render(input_value, True, BLACK)
    layout.blit(text_surface, (input_rect.left + 1, input_rect.top + 1))

def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)