import pygame             # importing pygame
from board import lvl_1   # importing made board lvl_1 from board

pygame.init()             # initialise all pygame modules

#Game Window

width = 900               # seting width
height = 950              # seting height
screen = pygame.display.set_mode([width, height])  # making screen by height and width
timer = pygame.time.Clock()                        # creating to help track time
fps = 60                                           # frames per second
font = pygame.font.SysFont('calibri', 20)          # setting font
