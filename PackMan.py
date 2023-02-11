import pygame             # importing pygame
from board import lvl_1   # importing made board lvl_1 from board
from pathlib import Path

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

# R, L, U, D
turns_allowed = [False, False, False, False]

flicker = False

player_images = []  # set of player images
player_assets = Path('assets/player/') # path to player's assets
for i in range(1, 5):  # adding all packman animation frames
    player_frames = player_assets / f'{i}.png'
    player_images.append(pygame.transform.scale(pygame.image.load(player_frames), (45, 45)))  # scailing and adding player image

def draw_board():   # function to draw map
    height_tile = ((height - 50) // 32) # height specialy for tile ( /32 because in original pacman there are 32 different vertical tiles)
    width_tile = (width // 30)          # width specialy for tile ( /30 because in original pacman there are 30 different horizontal tiles)
    for i in range(len(level)):
        for j in range(len(level[i])):
            # drawing dots
            if level[i][j] == 1:   # if element in board equals 1 then as we already described in file for us we draw small circle
                pygame.draw.circle(screen, color_2, (j * width_tile + (0.5 * width_tile), i * height_tile + (0.5 * height_tile)), 5)

            if level[i][j] == 2 and not flicker:   # if element in board equals 2 then as we already described in file for us we draw big circle
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
        screen.blit(player_images[counter // 5], (packman_x, packman_y))   # placing PacMan in such position and with no transformations
    elif direction == 1:  # PacMan looks left,
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (packman_x, packman_y))   # placing PacMan in such position and flip the image
    elif direction == 2:  # PacMan looks up,
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (packman_x, packman_y))   # placing PacMan in such position and rotate 90 degrees
    elif direction == 3:  # PacMan looks down,
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (packman_x, packman_y))   # placing PacMan in such position and rotate 270 degrees

def check_position(centerx, centery):
    turns = [False, False, False, False]
    height_tile = (height - 50) // 32
    width_tile = (width // 30)
    fudge_factor = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // height_tile][(centerx - fudge_factor) // width_tile] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // height_tile][(centerx + fudge_factor) // width_tile] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + fudge_factor) // height_tile][centerx // width_tile] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - fudge_factor) // height_tile][centerx // width_tile] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % width_tile <= 18:
                if level[(centery + fudge_factor) // height_tile][centerx // width_tile] < 3:
                    turns[3] = True
                if level[(centery - fudge_factor) // height_tile][centerx // width_tile] < 3:
                    turns[2] = True
            if 12 <= centery % height_tile <= 18:
                if level[centery // height_tile][(centerx - width_tile) // width_tile] < 3:
                    turns[1] = True
                if level[centery // height_tile][(centerx + width_tile) // width_tile] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % width_tile <= 18:
                if level[(centery + height_tile) // height_tile][centerx // width_tile] < 3:
                    turns[3] = True
                if level[(centery - height_tile) // height_tile][centerx // width_tile] < 3:
                    turns[2] = True
            if 12 <= centery % height_tile <= 18:
                if level[centery // height_tile][(centerx - fudge_factor) // width_tile] < 3:
                    turns[1] = True
                if level[centery // height_tile][(centerx + fudge_factor) // width_tile] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

run = True
while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0

    screen.fill('black')
    draw_board()
    draw_player()
    center_x = packman_x + 23
    center_y = packman_y + 24
    turns_allowed = check_position(center_x, center_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip()
pygame.quit()