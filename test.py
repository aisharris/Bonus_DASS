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
SELECT_GROUP=12
GROUP_OBJECTS=13
UNGROUP_OBJECTS=14

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
        select_group_button_colour = SELECTED_BUTTON_COLOR if self.selected_tool == SELECT_GROUP else BUTTON_COLOR

        # Button widths
        button_width = 50  # Decreased button width
        button_height = 40  # Decreased button height

        # Draw Line button
        pygame.draw.rect(screen, draw_line_button_color, (20, HEIGHT - 80, button_width, button_height))
        draw_line_label = pygame.font.SysFont(None, 20).render("Line", True, (0, 0, 0))  # Increased text size
        screen.blit(draw_line_label, (30, HEIGHT - 85))  # Adjusted position
    
        # Draw Rectangle button
        pygame.draw.rect(screen, draw_rect_button_color, (90, HEIGHT - 80, button_width, button_height))  # Adjusted position
        draw_rect_label = pygame.font.SysFont(None, 20).render("Rect", True, (0, 0, 0))  # Increased text size
        screen.blit(draw_rect_label, (100, HEIGHT - 85))  # Adjusted position

        # Draw color buttons
        color_buttons_pos = [(160, HEIGHT - 80), (230, HEIGHT - 80), (300, HEIGHT - 80), (370, HEIGHT - 80)]  # Adjusted positions
        color_labels = ["Red", "Green", "Blue", "Black"]  # Color labels
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]):
            pygame.draw.rect(screen, color, (color_buttons_pos[i][0], color_buttons_pos[i][1], button_height, button_height))
            color_label = pygame.font.SysFont(None, 20).render(color_labels[i], True, (0, 0, 0))  # Increased text size
            screen.blit(color_label, (color_buttons_pos[i][0] + 5, HEIGHT - 85))  # Adjusted position

        # Draw select object button
        pygame.draw.rect(screen, draw_select_button_color, (450, HEIGHT - 80, button_width, button_height))  # Adjusted position
        select_label = pygame.font.SysFont(None, 20).render("Select", True, (0, 0, 0))  # Increased text size
        screen.blit(select_label, (460, HEIGHT - 85))  # Adjusted position

        # Draw delete object button
        pygame.draw.rect(screen, draw_delete_button_color, (520, HEIGHT - 80, button_width, button_height))  # Adjusted position
        delete_label = pygame.font.SysFont(None, 20).render("Delete", True, (0, 0, 0))  # Increased text size
        screen.blit(delete_label, (530, HEIGHT - 85))  # Adjusted position

        # Draw move object button
        pygame.draw.rect(screen, draw_move_button_color, (590, HEIGHT - 80, button_width, button_height))  # Adjusted position
        move_label = pygame.font.SysFont(None, 20).render("Move", True, (0, 0, 0))  # Increased text size
        screen.blit(move_label, (600, HEIGHT - 85))  # Adjusted position

        # Draw copy object button
        pygame.draw.rect(screen, draw_copy_button_color, (660, HEIGHT - 80, button_width, button_height))  # Adjusted position
        copy_label = pygame.font.SysFont(None, 20).render("Copy", True, (0, 0, 0))  # Increased text size
        screen.blit(copy_label, (670, HEIGHT - 85))  # Adjusted position

        # Draw select rounded edges button
        pygame.draw.rect(screen, draw_rounded_button_color, (730, HEIGHT - 80, button_width, button_height))  # Adjusted position
        rounded_label = pygame.font.SysFont(None, 20).render("Rounded", True, (0, 0, 0))  # Increased text size
        screen.blit(rounded_label, (740, HEIGHT - 85))  # Adjusted position

        # Draw increase radius button
        pygame.draw.rect(screen, increase_rounded_button_color, (800, HEIGHT - 80, button_width, button_height))  # Adjusted position
        increase_label = pygame.font.SysFont(None, 20).render("+", True, (0, 0, 0))  # Increased text size
        screen.blit(increase_label, (810, HEIGHT - 85))  # Adjusted position

        # Draw decrease radius button
        pygame.draw.rect(screen, decrease_rounded_button_color, (870, HEIGHT - 80, button_width, button_height))  # Adjusted position
        decrease_label = pygame.font.SysFont(None, 20).render("-", True, (0, 0, 0))  # Increased text size
        screen.blit(decrease_label, (880, HEIGHT - 85))  # Adjusted position

        # Draw select objects to group button
        pygame.draw.rect(screen, BUTTON_COLOR, (940, HEIGHT - 80, button_width, button_height))  # Adjusted position
        select_objects_label = pygame.font.SysFont(None, 20).render("Select", True, (0, 0, 0))  # Increased text size
        screen.blit(select_objects_label, (950, HEIGHT - 85))  # Adjusted position

        # Draw group selected objects button
        pygame.draw.rect(screen, BUTTON_COLOR, (1010, HEIGHT - 80, button_width, button_height))  # Adjusted position
        group_selected_label = pygame.font.SysFont(None, 20).render("Group", True, (0, 0, 0))  # Increased text size
        screen.blit(group_selected_label, (1020, HEIGHT - 85))  # Adjusted position

        # Draw ungroup button
        pygame.draw.rect(screen, BUTTON_COLOR, (1080, HEIGHT - 80, button_width, button_height))  # Adjusted position
        ungroup_label = pygame.font.SysFont(None, 20).render("Ungroup", True, (0, 0, 0))  # Increased text size
        screen.blit(ungroup_label, (1090, HEIGHT - 85))  # Adjusted position



# GroupedObject class
class GroupedObject(Object):
    def __init__(self):
        super().__init__()
        self.objects = []  # List to hold individual objects in the group

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def draw(self, canvas):
        for obj in self.objects:
            obj.draw(canvas)

    def move(self, pos):
        for obj in self.objects:
            obj.move(pos)


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
            copied_obj.set_radius(obj.radius)
            copied_obj.rounded=True
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
                        if 20 <= event.pos[0] < 70:
                            self.toolbar.select_tool(DRAW_LINE)
                        elif 90 <= event.pos[0] < 140:
                            self.toolbar.select_tool(DRAW_RECT)
                        elif 160 <= event.pos[0] < 210:
                            self.toolbar.selected_object = None
                            self.toolbar.select_color((255, 0, 0))
                        elif 230 <= event.pos[0] < 280:
                            self.toolbar.selected_object = None
                            self.toolbar.select_color((0, 255, 0))
                        elif 300 <= event.pos[0] < 350:
                            self.toolbar.selected_object = None
                            self.toolbar.select_color((0, 0, 255))
                        elif 370 <= event.pos[0] < 420:
                            self.toolbar.selected_object = None
                            self.toolbar.select_color((0, 0, 0))
                        elif 450 <= event.pos[0] < 500 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(SELECT_OBJ)
                        elif 520 <= event.pos[0] < 570 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(DELETE_OBJ)
                        elif 590 <= event.pos[0] < 640 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(MOVE_OBJ)
                        elif 660 <= event.pos[0] < 710 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(COPY)
                        elif 730 <= event.pos[0] < 780 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(ROUNDED_SELECT)
                        elif 800 <= event.pos[0] < 850 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            if isinstance(self.toolbar.selected_object, Rectangle):
                                self.toolbar.selected_object.rounded=True
                                self.toolbar.selected_object.radius += 5
                                print("After increase:", self.toolbar.selected_object.radius)
                                self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                for obj in self.objects:
                                    obj.draw(self.canvas)
                        elif 870 <= event.pos[0] < 920 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            if isinstance(self.toolbar.selected_object, Rectangle) and self.toolbar.selected_object.rounded:
                                if self.toolbar.selected_object.radius >= 5:
                                    self.toolbar.selected_object.radius -= 5
                                    self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                    for obj in self.objects:
                                        obj.draw(self.canvas)
                        elif 940 <= event.pos[0] < 990 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(SELECT_GROUP)
                        elif 1010 <= event.pos[0] < 1060 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(GROUP_OBJECTS)
                        elif 1080 <= event.pos[0] < 1130 and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30:
                            self.toolbar.select_tool(UNGROUP_OBJECTS)
                        else:
                            self.toolbar.select_button_color = BUTTON_COLOR
                            self.toolbar.radius_button_color = BUTTON_COLOR
                    else:  # Clicked on canvas
                        if (self.toolbar.selected_tool == DRAW_LINE or self.toolbar.selected_tool == DRAW_RECT) :
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
                            
                        elif self.toolbar.selected_tool== SELECT_GROUP:
                            pass
                        
                        elif self.toolbar.selected_tool == GROUP_OBJECTS:
                            pass
                        
                        elif self.toolbar.selected_tool == UNGROUP_OBJECTS:
                            pass
                            


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
