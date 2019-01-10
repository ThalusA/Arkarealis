import sys
import tkinter

import MySQLdb
import pygame

pygame.font.init()
pygame.init()
root = tkinter.Tk()

screen_width, screen_height = root.winfo_screenwidth() , root.winfo_screenheight()
size = screen_width, screen_height
screen = pygame.display.set_mode(tuple(var//2 for var in size), pygame.RESIZABLE)
fake_screen = screen.copy()
interaction_box = list()
cursor_line = None
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


def get_optimal_font(self):
    tmp_Font_Size = 0
    ShiftToLeft, ShiftToRight = False, False
    for text in self.textStorage:
        text.replace("|", "")
    all_text = ''.join(str(e) for e in self.textStorage)
    while True:
        tmp_Font_Size += 1
        self.font = pygame.font.Font(pygame.font.match_font("freesansbold"), tmp_Font_Size)
        if self.font.size(all_text)[1] > transform_y(self.clickable_surface[3] - 0.2):
            self.font = pygame.font.Font(pygame.font.match_font("freesansbold"), tmp_Font_Size - 1)
            break
    if self.cursorPos < len(self.textStorage[0]):
        ShiftToLeft = True
        i = len(all_text) - len(self.textStorage[2])
    elif self.cursorPos > (len(all_text) - len(self.textStorage[2])):
        ShiftToRight = True
        i = len(self.textStorage[0])
    while True:
        if ShiftToLeft:
            if self.font.size(all_text[len(self.textStorage[0])-1:i])[0] < transform_x(self.clickable_surface[2] - 0.2):
                self.textStorage = [all_text[len(self.textStorage[0])-1:], all_text[len(self.textStorage[0])-1:i], all_text[i:]]
                break
            i -= 1
        elif ShiftToRight:
            if self.font.size(all_text[i:len(all_text)-len(self.textStorage[2])+1])[0] < transform_x(self.clickable_surface[2] - 0.2):
                self.textStorage = [all_text[len(self.textStorage[0])+1:], all_text[len(self.textStorage[0])+1:i], all_text[i:]]
                break
            i += 1
        else:
            break
    self.textStorage[1] = self.textStorage[1][:self.cursorPos-len(self.textStorage[0])] + "|" + self.textStorage[1][self.cursorPos-len(self.textStorage[0]):]
        

class Text():
    def __init__(self, xy_var, text, font="freesansbold", size=48, text_color=(0, 0, 0), underline=0, bold=0, italic=0, button_mode=0, centered=1):
        self.text_color = text_color
        if button_mode:
            xy_var = (xy_var[0]+(xy_var[2]//2), xy_var[1]+(xy_var[3]//2))
        self.font = pygame.font.Font(pygame.font.match_font(font), size)
        self.font.set_underline(underline)
        self.font.set_bold(bold)
        self.font.set_italic(italic)
        rendered_text = self.font.render(text, True, text_color)
        if centered:
            xy_var[0] = transform_x(xy_var[0]) - (rendered_text.get_width() // 2)
            xy_var[1] = transform_y(xy_var[1]) - (rendered_text.get_height() // 2)
        else:
            xy_var = transform_x(xy_var[0]), transform_y(xy_var[1])
        self.xy_var = xy_var
        fake_screen.blit(rendered_text, xy_var)
    def modify(self, new_text):
        rendered_text = self.font.render(new_text, True, self.text_color)
        fake_screen.blit(rendered_text, self.xy_var)


class Button(Text):
    def __init__(self, xy_wh_var, command, *args, button_color=(255, 0, 0)):
        self.command = command
        self.type = "Button"
        self.xy_wh_var = xy_wh_var
        pygame.draw.rect(fake_screen, button_color, multi_transform(*xy_wh_var))
        Text.__init__(xy_wh_var, *args, button_mode=1)
        interaction_box.append(self)
    def on_click(self, xy_var):
        if transform_x(self.xy_wh_var[0]) <= xy_var[0] and xy_var[0] <= transform_x(self.xy_wh_var[0] + self.xy_wh_var[2]):
            if transform_y(self.xy_wh_var[1]) <= xy_var[1] and xy_var[1] <= transform_y(self.xy_wh_var[1] + self.xy_wh_var[3]):
                exec(self.command)
class TextBox():
    def __init__(self, xy_wh_var, id_str, in_background_color=(255,255,255), out_background_color=(0,0,0), text_color=(0,0,0)):
        x, y, w, h = xy_wh_var
        self.previous_rendered_text = False
        self.id = id_str
        self.type = "TextBox"
        self.in_background_color = in_background_color
        self.clickable_surface = (x+0.5, y+0.5, w-1, h-1)
        self.text_color = text_color
        self.isSelected = False
        self.cursorPos = 0
        self.textStorage = ["","",""]
        self.font = pygame.font.Font(pygame.font.match_font("freesansbold"), 0)
        pygame.draw.rect(fake_screen, in_background_color, multi_transform(*xy_wh_var))
        pygame.draw.rect(fake_screen, out_background_color, multi_transform(*self.clickable_surface), 2)
        interaction_box.append(self)
    def on_click(self, xy_var):
        if transform_x(self.clickable_surface[0]) <= xy_var[0] and xy_var[0] <= transform_x(self.clickable_surface[0] + self.clickable_surface[2]):
            if transform_y(self.clickable_surface[1]) <= xy_var[1] and xy_var[1] <= transform_y(self.clickable_surface[1] + self.clickable_surface[3]):
                self.isSelected = True
                self.keyboard_pressed(0, mode=True)
            else: 
                self.isSelected = False
        else:
            self.isSelected = False
    def keyboard_pressed(self, touch, mode=False):
        if self.isSelected:
            if touch == pygame.K_RIGHT:
                if self.cursorPos != (len(self.textStorage[0])+len(self.textStorage[1])+len(self.textStorage[2])):
                    self.cursorPos += 1
            elif touch == pygame.K_LEFT:
                if bool(self.cursorPos):
                    self.cursorPos -= 1
            elif touch == pygame.K_BACKSPACE:
                if bool(self.cursorPos):
                    if (bool(len(self.textStorage[0])) and self.cursorPos <= len(self.textStorage[0])):
                        self.textStorage[0] = self.textStorage[0][:(len(self.textStorage[0])-2)]
                        self.cursorPos -= 1
                    elif (bool(len(self.textStorage[1])) and self.cursorPos > len(self.textStorage[0])):
                        self.textStorage[1] = self.textStorage[1][:(len(self.textStorage[1])-2)]
                        self.cursorPos -= 1
            elif touch == pygame.K_RETURN:
                self.isSelected = False
            elif not mode:
                self.textStorage[1] = self.textStorage[1][:self.cursorPos] + chr(touch) + self.textStorage[1][self.cursorPos:]
                self.cursorPos += 1
            get_optimal_font(self)
            rendered_text = self.font.render(self.textStorage[1], True, self.text_color)
            if self.previous_rendered_text:
                fake_screen.blit(self.previous_rendered_text, (transform_x(self.clickable_surface[0]+0.2), transform_y(self.clickable_surface[1]+0.1)))
            self.previous_rendered_text = self.font.render(self.textStorage[1], True, self.in_background_color)
            update()
            fake_screen.blit(rendered_text, (transform_x(self.clickable_surface[0]+0.2), transform_y(self.clickable_surface[1]+0.1)))
            print(self.textStorage)
        
        

def clear_screen():
    interaction_box.clear()
    screen.fill((255, 255, 255))
    fake_screen.fill((255, 255, 255))
 
def update():
    screen.blit(fake_screen, (0,0))
    pygame.display.flip()

def main_screen():
    clear_screen()
    global screen
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    Button((45, 45, 10, 10), "option_screen()", "Réglages")
    Button((45, 30, 10, 10), "select_screen()", "Jouer")
    Button((45, 60, 10, 10), "quit_screen()", "Quitter")
    update()

def launcher_screen():
    clear_screen()
    Text((5, 5), "Nom d'utilisateur : ", centered=0)
    Text((5, 15), "Mot de passe : ", centered=0)
    TextBox((20, 5, 60, 8), "username")
    TextBox((20, 15, 60, 8), "password")
    update()
 
def option_screen():
    clear_screen()
    update()

def select_screen():
    clear_screen()
    Text((50,15), "Selectionner votre personnage")
    for i in range (4):
        pygame.draw.rect(fake_screen, (255,0,0), multi_transform((i*20)+11.5, 25, 17, 50), 5)
    update()
    
def quit_screen():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
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
                for _class in interaction_box:
                    _class.on_click(event.pos)
                    to_update = True
        elif event.type == pygame.KEYDOWN:
            for _class in interaction_box:
                if _class.type == "TextBox":
                    if _class.isSelected:
                        _class.keyboard_pressed(event.key)
                        to_update = True
    if to_update == True:
        update()
