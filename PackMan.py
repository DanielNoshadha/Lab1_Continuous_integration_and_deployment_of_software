#     ---------------- Import Libraries ----------------

import pygame             # importing pygame
from board import lvl_1   # importing made board lvl_1 from board
from pathlib import Path
#     --------------------------------------------------
pygame.init()             # initialise all pygame modules

#     ----------------   Game Window   -----------------

width = 900                                        # seting width
height = 950                                       # seting height
screen = pygame.display.set_mode([width, height])  # making screen by height and width
timer = pygame.time.Clock()                        # creating to help track time
fps = 60                                           # frames per second
font = pygame.font.SysFont('calibri', 20)          # setting font

level = lvl_1
color_1 = '#0094ff'                                # color of walls on a map
color_2 = 'white'                                  # color of small dots
color_3 = '#fff5cc'                                # color of big dots

direction = 0                                      # direction variable
counter = 0                                        # counter variable
packman_x = 450                                    # x position variable
packman_y = 663                                    # y position variable
flicker = False

# R, L, U, D
turns_allowed = [False, False, False, False]       # turn position
direction_command = 0                              # direction number from 0 to 3
packman_speed = 2                                  # packman speed
score = 0                                          # score

player_images = []                                 # set of player images
player_assets = Path('assets/player/')             # path to player's assets with pathlib
for i in range(1, 5):                              # adding all packman animation frames
    player_frames = player_assets / f'{i}.png'     # creating path for [i] file
    player_images.append(pygame.transform.scale(pygame.image.load(player_frames), (45, 45)))  # scaling and adding player image

ghost_assets = Path('assets/ghosts/')             # path to player's assets with pathlib

blinky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Red_Ghost.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Pink_Ghost.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Aqua_Ghost.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Orange_Ghost.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'dead.png'), (45, 45))

blinky_x = 440
blinky_y = 438
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 56
pinky_y = 58
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False

targets = [(packman_x, packman_y), (packman_x, packman_y), (packman_x, packman_y), (packman_x, packman_y)]
eaten_ghost = [False, False, False, False]
moving = False
ghost_speeds = [2, 2, 2, 2]


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    

# ---------------- Drawing gaming board ----------------
def draw_board():
    height_tile = ((height - 50) // 32)     # height specially for tile ( /32 because in original pacman there are 32 different vertical tiles)
    width_tile = (width // 30)              # width specially for tile ( /30 because in original pacman there are 30 different horizontal tiles)
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

# ---------------- Drawing player ----------------
def draw_player():
    # 0 - right
    # 1 - left
    # 2 - up
    # 3 - down
    if direction == 0:  # PacMan looks right,
        screen.blit(player_images[counter // 5], (packman_x, packman_y))   # placing PacMan in such position and with no transformations
    elif direction == 1:  # PacMan looks left,
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (packman_x, packman_y))   # placing PacMan in such position and flip the image
    elif direction == 2:  # PacMan looks up,
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (packman_x, packman_y))   # placing PacMan in such position and rotate 90 degrees
    elif direction == 3:  # PacMan looks down,
        screen.blit(pygame.transform.rotate(player_images[counter // 5], -90), (packman_x, packman_y))   # placing PacMan in such position and rotate -90 degrees

# ---------------- Checking position ----------------
def check_position(centerx, centery):
    turns = [False, False, False, False]
    height_tile = (height - 50) // 32   # height of a tile
    width_tile = (width // 30)          # width of a tile
    fudge_factor = 15                   # imaginary number from center to borders

    # ----------- check collisions based on center x and center y of player +/- fudge number ------------

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

# ---------------- Check collision ----------------
def check_collision(score):
    height_tile = ((height - 50) // 32)     # height of a tile
    width_tile = (width // 30)              # width of a tile
    if 0 < packman_x < 870:
        if level[center_y // height_tile][center_x // width_tile] == 1:
            level[center_y // height_tile][center_x // width_tile] = 0
            score += 10
        if level[center_y // height_tile][center_x // width_tile] == 2:
            level[center_y // height_tile][center_x // width_tile] = 0
            score += 100
    return score

# ---------------- Move packman ----------------
def move_packman(player_x, player_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        player_x += packman_speed
    elif direction == 1 and turns_allowed[1]:
        player_x -= packman_speed
    if direction == 2 and turns_allowed[2]:
        player_y -= packman_speed
    elif direction == 3 and turns_allowed[3]:
        player_y += packman_speed
    return player_x, player_y

# ---------------- Draw stuf ----------------
def draw_stuff():
    '''
    shows score at the bottom left corner
    '''
    score_text = font.render(f'Score: {score}', True, 'white')    # drawing score
    screen.blit(score_text, (10, 920))                            # show

# ------------ Running game
run = True
while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 9:
            flicker = False
        else:
            flicker = True
    else:
        counter = 0


    screen.fill('black')            # background color
    draw_board()                    # drawing game board
    draw_player()                   # drawing player
    draw_stuff()                    # drawing miscellaneous
    center_x = packman_x + 23       # center position of packman in OX
    center_y = packman_y + 24       # center position of packman in OY
    turns_allowed = check_position(center_x, center_y)
    packman_x, packman_y = move_packman(packman_x, packman_y)
    score = check_collision(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i
    # this part of code teleports player from right to left and vice versa if they've got to the part of the map where it's possible
    if packman_x > 900:
        packman_x = -47
    elif packman_x < -50:
        packman_x = 897

    pygame.display.flip()
pygame.quit()