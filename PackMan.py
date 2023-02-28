#     ---------------- Import Libraries ----------------
import pygame             # importing pygame
from board import lvl_1   # importing made board lvl_1 from board
from pathlib import Path  # importing pathlib library for make universal path
import copy               # importing made board lvl_1 from board
#     --------------------------------------------------

pygame.init()             # initialise all pygame module

#     -------------------   Game   ---------------------

width = 900                                        # setting width
height = 950                                       # setting height
screen = pygame.display.set_mode([width, height])  # making screen by height and width
timer = pygame.time.Clock()                        # creating to help track time
fps = 60                                           # frames per second
font = pygame.font.SysFont('calibri', 20)          # setting font

level = copy.deepcopy(lvl_1)
color_1 = '#0094ff'                                # color of walls on a map
color_2 = 'white'                                  # color of small dots
color_3 = '#fff5cc'                                # color of big dots

direction = 0                                      # direction variable
counter = 0                                        # counter variable
packman_x = 450                                    # x position variable
packman_y = 663                                    # y position variable
flicker = False

# R, L, U, D
turns_allowed = [False, False, False, False]       # if turn is allowed then one of indexes will be True
direction_command = 0                              # direction using numbers
packman_speed = 2                                  # packman speed variable
score = 0                                          # score variable
powerup = False                                    # if there is powerup
powerup_counter = 0                                # powerup timer variable
eaten_ghosts = [False, False, False, False]        # if ghost is eaten then one of  indexes will be True
moving = False                                     # variable to prevent packman from moving
startup_counter = 0                                # variables to set amount of time before moving
lives = 5                                          # variables for amount of lives

player_images = []                                 # set of player images
player_assets = Path('assets/player/')             # path to player's assets with pathlib

for i in range(1, 5):                              # adding all packman animation frames
    player_frames = player_assets / f'{i}.png'     # creating path for [i] file
    player_images.append(pygame.transform.scale(pygame.image.load(player_frames), (45, 45)))  # scaling and adding player image

ghost_assets = Path('assets/ghosts/')             # path to ghosts assets with pathlib

blinky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Red_Ghost.png'), (45, 45))       # blinky image
pinky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Pink_Ghost.png'), (45, 45))       # pinky image
inky_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Aqua_Ghost.png'), (45, 45))        # inky image
clyde_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Orange_Ghost.png'), (45, 45))     # clyde image
spooked_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'Spooked_Ghost.png'), (45, 45))  # spooked image
dead_img = pygame.transform.scale(pygame.image.load(ghost_assets / f'dead.png'), (45, 45))              # dead image

blinky_x = 380                          # blinky position X
blinky_y = 438                          # blinky position Y
blinky_direction = 0                    # blinky direction numeric

inky_x = 430                            # inky position X
inky_y = 438                            # inky position Y
inky_direction = 2                      # inky direction numeric

pinky_x = 56                            # pinky position X
pinky_y = 58                            # pinky position Y
pinky_direction = 2                     # pinky direction numeric

clyde_x = 480                           # clyde position X
clyde_y = 438                           # clyde position Y
clyde_direction = 2                     # clyde direction numeric

blinky_dead = False                     # blinky is dead True or False
inky_dead = False                       # blinky is dead True or False
clyde_dead = False                      # blinky is dead True or False
pinky_dead = False                      # blinky is dead True or False

blinky_box = False                      # blinky is in box
inky_box = False                        # inky is in box
clyde_box = False                       # clyde is in box
pinky_box = False                       # pinky is in box

targets = [(packman_x, packman_y), (packman_x, packman_y), (packman_x, packman_y), (packman_x, packman_y)]      # setting target
ghost_speeds = [2, 2, 2, 2]             # variable for each ghost speed

game_over = False                       # variable for game over
game_won = False                        # variable for game won

class Ghost:                            # class Ghost
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):   # function for initialization
        self.x_pos = x_coord                            # variable for coordinate X
        self.y_pos = y_coord                            # variable for coordinate Y
        self.center_x = self.x_pos + 22                 # variable for center X
        self.center_y = self.y_pos + 22                 # variable for center Y
        self.target = target                            # variable for target
        self.speed = speed                              # variable for speed
        self.img = img                                  # variable for image
        self.direction = direct                         # variable for direction
        self.dead = dead                                # variable if ghost is dead
        self.in_box = box                               # variable if ghost is in box
        self.id = id                                    # variable for id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        # R, L, U, D
        num1 = ((height - 50) // 32)
        num2 = (width // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


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
def check_collision(score, powerup, powerup_counter, eaten_ghosts):
    height_tile = ((height - 50) // 32)     # height of a tile
    width_tile = (width // 30)              # width of a tile
    if 0 < packman_x < 870:
        if level[center_y // height_tile][center_x // width_tile] == 1:
            level[center_y // height_tile][center_x // width_tile] = 0
            score += 10
        if level[center_y // height_tile][center_x // width_tile] == 2:
            level[center_y // height_tile][center_x // width_tile] = 0
            score += 100
            powerup = True
            powerup_counter = 0
            eaten_ghosts = [False, False, False, False]
    return score, powerup, powerup_counter, eaten_ghosts

# ---------------- Move packman ----------------
def move_packman(packman_x, packman_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        packman_x += packman_speed
    elif direction == 1 and turns_allowed[1]:
        packman_x -= packman_speed
    if direction == 2 and turns_allowed[2]:
        packman_y -= packman_speed
    elif direction == 3 and turns_allowed[3]:
        packman_y += packman_speed
    return packman_x, packman_y

# ---------------- Draw stuff ----------------
def draw_stuff():
    '''
    shows score at the bottom left corner, blue circle if the powerup is active
    '''
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

# ---------------- Get targets ----------------
def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if packman_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if packman_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghosts[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghosts[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (packman_x, packman_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghosts[1]:
            ink_target = (runaway_x, packman_y)
        elif not inky.dead and eaten_ghosts[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (packman_x, packman_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (packman_x, runaway_y)
        elif not pinky.dead and eaten_ghosts[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (packman_x, packman_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghosts[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghosts[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (packman_x, packman_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (packman_x, packman_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (packman_x, packman_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (packman_x, packman_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (packman_x, packman_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


# ------------ Running game ------------
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
    if powerup and powerup_counter < 600:
        powerup_counter += 1
    elif powerup and powerup_counter >= 600:
        powerup_counter = 0
        powerup = False
        eaten_ghosts = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    center_x = packman_x + 23  # center position of packman in OX
    center_y = packman_y + 24  # center position of packman in OY
    screen.fill('black')            # background color
    draw_board()                    # drawing game board
    player_circle = pygame.draw.circle(screen, (0, 0, 0, 128), (center_x, center_y), 20, 2)
    draw_player()                   # drawing player
    draw_stuff()                    # drawing miscellaneous
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghosts[0]:
        ghost_speeds[0] = 2
    if eaten_ghosts[1]:
        ghost_speeds[1] = 2
    if eaten_ghosts[2]:
        ghost_speeds[2] = 2
    if eaten_ghosts[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4




    turns_allowed = check_position(center_x, center_y)
    if moving:
        packman_x, packman_y = move_packman(packman_x, packman_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, powerup_count, eaten_ghosts = check_collision(score, powerup, powerup_counter, eaten_ghosts)
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                packman_x = 450
                packman_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghosts[0] and not blinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            packman_x = 450
            packman_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghosts[1] and not inky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            packman_x = 450
            packman_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghosts[2] and not pinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            packman_x = 450
            packman_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghosts[3] and not clyde.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            packman_x = 450
            packman_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghosts[0]:
        blinky_dead = True
        eaten_ghosts[0] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghosts[1]:
        inky_dead = True
        eaten_ghosts[1] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghosts[2]:
        pinky_dead = True
        eaten_ghosts[2] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghosts[3]:
        clyde_dead = True
        eaten_ghosts[3] = True
        score += (2 ** eaten_ghosts.count(True)) * 100

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

            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                packman_x = 450
                packman_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(lvl_1)
                game_over = False
                game_won = False

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

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()