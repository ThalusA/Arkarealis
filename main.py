import sys
import time
import tkinter as tk

import pygame

pygame.font.init()
pygame.init()
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

size = screen_width, screen_height
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
fake_screen = screen.copy()
button_array = list()
to_update = False

def transform_x(percentage):
    if percentage > 100:
        raise Exception("Invalid Number")
    return int((percentage/100)*pygame.display.Info().current_w)

def transform_y(percentage):
    if percentage > 100:
        raise Exception("Invalid Number")
    return int((percentage/100)*pygame.display.Info().current_h)

def multi_transform(x, y, width, height):
    return (transform_x(x), transform_y(y), transform_x(width), transform_y(height))


def render_text(string, tuple_var, font="freesansbold", size=48, text_color=(0, 0, 0), underline=0, bold=0, italic=0):
    init_font = pygame.font.Font(pygame.font.match_font(font), size)
    rendered_text = init_font.render(string, True, text_color)
    fake_screen.blit(rendered_text, (transform_x(tuple_var[0]) - (rendered_text.get_width()//2), transform_y(tuple_var[1])-(rendered_text.get_height()//2)))

def make_button(x, y, width, height, command, string="", font="freesansbold", size=48, text_color=(0,0,0), button_color=(255,0,0), large=0, underline=0, bold=0, italic=0):
    x2, y2, width2, height2 = multi_transform(x, y, width, height)
    pygame.draw.rect(fake_screen, button_color, (x2, y2, width2, height2), large)
    render_text(string, ((x+(width//2)),(y+(height//2))), font, size, text_color, underline, bold, italic)
    button_array.append([[x2, y2, x2 + width2, y2 + height2], command])

def clear_screen():
    screen.fill((255,255,255))
    fake_screen.fill((255,255,255))
 
def main_screen():
    clear_screen()
    make_button(45,45,10,10, "option_screen()", "Réglages")
    pygame.display.flip()

def option_screen():
    clear_screen()
    pygame.display.flip()

main_screen()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(fake_screen, event.dict['size']),(0,0))
            to_update = True 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for value in button_array:
                    if (value[0][0] < event.pos[0] and event.pos[0] < value[0][2] and value[0][1] < event.pos[1] and event.pos[1] < value[0][3]):
                        exec(value[1])
                        button_array.clear()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.draw.rect(fake_screen, (255,0,0), multi_transform(5,5,5,5))
                to_update = True
    if to_update == True:
        pygame.display.flip()
