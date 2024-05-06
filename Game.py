import pygame
import xml.etree.ElementTree as ET
import os

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH = 1300
HEIGHT = 800
CANVAS_COLOR = (255, 255, 255)
TOOLBAR_COLOR = (200, 200, 200)
TOOLBAR_COLOR2 = (250, 200, 200)
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
ROUNDED_SELECT = 9
INCREASE_RADIUS = 10
DECREASE_RADIUS = 11
SELECT_GROUP = 12
GROUP_OBJECTS = 13
UNGROUP_OBJECTS = 14
SAVE = 15
OPEN = 16
EXPORT_TO_XML = 17


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
            pygame.draw.line(
                canvas, self.color, self.start_pos, self.end_pos, LINE_WIDTH
            )


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
                rect = pygame.Rect(
                    self.start_pos[0], self.start_pos[1], rect_width, rect_height
                )
                pygame.draw.rect(canvas, self.color, rect, border_radius=self.radius)
            else:
                pygame.draw.rect(
                    canvas,
                    self.color,
                    (
                        self.start_pos,
                        (
                            self.end_pos[0] - self.start_pos[0],
                            self.end_pos[1] - self.start_pos[1],
                        ),
                    ),
                )


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
        pygame.draw.rect(
            screen, TOOLBAR_COLOR, (0, HEIGHT - 100, WIDTH, 100)
        )  # Toolbar area

        draw_line_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_LINE else BUTTON_COLOR
        )
        draw_rect_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == DRAW_RECT else BUTTON_COLOR
        )
        draw_select_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == SELECT_OBJ else BUTTON_COLOR
        )
        draw_delete_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == DELETE_OBJ else BUTTON_COLOR
        )
        draw_move_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == MOVE_OBJ else BUTTON_COLOR
        )
        draw_copy_button_color = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == COPY or self.selected_tool == PASTE
            else BUTTON_COLOR
        )
        draw_rounded_button_color = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == ROUNDED_SELECT
            else BUTTON_COLOR
        )
        increase_rounded_button_color = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == INCREASE_RADIUS
            else BUTTON_COLOR
        )
        decrease_rounded_button_color = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == DECREASE_RADIUS
            else BUTTON_COLOR
        )
        select_group_button_colour = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == SELECT_GROUP
            else BUTTON_COLOR
        )
        group_button_colour = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == GROUP_OBJECTS
            else BUTTON_COLOR
        )
        ungroup_button_colour = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == UNGROUP_OBJECTS
            else BUTTON_COLOR
        )

        # Button widths
        button_width = 50  # Decreased button width
        button_height = 40  # Decreased button height

        # Draw Line button
        pygame.draw.rect(
            screen,
            draw_line_button_color,
            (20, HEIGHT - 80, button_width, button_height),
        )
        draw_line_label = pygame.font.SysFont(None, 20).render(
            "Line", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(draw_line_label, (30, HEIGHT - 85))  # Adjusted position

        # Draw Rectangle button
        pygame.draw.rect(
            screen,
            draw_rect_button_color,
            (90, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        draw_rect_label = pygame.font.SysFont(None, 20).render(
            "Rect", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(draw_rect_label, (100, HEIGHT - 85))  # Adjusted position

        # Draw color buttons
        color_buttons_pos = [
            (160, HEIGHT - 80),
            (230, HEIGHT - 80),
            (300, HEIGHT - 80),
            (370, HEIGHT - 80),
        ]  # Adjusted positions
        color_labels = ["Red", "Green", "Blue", "Black"]  # Color labels
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]):
            pygame.draw.rect(
                screen,
                color,
                (
                    color_buttons_pos[i][0],
                    color_buttons_pos[i][1],
                    button_height,
                    button_height,
                ),
            )
            color_label = pygame.font.SysFont(None, 20).render(
                color_labels[i], True, (0, 0, 0)
            )  # Increased text size
            screen.blit(
                color_label, (color_buttons_pos[i][0] + 5, HEIGHT - 85)
            )  # Adjusted position

        # Draw select object button
        pygame.draw.rect(
            screen,
            draw_select_button_color,
            (450, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        select_label = pygame.font.SysFont(None, 20).render(
            "Select", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(select_label, (460, HEIGHT - 85))  # Adjusted position

        # Draw delete object button
        pygame.draw.rect(
            screen,
            draw_delete_button_color,
            (520, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        delete_label = pygame.font.SysFont(None, 20).render(
            "Delete", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(delete_label, (530, HEIGHT - 85))  # Adjusted position

        # Draw move object button
        pygame.draw.rect(
            screen,
            draw_move_button_color,
            (590, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        move_label = pygame.font.SysFont(None, 20).render(
            "Move", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(move_label, (600, HEIGHT - 85))  # Adjusted position

        # Draw copy object button
        pygame.draw.rect(
            screen,
            draw_copy_button_color,
            (660, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        copy_label = pygame.font.SysFont(None, 20).render(
            "Copy", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(copy_label, (670, HEIGHT - 85))  # Adjusted position

        # Draw select rounded edges button
        pygame.draw.rect(
            screen,
            draw_rounded_button_color,
            (730, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        rounded_label = pygame.font.SysFont(None, 20).render(
            "Rounded", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(rounded_label, (740, HEIGHT - 85))  # Adjusted position

        # Draw increase radius button
        pygame.draw.rect(
            screen,
            increase_rounded_button_color,
            (800, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        increase_label = pygame.font.SysFont(None, 20).render(
            "+", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(increase_label, (810, HEIGHT - 85))  # Adjusted position

        # Draw decrease radius button
        pygame.draw.rect(
            screen,
            decrease_rounded_button_color,
            (870, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        decrease_label = pygame.font.SysFont(None, 20).render(
            "-", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(decrease_label, (880, HEIGHT - 85))  # Adjusted position

        # Draw select objects to group button
        pygame.draw.rect(
            screen,
            select_group_button_colour,
            (940, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        select_objects_label = pygame.font.SysFont(None, 20).render(
            "Select", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(select_objects_label, (950, HEIGHT - 85))  # Adjusted position

        # Draw group selected objects button
        pygame.draw.rect(
            screen,
            group_button_colour,
            (1010, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        group_selected_label = pygame.font.SysFont(None, 20).render(
            "Group", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(group_selected_label, (1020, HEIGHT - 85))  # Adjusted position

        # Draw ungroup button
        pygame.draw.rect(
            screen,
            ungroup_button_colour,
            (1080, HEIGHT - 80, button_width, button_height),
        )  # Adjusted position
        ungroup_label = pygame.font.SysFont(None, 20).render(
            "Ungroup", True, (0, 0, 0)
        )  # Increased text size
        screen.blit(ungroup_label, (1090, HEIGHT - 85))  # Adjusted position


class Menu:
    def __init__(self):
        self.button_height = 40
        self.button_color = (150, 150, 150)
        self.selected_tool = None
        self.button_font = pygame.font.SysFont(None, 20)  # Font for button labels

    def draw(self, screen):
        # Draw the menu background
        pygame.draw.rect(screen, TOOLBAR_COLOR2, (WIDTH - 100, 0, 100, HEIGHT))

        # Define button positions
        button_y_positions = [50, 150, 250]  # Adjusted positions

        draw_save_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == SAVE else BUTTON_COLOR
        )
        draw_open_button_color = (
            SELECTED_BUTTON_COLOR if self.selected_tool == OPEN else BUTTON_COLOR
        )
        draw_XML_button_color = (
            SELECTED_BUTTON_COLOR
            if self.selected_tool == EXPORT_TO_XML
            else BUTTON_COLOR
        )

        # Draw "Save" button
        pygame.draw.rect(
            screen,
            draw_save_button_color,
            (WIDTH - 90, button_y_positions[0], 80, self.button_height),
        )
        save_label = self.button_font.render("Save", True, (0, 0, 0))
        screen.blit(save_label, (WIDTH - 80, button_y_positions[0] + 5))

        # Draw "Open" button
        pygame.draw.rect(
            screen,
            draw_open_button_color,
            (WIDTH - 90, button_y_positions[1], 80, self.button_height),
        )
        open_label = self.button_font.render("Open", True, (0, 0, 0))
        screen.blit(open_label, (WIDTH - 80, button_y_positions[1] + 5))

        # Draw "Export to XML" button
        pygame.draw.rect(
            screen,
            draw_XML_button_color,
            (WIDTH - 90, button_y_positions[2], 80, self.button_height),
        )
        export_label = self.button_font.render("Export to XML", True, (0, 0, 0))
        screen.blit(
            export_label, (WIDTH - 110, button_y_positions[2] + 5)
        )  # Adjusted position for longer text


# GroupedObject class
class GroupedObject(Object):
    def __init__(self):
        super().__init__()
        self.objects = []  # List to hold individual objects in the group
        self.top_left_x = 10000
        self.top_left_y = 10000

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def draw(self, canvas):
        for obj in self.objects:
            obj.draw(canvas)

    def set_color(self, color):
        for obj in self.objects:
            obj.set_color(color)

    def move(self, pos):
        # Calculate displacement between new top-left and current top-left
        delta_x = pos[0] - self.top_left_x
        delta_y = pos[1] - self.top_left_y

        # Update top-left position
        self.top_left_x = pos[0]
        self.top_left_y = pos[1]

        # Move all objects in the group by the same displacement
        for obj in self.objects:
            if isinstance(obj, GroupedObject):
                obj.move((obj.top_left_x + delta_x, obj.top_left_y + delta_y))
            else:
                obj.move((obj.start_pos[0] + delta_x, obj.start_pos[1] + delta_y))


# Main game class
class DrawingApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Canvas with Toolbar")

        self.canvas = pygame.Surface(
            (WIDTH - 100, HEIGHT - 100)
        )  # Create a surface for the canvas
        self.canvas.fill(CANVAS_COLOR)

        self.toolbar = Toolbar()
        self.menu = Menu()
        self.objects = []

        self.selected_for_grouping_list = []

        self.drawing_object = None

    def export_to_xml(self, filename):
        root = ET.Element("drawing")

        for obj in self.objects:
            if isinstance(obj, Line):
                line_elem = ET.SubElement(root, "line")
                begin_elem = ET.SubElement(line_elem, "begin")
                ET.SubElement(begin_elem, "x").text = str(obj.start_pos[0])
                ET.SubElement(begin_elem, "y").text = str(obj.start_pos[1])
                end_elem = ET.SubElement(line_elem, "end")
                ET.SubElement(end_elem, "x").text = str(obj.end_pos[0])
                ET.SubElement(end_elem, "y").text = str(obj.end_pos[1])
                ET.SubElement(line_elem, "color").text = self.color_to_string(obj.color)
            elif isinstance(obj, Rectangle):
                rect_elem = ET.SubElement(root, "rectangle")
                upper_left_elem = ET.SubElement(rect_elem, "upper-left")
                ET.SubElement(upper_left_elem, "x").text = str(obj.start_pos[0])
                ET.SubElement(upper_left_elem, "y").text = str(obj.start_pos[1])
                lower_right_elem = ET.SubElement(rect_elem, "lower-right")
                ET.SubElement(lower_right_elem, "x").text = str(obj.end_pos[0])
                ET.SubElement(lower_right_elem, "y").text = str(obj.end_pos[1])
                ET.SubElement(rect_elem, "color").text = self.color_to_string(obj.color)
                ET.SubElement(rect_elem, "corner").text = (
                    "rounded" if obj.rounded else "square"
                )
            else:
                group_elem = ET.SubElement(root, "group")
                self.export_to_xml_group(filename, obj, group_elem)

        tree = ET.ElementTree(root)
        tree.write(filename)

    def export_to_xml_group(self, filename, object: GroupedObject, root):
        for obj in object.objects:
            if isinstance(obj, Line):
                line_elem = ET.SubElement(root, "line")
                begin_elem = ET.SubElement(line_elem, "begin")
                ET.SubElement(begin_elem, "x").text = str(obj.start_pos[0])
                ET.SubElement(begin_elem, "y").text = str(obj.start_pos[1])
                end_elem = ET.SubElement(line_elem, "end")
                ET.SubElement(end_elem, "x").text = str(obj.end_pos[0])
                ET.SubElement(end_elem, "y").text = str(obj.end_pos[1])
                ET.SubElement(line_elem, "color").text = self.color_to_string(obj.color)
            elif isinstance(obj, Rectangle):
                rect_elem = ET.SubElement(root, "rectangle")
                upper_left_elem = ET.SubElement(rect_elem, "upper-left")
                ET.SubElement(upper_left_elem, "x").text = str(obj.start_pos[0])
                ET.SubElement(upper_left_elem, "y").text = str(obj.start_pos[1])
                lower_right_elem = ET.SubElement(rect_elem, "lower-right")
                ET.SubElement(lower_right_elem, "x").text = str(obj.end_pos[0])
                ET.SubElement(lower_right_elem, "y").text = str(obj.end_pos[1])
                ET.SubElement(rect_elem, "color").text = self.color_to_string(obj.color)
                ET.SubElement(rect_elem, "corner").text = (
                    "rounded" if obj.rounded else "square"
                )
            else:
                group_elem = ET.SubElement(root, "group")
                self.export_to_xml_group(filename, obj, group_elem)

    def color_to_string(self, color):
        if color == (255, 0, 0):
            return "red"
        elif color == (0, 255, 0):
            return "green"
        elif color == (0, 0, 255):
            return "blue"
        elif color == (0, 0, 0):
            return "black"
        else:
            return "unknown"

    def save_drawing(self, filename):
        with open(filename, "w") as file:
            for obj in self.objects:
                if isinstance(obj, Line):
                    file.write(
                        f"line {obj.start_pos[0]} {obj.start_pos[1]} {obj.end_pos[0]} {obj.end_pos[1]} ({obj.color[0]},{obj.color[1]},{obj.color[2]})\n"
                    )
                elif isinstance(obj, Rectangle):
                    style = "r" if obj.rounded else "s"
                    rad = ""
                    if style == "r":
                        rad = obj.radius
                    file.write(
                        f"rect {obj.start_pos[0]} {obj.start_pos[1]} {obj.end_pos[0]} {obj.end_pos[1]} ({obj.color[0]},{obj.color[1]},{obj.color[2]}) {style} {rad}\n"
                    )
                elif isinstance(obj, GroupedObject):
                    file.write("begin\n")
                    for sub_obj in obj.objects:
                        # Recursively save grouped objects
                        self.save_grouped_object(file, sub_obj)
                    file.write("end\n")

    def save_grouped_object(self, file, obj):
        if isinstance(obj, Line):
            file.write(
                f"line {obj.start_pos[0]} {obj.start_pos[1]} {obj.end_pos[0]} {obj.end_pos[1]} ({obj.color[0]},{obj.color[1]},{obj.color[2]})\n"
            )
        elif isinstance(obj, Rectangle):
            style = "r" if obj.rounded else "s"
            rad = ""
            if style == "r":
                rad = obj.radius
            file.write(
                f"rect {obj.start_pos[0]} {obj.start_pos[1]} {obj.end_pos[0]} {obj.end_pos[1]} ({obj.color[0]},{obj.color[1]},{obj.color[2]}) {style} {rad}\n"
            )
        elif isinstance(obj, GroupedObject):
            file.write("begin\n")
            for sub_obj in obj.objects:
                self.save_grouped_object(file, sub_obj)
            file.write("end\n")

    def open_drawing(self, filename):

        with open(filename, "r") as file:
            for line in file:
                # print(line)
                line = line.strip().split()
                if line[0] == "line":
                    start_pos = (int(line[1]), int(line[2]))
                    end_pos = (int(line[3]), int(line[4]))
                    A = line[5].replace("(", "").replace(")", "").split(",")
                    color = tuple(map(int, A))
                    new_line = Line()
                    new_line.set_start_pos(start_pos)
                    new_line.set_end_pos(end_pos)
                    new_line.set_color(color)
                    self.objects.append(new_line)
                elif line[0] == "rect":
                    start_pos = (int(line[1]), int(line[2]))
                    end_pos = (int(line[3]), int(line[4]))
                    A = line[5].replace("(", "").replace(")", "").split(",")
                    color = tuple(map(int, A))
                    style = line[6]
                    rounded = True if style == "r" else False
                    rad = 0
                    if rounded == True:
                        rad = int(line[7])
                    new_rect = Rectangle(rounded=rounded)
                    new_rect.set_start_pos(start_pos)
                    new_rect.set_end_pos(end_pos)
                    new_rect.set_color(color)
                    new_rect.rounded = rounded
                    new_rect.radius = rad
                    self.objects.append(new_rect)
                elif line[0] == "begin":
                    group = GroupedObject()
                    self.open_group(file, group)
                    self.objects.append(group)

    def open_group(self, file, group: GroupedObject):
        for line in file:
            # print(line)
            line = line.strip().split()
            if line[0] == "end":
                return
            elif line[0] == "line":
                start_pos = (int(line[1]), int(line[2]))
                end_pos = (int(line[3]), int(line[4]))
                A = line[5].replace("(", "").replace(")", "").split(",")
                color = tuple(map(int, A))
                new_line = Line()
                new_line.set_start_pos(start_pos)
                new_line.set_end_pos(end_pos)
                new_line.set_color(color)
                group.add_object(new_line)
                if new_line.start_pos[0] < group.top_left_x:
                    group.top_left_x = new_line.start_pos[0]
                if new_line.start_pos[1] < group.top_left_y:
                    group.top_left_y = new_line.start_pos[1]
            elif line[0] == "rect":
                start_pos = (int(line[1]), int(line[2]))
                end_pos = (int(line[3]), int(line[4]))
                A = line[5].replace("(", "").replace(")", "").split(",")
                color = tuple(map(int, A))
                style = line[6]
                rounded = True if style == "r" else False
                rad = 0
                if rounded == True:
                    rad = int(line[7])
                new_rect = Rectangle(rounded=rounded)
                new_rect.set_start_pos(start_pos)
                new_rect.set_end_pos(end_pos)
                new_rect.set_color(color)
                new_rect.rounded = rounded
                new_rect.radius = rad
                group.objects.append(new_rect)
                if new_rect.start_pos[0] < group.top_left_x:
                    group.top_left_x = new_rect.start_pos[0]
                if new_rect.start_pos[1] < group.top_left_y:
                    group.top_left_y = new_rect.start_pos[1]
            elif line[0] == "begin":
                sub_group = GroupedObject()
                self.open_group(file, sub_group)
                group.add_object(sub_group)
                if sub_group.top_left_x < group.top_left_x:
                    group.top_left_x = sub_group.top_left_x
                if sub_group.top_left_y < group.top_left_y:
                    group.top_left_y = sub_group.top_left_y

    def get_selected_object(self, pos):
        for obj in reversed(self.objects):
            if isinstance(obj, Rectangle):
                rect = pygame.Rect(
                    obj.start_pos[0],
                    obj.start_pos[1],
                    abs(obj.end_pos[0] - obj.start_pos[0]),
                    abs(obj.end_pos[1] - obj.start_pos[1]),
                )
                if rect.collidepoint(pos):
                    return obj
            elif isinstance(obj, Line):
                if (
                    obj.start_pos[0] <= pos[0] <= obj.end_pos[0]
                    and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]
                ):
                    return obj
            elif isinstance(obj, GroupedObject):
                selected_obj = self.get_selected_object_grp(pos, obj)
                if selected_obj:
                    return selected_obj
        return None

    def get_selected_object_grp(self, pos, grp: GroupedObject):
        for obj in reversed(grp.objects):
            if isinstance(obj, Rectangle):
                rect = pygame.Rect(
                    obj.start_pos[0],
                    obj.start_pos[1],
                    abs(obj.end_pos[0] - obj.start_pos[0]),
                    abs(obj.end_pos[1] - obj.start_pos[1]),
                )
                if rect.collidepoint(pos):
                    return grp
            elif isinstance(obj, Line):
                if (
                    obj.start_pos[0] <= pos[0] <= obj.end_pos[0]
                    and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]
                ):
                    return grp
            elif isinstance(obj, GroupedObject):
                selected_obj = self.get_selected_object_grp(pos, obj)
                if selected_obj:
                    return grp
        return None

    def get_selected_object_rounded(self, pos):
        # print('here')
        for obj in reversed(self.objects):
            if isinstance(obj, Rectangle):
                rect = pygame.Rect(
                    obj.start_pos[0],
                    obj.start_pos[1],
                    abs(obj.end_pos[0] - obj.start_pos[0]),
                    abs(obj.end_pos[1] - obj.start_pos[1]),
                )
                if rect.collidepoint(pos):
                    return obj
            elif isinstance(obj, Line):
                if (
                    obj.start_pos[0] <= pos[0] <= obj.end_pos[0]
                    and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]
                ):
                    return obj
            elif isinstance(obj, GroupedObject):
                selected_obj = self.get_selected_object_grp_rounded(pos, obj)
                if selected_obj:
                    return selected_obj
        return None

    def get_selected_object_grp_rounded(self, pos, grp: GroupedObject):
        for obj in reversed(grp.objects):
            if isinstance(obj, Rectangle):
                rect = pygame.Rect(
                    obj.start_pos[0],
                    obj.start_pos[1],
                    abs(obj.end_pos[0] - obj.start_pos[0]),
                    abs(obj.end_pos[1] - obj.start_pos[1]),
                )
                if rect.collidepoint(pos):
                    return obj
            elif isinstance(obj, Line):
                if (
                    obj.start_pos[0] <= pos[0] <= obj.end_pos[0]
                    and obj.start_pos[1] <= pos[1] <= obj.end_pos[1]
                ):
                    return obj
            elif isinstance(obj, GroupedObject):
                selected_obj = self.get_selected_object_grp_rounded(pos, obj)
                if selected_obj:
                    return selected_obj
        return None

    def copy_object(self, obj):
        if isinstance(obj, Rectangle):
            copied_obj = Rectangle()
            copied_obj.set_radius(obj.radius)
            copied_obj.rounded = True
            copied_obj.set_start_pos(obj.start_pos)
            copied_obj.set_end_pos(obj.end_pos)
            copied_obj.set_color(obj.color)
        elif isinstance(obj, Line):
            copied_obj = Line()
            copied_obj.set_start_pos(obj.start_pos)
            copied_obj.set_end_pos(obj.end_pos)
            copied_obj.set_color(obj.color)
        elif isinstance(obj, GroupedObject):
            copied_obj = GroupedObject()
            copied_obj.top_left_x = obj.top_left_x
            copied_obj.top_left_y = obj.top_left_y
            for sub_obj in obj.objects:
                copied_sub_obj = self.copy_object(sub_obj)
                if copied_sub_obj is not None:
                    copied_obj.add_object(copied_sub_obj)

        else:
            return None

        return copied_obj

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (
                        WIDTH - 100 <= event.pos[0] < WIDTH
                    ):  # Check if menu area clicked
                        if (
                            50 <= event.pos[1] < 50 + self.menu.button_height
                        ):  # Check if "Save" button clicked
                            print("Save button clicked!!! Enter File Name:")
                            file_name_inp = input() + ".txt"
                            self.menu.selected_tool = SAVE
                            self.save_drawing(file_name_inp)
                            print("Done")
                            # Add code to handle "Save" button click
                        elif (
                            150 <= event.pos[1] < 150 + self.menu.button_height
                        ):  # Check if "Open" button clicked
                            print("Open button clicked!!! Enter File Name:")
                            self.menu.selected_tool = OPEN
                            for i in range(0, len(self.objects)):
                                self.objects.remove(self.objects[0])
                            self.drawing_object = None
                            self.canvas.fill(CANVAS_COLOR)
                            self.toolbar.draw(self.screen)
                            self.menu.draw(self.screen)
                            self.toolbar.selected_object = None
                            file_name_inp = input() + ".txt"
                            if os.path.exists(file_name_inp):
                                self.open_drawing(file_name_inp)
                                print("Done")
                            else:
                                print("file not found")
                            # Add code to handle "Open" button click
                        elif (
                            250 <= event.pos[1] < 250 + self.menu.button_height
                        ):  # Check if "Export to XML" button clicked
                            print("Export to XML button clicked!!! Enter File Name:")
                            file_name_inp = input() + ".xml"
                            self.export_to_xml(file_name_inp)
                            print("Done")
                            self.menu.selected_tool = EXPORT_TO_XML
                    elif (
                        HEIGHT - 100 <= event.pos[1] < HEIGHT
                    ):  # Check if toolbar area clicked
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
                        elif (
                            450 <= event.pos[0] < 500
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(SELECT_OBJ)
                        elif (
                            520 <= event.pos[0] < 570
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(DELETE_OBJ)
                        elif (
                            590 <= event.pos[0] < 640
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(MOVE_OBJ)
                        elif (
                            660 <= event.pos[0] < 710
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(COPY)
                        elif (
                            730 <= event.pos[0] < 780
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(ROUNDED_SELECT)
                        elif (
                            800 <= event.pos[0] < 850
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            if isinstance(self.toolbar.selected_object, Rectangle):
                                self.toolbar.selected_object.rounded = True
                                self.toolbar.selected_object.radius += 5
                                print(
                                    "After increase:",
                                    self.toolbar.selected_object.radius,
                                )
                                self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                for obj in self.objects:
                                    obj.draw(self.canvas)
                        elif (
                            870 <= event.pos[0] < 920
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            if (
                                isinstance(self.toolbar.selected_object, Rectangle)
                                and self.toolbar.selected_object.rounded
                            ):
                                if self.toolbar.selected_object.radius >= 5:
                                    self.toolbar.selected_object.radius -= 5
                                    self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                                    for obj in self.objects:
                                        obj.draw(self.canvas)
                        elif (
                            940 <= event.pos[0] < 990
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(SELECT_GROUP)
                        elif (
                            1010 <= event.pos[0] < 1060
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(GROUP_OBJECTS)
                            if len(self.selected_for_grouping_list) > 0:
                                grouped_obj = GroupedObject()
                                for obj in self.selected_for_grouping_list:
                                    grouped_obj.add_object(obj)
                                    if obj.start_pos[0] < grouped_obj.top_left_x:
                                        grouped_obj.top_left_x = obj.start_pos[0]
                                    if obj.start_pos[1] < grouped_obj.top_left_y:
                                        grouped_obj.top_left_y = obj.start_pos[1]
                                for obj in self.selected_for_grouping_list:
                                    self.objects.remove(obj)
                                self.selected_for_grouping_list.clear()
                                self.objects.append(grouped_obj)
                                self.toolbar.selected_tool = None

                        elif (
                            1080 <= event.pos[0] < 1130
                            and HEIGHT - 80 <= event.pos[1] < HEIGHT - 30
                        ):
                            self.toolbar.select_tool(UNGROUP_OBJECTS)
                        else:
                            self.toolbar.select_button_color = BUTTON_COLOR
                            self.toolbar.radius_button_color = BUTTON_COLOR
                    else:  # Clicked on canvas
                        if (
                            self.toolbar.selected_tool == DRAW_LINE
                            or self.toolbar.selected_tool == DRAW_RECT
                        ):
                            if self.drawing_object is None:
                                self.drawing_object = (
                                    Line()
                                    if self.toolbar.selected_tool == DRAW_LINE
                                    else Rectangle()
                                )
                                self.drawing_object.set_start_pos(
                                    (event.pos[0], event.pos[1])
                                )
                                self.drawing_object.set_color(
                                    self.toolbar.selected_color
                                )
                            else:
                                self.drawing_object.set_end_pos(
                                    (event.pos[0], event.pos[1])
                                )
                                self.objects.append(self.drawing_object)
                                self.drawing_object = None
                        elif self.toolbar.selected_tool == SELECT_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(
                                event.pos
                            )
                            if not self.toolbar.selected_object:
                                continue
                            self.toolbar.selected_object.set_color(
                                self.toolbar.selected_color
                            )
                            self.toolbar.selected_object = None
                        elif self.toolbar.selected_tool == DELETE_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(
                                event.pos
                            )
                            if not self.toolbar.selected_object:
                                continue
                            self.objects.remove(self.toolbar.selected_object)
                            self.toolbar.selected_object = None
                            self.canvas.fill(CANVAS_COLOR)  # Clear the canvas
                            # Redraw objects
                            for obj in self.objects:
                                obj.draw(self.canvas)
                        elif self.toolbar.selected_tool == MOVE_OBJ:
                            self.toolbar.selected_object = self.get_selected_object(
                                event.pos
                            )
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
                            self.toolbar.selected_object = self.get_selected_object(
                                event.pos
                            )
                            if not self.toolbar.selected_object:
                                continue
                            self.toolbar.selected_tool = PASTE
                        elif self.toolbar.selected_tool == PASTE:
                            copied_obj = self.copy_object(self.toolbar.selected_object)
                            if isinstance(copied_obj, Line) or isinstance(
                                copied_obj, Rectangle
                            ):
                                delta_x = event.pos[0] - copied_obj.start_pos[0]
                                delta_y = event.pos[1] - copied_obj.start_pos[1]
                                copied_obj.start_pos = event.pos
                                copied_obj.end_pos = (
                                    copied_obj.end_pos[0] + delta_x,
                                    copied_obj.end_pos[1] + delta_y,
                                )
                                copied_obj.set_start_pos(event.pos)
                                self.objects.append(copied_obj)
                                self.drawing_object = None
                            elif isinstance(copied_obj, GroupedObject):
                                print("here is it")
                                copied_obj.move(event.pos)
                                self.objects.append(copied_obj)

                        elif self.toolbar.selected_tool == ROUNDED_SELECT:
                            self.toolbar.selected_object = (
                                self.get_selected_object_rounded(event.pos)
                            )
                            print(self.toolbar.selected_object)

                        elif self.toolbar.selected_tool == SELECT_GROUP:
                            obj = self.get_selected_object(event.pos)
                            if obj != None:
                                self.selected_for_grouping_list.append(obj)

                        elif self.toolbar.selected_tool == UNGROUP_OBJECTS:
                            print("here")
                            self.toolbar.selected_object = self.get_selected_object(
                                event.pos
                            )
                            print(self.toolbar.selected_object)
                            if isinstance(self.toolbar.selected_object, GroupedObject):
                                list_obj = []
                                for o in self.toolbar.selected_object.objects:
                                    list_obj.append(o)
                                self.objects.remove(self.toolbar.selected_object)
                                self.objects.extend(list_obj)

            # print(self.toolbar.selected_tool)
            # Fill the screen with the canvas and toolbar
            self.screen.fill((0, 0, 0))  # Clear the screen

            # Draw toolbar
            self.toolbar.draw(self.screen)
            self.menu.draw(self.screen)

            # Draw objects
            for obj in self.objects:
                obj.draw(self.canvas)
                # print(obj)

            # print()
            #
            # for obj in self.selected_for_grouping_list:
            #    print(obj)
            #
            # print()

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
