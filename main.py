import sys
import tkinter

import MySQLdb
import pygame

pygame.font.init()
pygame.init()
root = tkinter.Tk()

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight() // 2
size = screen_width, screen_height
screen = pygame.display.set_mode(tuple(var//2 for var in size), pygame.RESIZABLE)
fake_screen = screen.copy()
interaction_box = list()
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

def get_optimal_font_size(width, height, text, cursor):
    calculating_x, calculating_y = True, True
    tmp_Font_Size = 0
    all_text = str(text[0])+str(text[1])+str(text[2])
    while calculating_y:
        tmp_Font_Size += 0.1
        font = pygame.font.Font(pygame.font.match_font("freesansbold"), tmp_Font_Size)
        y_temp = font.size(text)[1]
        if y_temp > transform_y(height):
            font = pygame.font.Font(pygame.font.match_font("freesansbold"), tmp_Font_Size-0.1)
    i = 0
    if cursor.isdigit():
        text[2] = all_text[cursor:]
        all_text = all_text[:cursor]
    while calculating_x:
        if cursor == "last" and font.size(all_text[i:])[0] < transform_x(width):
            text[0], text[1] = all_text[:i], all_text[i:]
            calculating_x = False
            index = len(str(text[0]))+len(str(text[1]))
        i += 1
    return font, text, index


def render_text(text, tuple_var, font="freesansbold", size=48, text_color=(0, 0, 0), underline=0, bold=0, italic=0):
    init_font = pygame.font.Font(pygame.font.match_font(font), size)
    rendered_text = init_font.render(text, True, text_color)
    fake_screen.blit(rendered_text, (transform_x(tuple_var[0]) - (rendered_text.get_width()//2), transform_y(tuple_var[1])-(rendered_text.get_height()//2)))

def make_button(x, y, width, height, command, text="", font="freesansbold", size=48, text_color=(0,0,0), button_color=(255,0,0), large=0, underline=0, bold=0, italic=0):
    pygame.draw.rect(fake_screen, button_color, multi_transform(x, y, width, height), large)
    render_text(text, ((x+(width//2)),(y+(height//2))), font, size, text_color, underline, bold, italic)
    interaction_box.append([[x, y, x + width, y + height], command])

def text_box(x, y, width, height, size=16):
    pygame.draw.rect(fake_screen, (255, 255, 255), multi_transform(x, y, width, height))
    pygame.draw.rect(fake_screen, (0, 0, 0), multi_transform(x+0.5, y+0.5, width-1, height-1),2)
    interaction_box.append([[x+0.5, y+0.5, width-1, height-1], "activate_input("+str(len(interaction_box))+")", [str(),str(),str()], False, 0])

def activate_input(id, cursor="last"):
    optimal_font = get_optimal_font_size(interaction_box[id][0][2] - 0.2, interaction_box[id][0][3] - 0.2, interaction_box[id][2], cursor)
    interaction_box[id][5] = optimal_font[2]
    rendered_text = optimal_font[0].render(optimal_font[1][1], True, (0, 0, 0))
    for key, value in enumerate(interaction_box):
        if key == id: continue
        value[3] = False
    interaction_box[id][3] = True
    fake_screen.blit(rendered_text, transform_x(interaction_box[id][0][0]+0.1), transform_y(interaction_box[id][0][1]+0.1))

def clear_screen():
    interaction_box.clear()
    screen.fill((255, 255, 255))
    fake_screen.fill((255, 255, 255))
 
def update():
    screen.blit(fake_screen, (0,0))
    pygame.display.flip()

def main_screen():
    clear_screen()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    make_button(45, 45, 10, 10, "option_screen()", "Réglages")
    make_button(45, 30, 10, 10, "select_screen()", "Jouer")
    make_button(45, 60, 10, 10, "quit_screen()", "Quitter")
    update()

def launcher_screen():
    clear_screen()
    update()

def option_screen():
    clear_screen()
    update()

def select_screen():
    clear_screen()
    render_text("Selectionner votre personnage", (50,15))
    for i in range (4):
        pygame.draw.rect(fake_screen, (255,0,0), multi_transform((i*20)+11.5, 25, 17, 50), 5)
    update()


def quit_screen():
    pygame.quit()
    sys.exit()

launcher_screen()

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
                for value in interaction_box:
                    value[0][0], value[0][1], value[0][2], value[0][3] = multi_transform(value[0][0], value[0][1], value[0][2], value[0][3])
                    if (value[0][0] < event.pos[0] and event.pos[0] < value[0][2] and value[0][1] < event.pos[1] and event.pos[1] < value[0][3]):
                        exec(value[1])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                for key, value in enumerate(interaction_box):
                    if value[3] == True:
                        if len(value[2][2]) != 0:
                            interaction_box[key][5] += 1
                            activate_input(key, interaction_box[key][5])
            elif event.key == pygame.K_LEFT:
                for key, value in enumerate(interaction_box):
                    if value[3] == True:
                        if len(value[2][0]) != 0:
                            interaction_box[key][5] -= 1
                            activate_input(key, interaction_box[key][5])
            else:
                for key, value in enumerate(interaction_box):
                    if value[3] == True:
                        interaction_box[key][2][1] += chr(event.key)
                        interaction_box[key][5] += 1
                        activate_input(key, interaction_box[key][5])
    if to_update == True:
        pygame.display.flip()
