import pygame             # importing pygame
from board import lvl_1   # importing made board lvl_1 from board
import os
pygame.init()             # initialise all pygame modules

#Game Window

width = 900               # seting width
height = 950              # seting height
screen = pygame.display.set_mode([width, height])  # making screen by height and width
timer = pygame.time.Clock()                        # creating to help track time
fps = 60                                           # frames per second
font = pygame.font.SysFont('calibri', 20)          # setting font

level = lvl_1
color_1 = '#0094ff' # color of walls on a map
color_2 = 'white'   # color of small dots
color_3 = '#fff5cc' # color of big dots

direction = 0      # direction variable
counter = 0        # counter variable
packman_x = 450    # x position variable
packman_y = 663    # y position variable


player_images = []  # set of player images
if os.path.exists("assets/player") == True:  # check if path exists because of different platforms (this one for Mac)
    for i in range(1, 4):  # adding a ll packman animation frames
        player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player/{i}.png'), (45, 45)))  # scailing and adding player image
else:  # (this one for Windows)
    for i in range(1, 4):  # adding a ll packman animation frames
        player_images.append(pygame.transform.scale(pygame.image.load(f'assets\player\{i}.png'), (45, 45)))  # scailing and adding player image



def draw_board():   # function to draw map
    height_tile = ((height - 50) // 32) # height specialy for tile ( /32 because in original pacman there are 32 different vertical tiles)
    width_tile = (width // 30)          # width specialy for tile ( /30 because in original pacman there are 30 different horizontal tiles)
    for i in range(len(level)):
        for j in range(len(level[i])):
            # drawing dots
            if level[i][j] == 1:   # if element in board equals 1 then as we already described in file for us we draw small circle
                pygame.draw.circle(screen, color_2, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 5)

            if level[i][j] == 2:   # if element in board equals 2 then as we already described in file for us we draw big circle
                pygame.draw.circle(screen, color_3, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 10)

            # drawing lines
            if level[i][j] == 3:   # if element in board equals 3 then as we already described in file for us we draw vertical boarder
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile), (j * width_tile + (0.5 * width_tile), i * height_tile + height_tile), 3) # vertical line

            if level[i][j] == 4:   # if element in board equals 4 then as we already described in file for us we draw horizontal boarder
                pygame.draw.line(screen, color_1, (j * width_tile, i * height_tile + (0.5 * height_tile)), (j * width_tile + width_tile, i * height_tile + (0.5 * height_tile)), 3) # horizontal line

            # drawing corners
            if level[i][j] == 5:   # if element in board equals 5 then as we already described in file for us we draw corner from left to down
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), (j * width_tile + (0.5 * width_tile), i * height_tile + height_tile), 3) # vertical part
                pygame.draw.line(screen, color_1, (j * width_tile, i * height_tile + (0.5 * height_tile)), (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 3) # horizontal part

            if level[i][j] == 6:   # if element in board equals 6 then as we already described in file for us we draw corner from down to right
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), (j * width_tile + (0.5 * width_tile), i * height_tile + height_tile), 3) # vertical part
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), (j * width_tile + width_tile, i * height_tile + (0.5 * height_tile)), 3) # horizontal line

            if level[i][j] == 7:   # if element in board equals 7 then as we already described in file for us we draw corner from up to right
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile), (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 3) # vertical part
                pygame.draw.line(screen, color_1, (j * width_tile + (width_tile * 0.5), i * height_tile + (0.5 * height_tile)), (j * width_tile + width_tile, i * height_tile + (0.5 * height_tile)), 3) # horizontal part

            if level[i][j] == 8:   # if element in board equals 8 then as we already described in file for us we draw corner from left to up
                pygame.draw.line(screen, color_1, (j * width_tile + (0.5 * width_tile), i * height_tile), (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 3) # vertical part
                pygame.draw.line(screen, color_1, (j * width_tile, i * height_tile + (0.5 * height_tile)), (j * width_tile + (width_tile * 0.5), i * height_tile + (0.5 * height_tile)), 3) # horizontal part

            # drawing gates
            if level[i][j] == 9:   # if element in board equals 9 then as we already described in file for us we draw gates for ghosts
                pygame.draw.line(screen, color_2, (j * width_tile, i * height_tile + (0.5 * height_tile)), (j * width_tile + width_tile, i * height_tile + (0.5 * height_tile)), 3)


def draw_player():
    # 0 - right,
    # 1 - left,
    # 2 - up,
    # 3 - down
    if direction == 0:  # PacMan looks right,
        screen.blit(player_images[counter // 8], (packman_x, packman_y))   # placing PacMan in such position and with no transformations
    elif direction == 1:  # PacMan looks left,
        screen.blit(pygame.transform.flip(player_images[counter // 8], True, False), (packman_x, packman_y))   # placing PacMan in such position and flip the image
    elif direction == 2:  # PacMan looks up,
        screen.blit(pygame.transform.rotate(player_images[counter // 8], 90), (packman_x, packman_y))   # placing PacMan in such position and rotate 90 degrees
    elif direction == 3:  # PacMan looks down,
        screen.blit(pygame.transform.rotate(player_images[counter // 8], 270), (packman_x, packman_y))   # placing PacMan in such position and rotate 270 degrees

run = True
while run:
    timer.tick(fps)

    if counter < 23:
        counter += 1
    else:
        counter = 0

    screen.fill('black')
    draw_board()
    draw_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()