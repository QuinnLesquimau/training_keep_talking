import pygame, sys, random

colors_to_rgb = {"red":(255,0,0),
        "yellow":(255,255,0),
        "green":(0,255,0),
        "blue":(0,0,255),
        "white":(255,255,255),
        "black":(0,0,0),
        "grey":(100,100,100)}
# The colors for the wires.
colors = list(colors_to_rgb.keys())[:-1]

# Visual parameters
distance_wires = 50
margin_to_click = 5
height_screen = distance_wires * 7
width_screen  = distance_wires * 9
size_screen = (width_screen, height_screen)
pygame.init()
screen = pygame.display.set_mode(size_screen)
size_font = 30
font = pygame.font.SysFont('Times New Roman', size_font)

def drawing_screen(wires, serial):
  """To draw the screen of the game"""
  background = pygame.Rect(0,0,width_screen,height_screen)
  pygame.draw.rect(screen,
                  colors_to_rgb["grey"],
                  background,
                  )
  for i,wire in enumerate(wires):
    height = (i + 1) * distance_wires
    pygame.draw.line(screen,
                    colors_to_rgb[wire],
                    (0, height),
                    (width_screen, height),
                    3)
  text_surface = font.render(serial, True, colors_to_rgb["black"])
  width_text = text_surface.get_width()
  height_text = text_surface.get_height()
  position_text = ((width_screen - width_text) / 2,
                  height_screen - height_text + 5)
  screen.blit(text_surface, position_text)
  pygame.display.update()

def answer(wires, serial):
  """Gives the index of the wire to cut"""
  nbr_wires = len(wires)
  last_digit_odd = int(serial[-1])%2 != 0
  if nbr_wires==3:
    if "red" not in wires:
      return 1
    if "red" in wires and wires.count("blue") == 2:
      return 2 - wires[::-1].index("blue")
    return 2
  if nbr_wires==4:
    if wires.count("red") > 1 and last_digit_odd:
      return 3 - wires[::-1].index("red")
    if "red" not in wires and wires[-1] == "yellow":
      return 0
    if wires.count("blue") == 1:
      return 0
    if wires.count("yellow") > 1:
      return 3
    return 1
  if nbr_wires==5:
    if wires[-1] == "black" and last_digit_odd:
      return 3
    if wires.count("red") == 1 and wires.count("yellow") > 1:
      return 0
    if "black" not in wires:
      return 1
    return 0
  if nbr_wires==6:
    if "yellow" not in wires and last_digit_odd:
      return 2
    if wires.count("yellow") == 1 and wires.count("white") > 1:
      return 3
    if "red" not in wires:
      return 5
    return 3
  raise ValueError("Incorrect number of wires")


def generate_wires(nbr_wires=None):
  """Generate a random list of colors"""
  if nbr_wires is None: nbr_wires = random.randint(3,6)
  return (nbr_wires, random.choices(colors, k=nbr_wires))

def generate_serial():
  """Generate a random sequence of
  alphanumerical characters, ending with a digit
  """
  alphanum = [chr(x) for x in list(range(48,58)) # 0-9
                            + list(range(65,91)) # A-Z
                            + list(range(97,123))] # a-z
  serial = "".join(random.choices(alphanum,k=9))
  serial += str(random.randint(0,9))
  return serial

nbr_wires, wires = generate_wires()
serial = generate_serial()
correct_answer = answer(wires, serial)
drawing_screen(wires, serial)

# Game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      x,y = pygame.mouse.get_pos()
      on_wire = (abs(round(y / distance_wires) * distance_wires - y) < margin_to_click
                and y > margin_to_click)
      index_wire = round(y / distance_wires) - 1
      if on_wire and index_wire < nbr_wires:
        # When click on the right answer
        if index_wire == correct_answer:
          nbr_wires, wires = generate_wires()
          serial = generate_serial()
          correct_answer = answer(wires, serial)
          drawing_screen(wires, serial)
        # When click on the wrong answer
        else:
          background = pygame.Rect(0,0,width_screen,height_screen)
          pygame.draw.rect(screen,
                          colors_to_rgb["red"],
                          background,
                          )
          pygame.display.update()
          pygame.time.wait(500)
          drawing_screen(wires, serial)