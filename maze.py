import pygame, sys, random

# importing mazes
f = open("data/mazes.txt", 'r')
mazes = []
for line in f.read().split('\n')[:-1]:
  mazes.append(list(map(eval,line.split(';'))))

# parameters for the display
size_screen = (233, 226)
change_x = 24
change_y = 24
start_x = 58
start_y = 46

def real_coordinates(pos):
  """To go from integer coordinates on the grid to real
  for the display
  """
  x, y = pos
  return (x * change_x + start_x + x/4 + y/4,
          y * change_y + start_y)

screen = pygame.display.set_mode(size_screen)
grid = pygame.image.load("images/training_maze.png")
grid_rect = grid.get_rect()

def draw_screen(x, y, mark1, mark2, goal):
  green = (0, 255, 0)
  red = (255, 0, 0)
  white = (255, 255, 255)
  screen.blit(grid, grid_rect)
  if mark1 is not None:
    pygame.draw.circle(screen, green, real_coordinates(mark1), 7, 1)
    pygame.draw.circle(screen, green, real_coordinates(mark2), 7, 1)
  if goal is not None:
    pygame.draw.circle(screen, red, real_coordinates(goal), 4)
  position = real_coordinates((x,y))
  pygame.draw.circle(screen, white, position, 3)
  pygame.display.update()

num_keys = [pygame.key.key_code(str(n)) for n in range(9)]
pos_x, pos_y = 0, 0
new_pos_x, new_pos_y = 0, 0
creating_maze = False
possible_moves, mark1, mark2 = mazes[0]
goal = None
draw_screen(pos_x, pos_y, mark1, mark2, None)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

    if event.type == pygame.KEYDOWN:
      new_pos_x, new_pos_y = pos_x, pos_y
      if event.key == pygame.K_LEFT:
        new_pos_x = max(pos_x - 1, 0)
      if event.key == pygame.K_RIGHT:
        new_pos_x = min(pos_x + 1, 5)
      if event.key == pygame.K_UP:
        new_pos_y = max(pos_y - 1, 0)
      if event.key == pygame.K_DOWN:
        new_pos_y = min(pos_y + 1, 5)

      if (pos_x, pos_y) != (new_pos_x, new_pos_y):
        if creating_maze: # when adding a new maze in the data
          possible_moves.add(((pos_x, pos_y),
                        (new_pos_x, new_pos_y)))
          pos_x, pos_y = new_pos_x, new_pos_y
        else:
          if (((pos_x, pos_y), (new_pos_x, new_pos_y)) in possible_moves 
              or ((new_pos_x, new_pos_y),(pos_x, pos_y)) in possible_moves):
            pos_x, pos_y = new_pos_x, new_pos_y      
          else:
            print("ERROR!")

      if event.key == pygame.K_w:
        # To add a new maze in the data.
        """
        if creating_maze:
          f = open("mazes.txt", 'a')
          f.write(str(possible_moves) + "\n")
          f.close()
          print("maze created")
        else:
          print("creating maze")
        creating_maze = not creating_maze
        possible_moves = set()
        """

      if event.key in num_keys:
        possible_moves, mark1, mark2 = mazes[num_keys.index(event.key)]
        creating_maze = False
      
      if event.key == pygame.K_r:
        goal = (random.randint(0,5), random.randint(0,5))
        pos_x, pos_y = random.randint(0,5), random.randint(0,5)
        possible_moves, mark1, mark2 = mazes[random.randint(0,8)]

      draw_screen(pos_x, pos_y, mark1, mark2, goal)