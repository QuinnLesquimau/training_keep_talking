import pygame, sys, random

words = [("YES",(0,1)), ("FIRST",(1,0)), ("DISPLAY",(1,2)),("OKAY",(1,0)),("SAYS",(1,2)),("NOTHING",(0,1)),("",(0,2)),("BLANK",(1,1)),("NO",(1,2)),("LED",(0,1)),("LEAD",(1,2)),("READ",(1,1)),("RED",(1,1)),("REED",(0,2)),("LEED",(0,2)),("HOLD ON",(1,2)),("YOU",(1,1)),("YOU ARE",(1,2)),("YOUR",(1,1)),("YOU'RE",(1,1)),("UR",(0,0)),("THERE",(1,2)),("THEY'RE",(0,2)),("THEIR",(1,1)),("THEY ARE",(0,1)),("SEE",(1,2)),("C",(1,0)),("CEE",(1,2))]

# Visual parameters
height_rect = 150
width_rect = height_rect * 2
height_screen = 4 * height_rect
width_screen = width_rect * 2
size_screen = (height_rect * 4, height_rect * 4)
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)

pygame.init()
screen = pygame.display.set_mode(size_screen)

def drawing_grid(result, pressed_rectangle):
  """Draws the grid of the game.
  If pressed_rectangle is not None, it will be
  integer coordinates (x,y), and will color
  the corresponding rectangle green or red 
  depending if result is True or False.
  """
  whole_screen = pygame.Rect(0, 0, *size_screen)
  pygame.draw.rect(screen, (255,255,255), whole_screen)
  big_rectangle = pygame.Rect(0, 0, height_rect * 4, height_rect)
  pygame.draw.rect(screen, (0,0,0), big_rectangle)
  for x in [0,1]:
    for y in [0,1,2]:
      small_rectangle = pygame.Rect(x*height_rect*2, 
                                  (y+1)*height_rect, 
                                  height_rect * 2,
                                  height_rect)
      pygame.draw.rect(screen, (0,0,0), small_rectangle, 1)
      if (x,y)==pressed_rectangle:
        color = green if result else red
        pygame.draw.rect(screen, color, small_rectangle)

def drawing_word(word):
  """Writes the word at the top of the screen"""
  size_font = 70
  font = pygame.font.SysFont('Times New Roman', size_font)
  text_surface = font.render(word, True, white, black)
  width_text = text_surface.get_width()
  height_text = text_surface.get_height()
  # The position is such that the text is centered
  position = ((width_screen - width_text)/2,
              (height_rect - height_text)/2)
  screen.blit(text_surface, position)

def drawing_screen(word, result=None, pressed_rectangle=None):
  """Draws everything on the screen. If a rectangle is pressed,
  it will lit with green if it is right (result == True)
  and red if it is wrong (result == False).
  """
  drawing_grid(result, pressed_rectangle)
  drawing_word(word)
  pygame.display.update()


word, answer = random.choice(words)
drawing_screen(word)

# Game loop
while True:
  for event in pygame.event.get():
    result, pressed_rectangle = None, None
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      x,y = pygame.mouse.get_pos()
      if y > height_rect:
        disc_x = x // width_rect
        disc_y = (y // height_rect) - 1
        pressed_rectangle = (disc_x, disc_y)
        result = (pressed_rectangle == answer)

    drawing_screen(word, result, pressed_rectangle)
    if result is not None:
      pygame.time.wait(500)
      if result:
        word, answer = random.choice(words)