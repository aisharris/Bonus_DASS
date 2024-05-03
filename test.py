import pygame

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH = 1000
HEIGHT = 800
CANVAS_COLOR = (255, 255, 255)
TOOLBAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)
SELECTED_BUTTON_COLOR = (100, 100, 100)
LINE_WIDTH = 3

# Define drawing tools
DRAW_LINE = 1
DRAW_RECT = 2
SELECT_OBJ = 3
SELECT_RADIUS = 4

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
    def __init__(self):
        super().__init__()
        self.radius = 0

    def set_radius(self, radius):
        self.radius = radius

    def draw(self, canvas):
        if self.start_pos and self.end_pos:
            rect_width = abs(self.end_pos[0] - self.start_pos[0])
            rect_height = abs(self.end_pos[1] - self.start_pos[1])
            rect = pygame.Rect(self.start_pos[0], self.start_pos[1], rect_width, rect_height)
            pygame.draw.rect(canvas, self.color, rect, border_radius=self.radius)

# Toolbar class
class Toolbar:
    def __init__(self):
        self.selected_tool = None
        self.selected_color = (0, 0, 0)
        self.selected_object = None
        self.select_button_color = BUTTON_COLOR
        self.radius_button_color = BUTTON_COLOR

    def select_tool(self, tool):
        self.selected_tool = tool

    def select_color(self, color):
        self.selected_color = color
        if self.selected_object:
            self.selected_object.set_color(color)

    def select_object(self, obj):
        self.selected_object = obj

    def draw(self, screen):
        # Draw toolbar buttons
        pygame.draw.rect(screen, TOOLBAR_COLOR, (0, HEIGHT - 100, WIDTH, 100))  # Toolbar area

        draw_line_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_LINE else BUTTON_COLOR
        draw_rect_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_RECT else BUTTON_COLOR
        draw_select_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == SELECT_OBJ else BUTTON_COLOR
        draw_radius_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == SELECT_RADIUS else BUTTON_COLOR

        pygame.draw.rect(screen, draw_line_button_color, (50, HEIGHT - 80, 100, 50))  # Draw Line button
        pygame.draw.rect(screen, draw_rect_button_color, (200, HEIGHT - 80, 100, 50))  # Draw Rectangle button

        # Draw color buttons
        color_buttons_pos = [(350, HEIGHT - 80), (500, HEIGHT - 80), (650, HEIGHT - 80)]
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            pygame.draw.rect(screen, color, (color_buttons_pos[i][0], color_buttons_pos[i][1], 50, 50))

        # Draw select object button
        pygame.draw.rect(screen, draw_select_button_color, (750, HEIGHT - 80, 150, 50))
        select_label = pygame.font.SysFont(None, 20).render("Select Object", True, (0, 0, 0))
        screen.blit(select_label, (765, HEIGHT - 70))

        # Draw radius button
        pygame.draw.rect(screen, draw_radius_button_color, (920, HEIGHT - 80, 50, 50))
        radius_label = pygame.font.SysFont(None, 20).render("R", True, (0, 0, 0))
        screen.blit(radius_label, (935, HEIGHT - 70))

        # Draw labels
        font = pygame.font.SysFont(None, 30)
        line_label = font.render("Draw Line", True, (0, 0, 0))
        rect_label = font.render("Draw Rectangle", True, (0, 0, 0))
        screen.blit(line_label, (60, HEIGHT - 70))
        screen.blit(rect_label, (210, HEIGHT - 70))

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
                        elif 350 <= event.pos[0] < 400:
                            self.toolbar.select_color((255, 0, 0))
                        elif 500 <= event.pos[0] < 550:
                            self.toolbar.select_color((0, 255, 0))
                        elif 650 <= event.pos[0] < 700:
                            self.toolbar.select_color((0, 0, 255))
                        elif 750 <= event.pos[0] < 900 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(SELECT_OBJ)
        
                        elif 920 <= event.pos[0] < 970 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(SELECT_RADIUS)
                        else:
                            self.toolbar.select_button_color = BUTTON_COLOR
                            self.toolbar.radius_button_color = BUTTON_COLOR
                    else:  # Clicked on canvas
                        if (self.toolbar.selected_tool==DRAW_LINE or self.toolbar.selected_tool==DRAW_RECT) and not self.toolbar.selected_object:
                            if self.drawing_object is None:
                                self.drawing_object = Line() if self.toolbar.selected_tool == DRAW_LINE else Rectangle()
                                self.drawing_object.set_start_pos((event.pos[0], event.pos[1] - 100))
                                self.drawing_object.set_color(self.toolbar.selected_color)
                            else:
                                self.drawing_object.set_end_pos((event.pos[0], event.pos[1] - 100))
                                self.objects.append(self.drawing_object)
                                self.drawing_object = None
                        elif self.toolbar.selected_tool==SELECT_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            print(self.toolbar.selected_object)
                            self.toolbar.selected_object.set_color(self.toolbar.selected_color)

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

    def get_selected_object(self, pos):
        for obj in reversed(self.objects):
            if isinstance(obj, Rectangle):
                print (obj.start_pos,obj.end_pos)
                rect = pygame.Rect(obj.start_pos[0], obj.start_pos[1], abs(obj.end_pos[0] - obj.start_pos[0]), abs(obj.end_pos[1] - obj.start_pos[1]))
                if rect.collidepoint(pos):
                    return obj
            elif isinstance(obj, Line):
                print (obj.start_pos,obj.end_pos)
                if obj.start_pos[0] <= pos[0] <= obj.end_pos[0] and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]:
                    return obj
        return None

# Run the application
app = DrawingApp()
app.run()
