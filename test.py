import pygame

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH = 1200
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
DELETE_OBJ = 4
MOVE_OBJ = 5
MOVE_OBJ2 = 6
COPY = 7
PASTE = 8
ROUNDED_SELECT=9
INCREASE_RADIUS=10
DECREASE_RADIUS=11

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

    def move(self, pos):
        if self.start_pos:
            if self.end_pos:
                delta_x = pos[0] - self.start_pos[0]
                delta_y = pos[1] - self.start_pos[1]
                self.start_pos = pos
                self.end_pos = (self.end_pos[0] + delta_x, self.end_pos[1] + delta_y)
            else:
                self.start_pos = pos

# Line class
class Line(Object):
    def draw(self, canvas):
        if self.start_pos and self.end_pos:
            pygame.draw.line(canvas, self.color, self.start_pos, self.end_pos, LINE_WIDTH)

class Rectangle(Object):
    def __init__(self, rounded=False, radius=0):
        super().__init__()
        self.rounded = rounded
        self.radius = radius

    def set_radius(self, radius):
        self.radius = radius

    def draw(self, canvas):
        if self.start_pos and self.end_pos:
            if self.rounded:
                rect_width = abs(self.end_pos[0] - self.start_pos[0])
                rect_height = abs(self.end_pos[1] - self.start_pos[1])
                rect = pygame.Rect(self.start_pos[0], self.start_pos[1], rect_width, rect_height)
                pygame.draw.rect(canvas, self.color, rect, border_radius=self.radius)
            else:
                pygame.draw.rect(canvas, self.color, (self.start_pos, (self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])))


# Toolbar class
class Toolbar:
    def __init__(self):
        self.selected_tool = None
        self.selected_color = (0, 0, 0)
        self.selected_object = None
        self.select_button_color = BUTTON_COLOR
        self.radius_button_color = BUTTON_COLOR
        self.rounded_button_color = BUTTON_COLOR
        self.increase_radius_button_color = BUTTON_COLOR
        self.decrease_radius_button_color = BUTTON_COLOR

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
        draw_delete_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DELETE_OBJ else BUTTON_COLOR
        draw_move_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == MOVE_OBJ else BUTTON_COLOR
        draw_copy_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == COPY or self.selected_tool == PASTE else BUTTON_COLOR
        draw_rounded_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == ROUNDED_SELECT else BUTTON_COLOR
        increase_rounded_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == INCREASE_RADIUS else BUTTON_COLOR
        decrease_rounded_button_color = SELECTED_BUTTON_COLOR if self.selected_tool == DECREASE_RADIUS else BUTTON_COLOR

        # Button widths
        button_width = 60  # Reduced button width
        button_height = 50

        # Draw Line button
        pygame.draw.rect(screen, draw_line_button_color, (20, HEIGHT - 80, button_width, button_height))

        # Draw Rectangle button
        pygame.draw.rect(screen, draw_rect_button_color, (100, HEIGHT - 80, button_width, button_height))

        # Draw color buttons
        color_buttons_pos = [(180, HEIGHT - 80), (260, HEIGHT - 80), (340, HEIGHT - 80)]  # Adjusted positions
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            pygame.draw.rect(screen, color, (color_buttons_pos[i][0], color_buttons_pos[i][1], button_height, button_height))

        # Draw select object button
        pygame.draw.rect(screen, draw_select_button_color, (440, HEIGHT - 80, button_width, button_height))  # Adjusted position
        select_label = pygame.font.SysFont(None, 20).render("Select", True, (0, 0, 0))  # Shortened label
        screen.blit(select_label, (455, HEIGHT - 70))  # Adjusted position

        # Draw delete object button
        pygame.draw.rect(screen, draw_delete_button_color, (520, HEIGHT - 80, button_width, button_height))  # Adjusted position
        delete_label = pygame.font.SysFont(None, 20).render("X", True, (0, 0, 0))
        screen.blit(delete_label, (535, HEIGHT - 70))

        # Draw move object button
        pygame.draw.rect(screen, draw_move_button_color, (600, HEIGHT - 80, button_width, button_height))  # Adjusted position
        move_label = pygame.font.SysFont(None, 20).render("Move", True, (0, 0, 0))  # Shortened label
        screen.blit(move_label, (615, HEIGHT - 70))  # Adjusted position

        # Draw copy object button
        pygame.draw.rect(screen, draw_copy_button_color, (680, HEIGHT - 80, button_width, button_height))  # Adjusted position
        copy_label = pygame.font.SysFont(None, 20).render("Copy", True, (0, 0, 0))  # Added copy button
        screen.blit(copy_label, (695, HEIGHT - 70))  # Adjusted position

        # Draw select rounded edges button
        pygame.draw.rect(screen, draw_rounded_button_color, (760, HEIGHT - 80, button_width, button_height))  # Adjusted position
        rounded_label = pygame.font.SysFont(None, 15).render("Rounded", True, (0, 0, 0))  # Shortened label
        screen.blit(rounded_label, (765, HEIGHT - 90))  # Adjusted position

        # Draw increase radius button
        pygame.draw.rect(screen, increase_rounded_button_color, (840, HEIGHT - 80, button_width, button_height))  # Adjusted position
        increase_label = pygame.font.SysFont(None, 15).render("+", True, (0, 0, 0))
        screen.blit(increase_label, (865, HEIGHT - 70))

        # Draw decrease radius button
        pygame.draw.rect(screen, decrease_rounded_button_color, (920, HEIGHT - 80, button_width, button_height))  # Adjusted position
        decrease_label = pygame.font.SysFont(None, 15).render("-", True, (0, 0, 0))
        screen.blit(decrease_label, (945, HEIGHT - 70))


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

    def get_selected_object(self, pos):
        for obj in reversed(self.objects):
            if isinstance(obj, Rectangle):
                rect = pygame.Rect(obj.start_pos[0], obj.start_pos[1], abs(obj.end_pos[0] - obj.start_pos[0]), abs(obj.end_pos[1] - obj.start_pos[1]))
                if rect.collidepoint(pos):
                    return obj
            elif isinstance(obj, Line):
                if obj.start_pos[0] <= pos[0] <= obj.end_pos[0] and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]:
                    return obj
        return None

    def copy_object(self, obj):
        if isinstance(obj, Rectangle):
            copied_obj = Rectangle()
        elif isinstance(obj, Line):
            copied_obj = Line()
        else:
            return None

        copied_obj.set_start_pos(obj.start_pos)
        copied_obj.set_end_pos(obj.end_pos)
        copied_obj.set_color(obj.color)
        return copied_obj

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if HEIGHT - 100 <= event.pos[1] < HEIGHT:  # Check if toolbar area clicked
                        # Determine which tool was selected
                        if 20 <= event.pos[0] < 80:
                            self.toolbar.select_tool(DRAW_LINE)
                        elif 100 <= event.pos[0] < 160:
                            self.toolbar.select_tool(DRAW_RECT)
                        elif 180 <= event.pos[0] < 240:
                            self.toolbar.select_color((255, 0, 0))
                        elif 260 <= event.pos[0] < 320:
                            self.toolbar.select_color((0, 255, 0))
                        elif 340 <= event.pos[0] < 400:
                            self.toolbar.select_color((0, 0, 255))
                        elif 440 <= event.pos[0] < 500 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(SELECT_OBJ)
                        elif 520 <= event.pos[0] < 580 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(DELETE_OBJ)
                        elif 600 <= event.pos[0] < 660 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(MOVE_OBJ)
                        elif 680 <= event.pos[0] < 740 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(COPY)
                        elif 760 <= event.pos[0] < 820 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(ROUNDED_SELECT)
                        elif 840 <= event.pos[0] < 900 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            if isinstance(self.toolbar.selected_object, Rectangle):
                                self.toolbar.selected_object.rounded=True
                                self.toolbar.selected_object.radius += 5
                                print("After increase:", self.toolbar.selected_object.radius)
                                self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                for obj in self.objects:
                                    obj.draw(self.canvas)
                        elif 920 <= event.pos[0] < 980 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            if isinstance(self.toolbar.selected_object, Rectangle) and self.toolbar.selected_object.rounded:
                                if self.toolbar.selected_object.radius >= 5:
                                    self.toolbar.selected_object.radius -= 5
                                    self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                    for obj in self.objects:
                                        obj.draw(self.canvas)
                        else:
                            self.toolbar.select_button_color = BUTTON_COLOR
                            self.toolbar.radius_button_color = BUTTON_COLOR
                    else:  # Clicked on canvas
                        if (self.toolbar.selected_tool == DRAW_LINE or self.toolbar.selected_tool == DRAW_RECT) and not self.toolbar.selected_object:
                            if self.drawing_object is None:
                                self.drawing_object = Line() if self.toolbar.selected_tool == DRAW_LINE else Rectangle()
                                self.drawing_object.set_start_pos((event.pos[0], event.pos[1] - 100))
                                self.drawing_object.set_color(self.toolbar.selected_color)
                            else:
                                self.drawing_object.set_end_pos((event.pos[0], event.pos[1] - 100))
                                self.objects.append(self.drawing_object)
                                self.drawing_object = None
                        elif self.toolbar.selected_tool == SELECT_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            if not self.toolbar.selected_object:
                                continue
                            self.toolbar.selected_object.set_color(self.toolbar.selected_color)
                            self.toolbar.selected_object = None
                        elif self.toolbar.selected_tool == DELETE_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            if not self.toolbar.selected_object:
                                continue
                            self.objects.remove(self.toolbar.selected_object)
                            self.toolbar.selected_object = None
                            self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                            # Redraw objects
                            for obj in self.objects:
                                obj.draw(self.canvas)
                        elif self.toolbar.selected_tool == MOVE_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            if not self.toolbar.selected_object:
                                continue
                            self.toolbar.selected_tool = MOVE_OBJ2
                        elif self.toolbar.selected_tool == MOVE_OBJ2:
                            self.toolbar.selected_object.move(event.pos)
                            self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                            # Redraw objects
                            for obj in self.objects:
                                obj.draw(self.canvas)
                        elif self.toolbar.selected_tool == COPY:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            if not self.toolbar.selected_object:
                                continue
                            self.toolbar.selected_tool = PASTE
                        elif self.toolbar.selected_tool == PASTE:
                            copied_obj = self.copy_object(self.toolbar.selected_object)
                            delta_x = event.pos[0] - copied_obj.start_pos[0]
                            delta_y = event.pos[1] - copied_obj.start_pos[1]
                            copied_obj.start_pos = event.pos
                            copied_obj.end_pos = (copied_obj.end_pos[0] + delta_x, copied_obj.end_pos[1] + delta_y)
                            copied_obj.set_start_pos(event.pos)
                            self.objects.append(copied_obj)
                            self.drawing_object = None
                            
                        elif self.toolbar.selected_tool== ROUNDED_SELECT:
                            self.toolbar.selected_object = self.get_selected_object(event.pos)
                            


            #print(self.toolbar.selected_tool)
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

# Run the application
app = DrawingApp()
app.run()
