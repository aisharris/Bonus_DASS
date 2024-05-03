import pygame

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH = 800
HEIGHT = 600
CANVAS_COLOR = (255, 255, 255)
TOOLBAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)
SELECTED_BUTTON_COLOR = (100, 100, 100)
LINE_WIDTH = 3

# Define drawing tools
DRAW_LINE = 1
DRAW_RECT = 2
ENLARGE_RECT = 3

# Object class
class Object:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.color = (0, 0, 0)

    def set_start_pos(self, pos):
        self.start_pos = pos

    def set_end_pos(self, pos):
        self.end_pos = pos

    def set_color(self, color):
        self.color = color

    def draw(self, canvas):
        pass

# Line class
class Line(Object):
    def draw(self, canvas):
        if self.start_pos and self.end_pos:
            pygame.draw.line(canvas, self.color, self.start_pos, self.end_pos, LINE_WIDTH)

# Rectangle class
class Rectangle(Object):
    def draw(self, canvas):
        if self.start_pos and self.end_pos:
            pygame.draw.rect(canvas, self.color, (min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]), abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1] - self.start_pos[1])))

    def enlarge(self, delta_x, delta_y):
        self.end_pos = (self.end_pos[0] + delta_x, self.end_pos[1] + delta_y)

# Toolbar class
class Toolbar:
    def __init__(self):
        self.selected_tool = None
        self.selected_color = (0, 0, 0)

    def select_tool(self, tool):
        self.selected_tool = tool

    def select_color(self, color):
        self.selected_color = color

    def draw(self, screen):
        # Draw toolbar buttons
        pygame.draw.rect(screen, TOOLBAR_COLOR, (0, HEIGHT - 100, WIDTH, 100))  # Toolbar area

        draw_line_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_LINE else BUTTON_COLOR
        draw_rect_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_RECT else BUTTON_COLOR
        enlarge_rect_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == ENLARGE_RECT else BUTTON_COLOR

        pygame.draw.rect(screen, draw_line_button_color, (50, HEIGHT - 80, 100, 50))  # Draw Line button
        pygame.draw.rect(screen, draw_rect_button_color, (200, HEIGHT - 80, 100, 50))  # Draw Rectangle button
        pygame.draw.rect(screen, enlarge_rect_button_color, (350, HEIGHT - 80, 150, 50))  # Enlarge Rectangle button

        # Draw color buttons
        color_buttons_pos = [(520, HEIGHT - 80), (640, HEIGHT - 80), (760, HEIGHT - 80)]
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            pygame.draw.rect(screen, color, (color_buttons_pos[i][0], color_buttons_pos[i][1], 50, 50))

        # Draw labels
        font = pygame.font.SysFont(None, 30)
        line_label = font.render("Draw Line", True, (0, 0, 0))
        rect_label = font.render("Draw Rectangle", True, (0, 0, 0))
        enlarge_label = font.render("Enlarge Rectangle", True, (0, 0, 0))
        screen.blit(line_label, (60, HEIGHT - 70))
        screen.blit(rect_label, (210, HEIGHT - 70))
        screen.blit(enlarge_label, (360, HEIGHT - 70))

# Main game class
class DrawingApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Canvas with Toolbar")

        self.canvas = pygame.Surface((WIDTH, HEIGHT - 100))  # Create a surface for the canvas
        self.canvas.fill(CANVAS_COLOR)

        self.toolbar = Toolbar()
        self.objects = []

        self.drawing_object = None

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if HEIGHT - 100 <= event.pos[1] < HEIGHT:  # Check if toolbar area clicked
                        # Determine which tool was selected
                        if 50 <= event.pos[0] < 150:
                            self.toolbar.select_tool(DRAW_LINE)
                        elif 200 <= event.pos[0] < 300:
                            self.toolbar.select_tool(DRAW_RECT)
                        elif 350 <= event.pos[0] < 500:
                            self.toolbar.select_tool(ENLARGE_RECT)
                        elif 520 <= event.pos[0] < 570:
                            self.toolbar.select_color((255, 0, 0))
                        elif 640 <= event.pos[0] < 690:
                            self.toolbar.select_color((0, 255, 0))
                        elif 760 <= event.pos[0] < 810:
                            self.toolbar.select_color((0, 0, 255))
                    else:  # Clicked on canvas
                        if self.toolbar.selected_tool:
                            if self.toolbar.selected_tool == ENLARGE_RECT:
                                self.enlarge_selected_rectangle()
                            else:
                                if self.drawing_object is None:
                                    self.drawing_object = Line() if self.toolbar.selected_tool == DRAW_LINE else Rectangle()
                                    self.drawing_object.set_start_pos((event.pos[0], event.pos[1] - 100))
                                    self.drawing_object.set_color(self.toolbar.selected_color)
                                else:
                                    self.drawing_object.set_end_pos((event.pos[0], event.pos[1] - 100))
                                    self.objects.append(self.drawing_object)
                                    self.drawing_object = None

            # Fill the screen with the canvas and toolbar
            self.screen.fill((0, 0, 0))  # Clear the screen

            # Draw toolbar
            self.toolbar.draw(self.screen)

            # Draw objects
            for obj in self.objects:
                obj.draw(self.canvas)

            # Draw the current drawing object
            if self.drawing_object:
                self.drawing_object.draw(self.canvas)

            # Blit the canvas surface onto the screen
            self.screen.blit(self.canvas, (0, 0))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

    def enlarge_selected_rectangle(self):
        for obj in self.objects:
            if isinstance(obj, Rectangle):
                if obj.start_pos[0] <= pygame.mouse.get_pos()[0] <= obj.end_pos[0] and obj.start_pos[1] <= pygame.mouse.get_pos()[1] <= obj.end_pos[1]:
                    obj.enlarge(10, 10)

# Run the application
app = DrawingApp()
app.run()
