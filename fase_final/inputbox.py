# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string, sys
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass


def display_message(screen,message, position, color):
    "Print a message in the screen at the position and color indicated"
    fontobject = pygame.font.SysFont("Fontdiner Swanky", 80)

    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, color ), position)
       
    pygame.display.flip()



def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont("Fontdiner Swanky", 80)
  pygame.draw.rect(screen, (255,255,255,0),
                   ((screen.get_width() *0.45)  ,
                    (screen.get_height() *0.8) + 90,
                    600,100), 0)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (31,73,125)),
                ((screen.get_width() *0.44) - 150, (screen.get_height() *0.8)+ 90))
       
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  num = 0
  current_string = []
  display_box(screen, question + ": " +(''.join(current_string)))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
      num = num - 1
    elif inkey == K_RETURN: break
    elif inkey== K_ESCAPE: pygame.quit(),sys.exit(0)
    elif inkey == K_MINUS:
      current_string.append("_")
    elif (inkey <= 127) and (num < 11):
      current_string.append(chr(inkey))
      num = num + 1
    display_box(screen, question + ": " + (''.join(current_string)))
  return (''.join(current_string))

def main():
  screen = pygame.display.set_mode((320,240))
  print (ask(screen, "Name") + " was entered")

if __name__ == '__main__': main()
