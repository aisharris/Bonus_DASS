import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty):
    # Do the job here !
    print ("value", value)
    print ("diff", difficulty)

    pass

def start_the_game():
    # Do the job here !
    pass

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Draw'), ('Easy')], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)