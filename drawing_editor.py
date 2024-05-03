import pygame
import os
import xml.etree.ElementTree as ET


"""
Drawing Editor

Initialize Pygame: Set up the display window and core functionalities.

Define Drawing Objects: Create classes for lines, rectangles (including properties like color and corner style), 
    and potentially future objects like ellipses.

Implement Object Selection: Use mouse events to detect clicks within object boundaries and visually highlight the selected object.

Object Manipulation:

    Delete: Remove the selected object from the drawing list.
    Copy: Create a duplicate of the selected object and add it to the drawing list.
    Move: Update the object's position based on mouse drag events while maintaining selection.
    Edit: Open a dialog box specific to the object type (e.g., color picker for lines) and update object properties upon user confirmation.

Group Management: Implement a Group class that can hold other objects. Selection within a group should highlight all member objects. 
    Moving or copying a group should move/copy all its members while maintaining relative positions. Implement functionalities for 
    grouping and ungrouping objects.

Saving and Loading: Use Python libraries like os and csv to write/read drawing object data in the specified ASCII format based on object 
    properties.

Optional XML Export: Utilize libraries like xml.etree to generate XML representations of drawings for future use.

"""

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Drawing Editor")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define corner styles for rectangles
SHARP = 0
ROUNDED = 1
RECT_STYLE = SHARP

# Define line width
LINE_WIDTH = 2

# Define object selection variables
selected_object = None
selected_group = None
dragging = False
offset_x = 0
offset_y = 0

# Define drawing objects list
drawing_objects = []

# Define group class
class Group:
    def __init__(self):
        self.members = []

    def add_member(self, obj):
        self.members.append(obj)

    def remove_member(self, obj):
        self.members.remove(obj)

    def draw(self):
        for obj in self.members:
            obj.draw()
    
    def move(self, dx, dy):
        for obj in self.members:
            obj.move(dx, dy)

# Define line class
class Line:
    def __init__(self, start, end, color):
        self.start = start
        self.end = end
        self.color = color

    def draw(self):
        pygame.draw.line(screen, self.color, self.start, self.end, LINE_WIDTH)

    def move(self, dx, dy):
        self.start = (self.start[0] + dx, self.start[1] + dy)
        self.end = (self.end[0] + dx, self.end[1] + dy)

# Define rectangle class
class Rectangle:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 0, RECT_STYLE)

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

# Function to check if a point is inside a rectangle
def point_in_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# Function to check if a point is inside a line
def point_in_line(point, start, end):
    x, y = point
    x1, y1 = start
    x2, y2 = end
    d = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5 + ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
    l = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return d <= l + 0.1

# Function to check if a point is inside an object
def point_in_object(point, obj):
    if isinstance(obj, Line):
        return point_in_line(point, obj.start, obj.end)
    elif isinstance(obj, Rectangle):
        return point_in_rect(point, obj.rect)
    return False

# Function to delete the selected object
def delete_object(obj):
    if obj in drawing_objects:
        drawing_objects.remove(obj)

# Function to copy the selected object
def copy_object(obj):
    if isinstance(obj, Line):
        new_obj = Line(obj.start, obj.end, obj.color)
    elif isinstance(obj, Rectangle):
        new_obj = Rectangle(obj.rect, obj.color)
    drawing_objects.append(new_obj)

# Function to move the selected object
def move_object(obj, dx, dy):
    if isinstance(obj, Line):
        obj.move(dx, dy)
    elif isinstance(obj, Rectangle):
        obj.move(dx, dy)

# Function to edit the selected object
def edit_object(obj):
    if isinstance(obj, Line):
        # Implement line editing functionality (e.g., color picker)
        pass
    elif isinstance(obj, Rectangle):
        # Implement rectangle editing functionality (e.g., color picker, corner style)
        pass

# # Function to save drawing objects to a file
# def save_objects(filename):
#     with
#     open("filename", "w") as file:
#         for obj in drawing_objects:
#             if isinstance(obj, Line):
#                 file.write(f"Line,{obj.start[0]},{obj.start[1]},{obj.end[0]},{obj.end[1]},{obj.color[0]},{obj.color[1]},{obj.color[2]}\n")
#             elif isinstance(obj, Rectangle):
#                 file.write(f"Rectangle,{obj.rect[0]},{obj.rect[1]},{obj.rect[2]},{obj.rect[3]},{obj.color[0]},{obj.color[1]},{obj.color[2]}\n")


while running:
    screen.fill(WHITE)

    #draw an object
    #choose from menu and use mouse

    #display a menu to choose objects from  

    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if selected_object:
                    if isinstance(selected_object, Group):
                        selected_group = selected_object
                        selected_object = None
                    else:
                        selected_object = None
                for obj in drawing_objects:
                    if point_in_object(event.pos, obj):
                        selected_object = obj
                        break
            elif event.button == 3:
                if selected_object:
                    delete_object(selected_object)
                    selected_object = None
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_c:
                if selected_object:
                    copy_object(selected_object)
            elif event.key == pygame.K_g:
                if selected_object:
                    group = Group()
                    group.add_member(selected_object)
                    drawing_objects.append(group)
                    delete_object(selected_object)
                    selected_object = group
            elif event.key == pygame.K_u:
                if selected_group:
                    for obj in selected_group.members:
                        drawing_objects.append(obj)
                    drawing_objects.remove(selected_group)
                    selected_group = None
            elif event.key == pygame.K_s:
                #save_objects("drawing.txt")
                pass
            elif event.key == pygame.K_l:
                #load_objects("drawing.txt")
                pass

    if selected_object:
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            move_object(selected_object, mouse_x - offset_x, mouse_y - offset_y)
            offset_x, offset_y = mouse_x, mouse_y
        else:
            dragging = True
            offset_x, offset_y = pygame.mouse.get_pos()
    else:
        dragging = False

    for obj in drawing_objects:
        obj.draw()

    if selected_object:
        if isinstance(selected_object, Group):
            for obj in selected_object.members:
                pygame.draw.rect(screen, GREEN, obj.rect, 2)
        else:
            if isinstance(selected_object, Line):
                pygame.draw.line(screen, GREEN, selected_object.start, selected_object.end, LINE_WIDTH)
            elif isinstance(selected_object, Rectangle):
                pygame.draw.rect(screen, GREEN, selected_object.rect, 2, RECT_STYLE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()