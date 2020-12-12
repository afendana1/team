import pygame

loose = 0
distance_to_mouse = 0
WIDTH = 1500
HEIGHT = 1000
BULLETS = []
hero_BULLETS = []

SURFACES = []
ENEMIES = []
Deads = []
DEAD = []
FPS = 30
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
monster_background = (0, 114, 188)
rnd = 0

room_size = 20
block_size = 50
number_rooms_H = 5
number_rooms_W = 5
number_walls_H = number_rooms_H * room_size + 1
number_walls_W = number_rooms_W * room_size + 1
ROOMS = []

WALLS = []
for i in range(number_rooms_H):
    ROOMS.append([0] * number_rooms_W)
for i in range(number_walls_H):
    WALLS.append([0] * number_walls_H)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

