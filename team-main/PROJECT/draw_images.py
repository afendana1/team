from os import path
import pygame
from pygame.draw import *

from Constants import *

images_dir = path.join(path.dirname(__file__), 'images')

animations = []

zombie_move = [ pygame.image.load(path.join(images_dir, 'zombie_move1.png')),
                pygame.image.load(path.join(images_dir, 'zombie_move2.png')),
                pygame.image.load(path.join(images_dir, 'zombie_move3.png')),
                pygame.image.load(path.join(images_dir, 'zombie_move4.png')),
                pygame.image.load(path.join(images_dir, 'zombie_move5.png')) ]

zombie_attack = [ pygame.image.load(path.join(images_dir, 'zombie_attack1.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack2.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack3.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack4.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack5.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack6.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack7.png')),
                  pygame.image.load(path.join(images_dir, 'zombie_attack8.png')) ]

zombie_die = [ pygame.image.load(path.join(images_dir, 'zombie_die1.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die2.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die3.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die4.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die5.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die6.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die7.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die8.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die9.png')),
               pygame.image.load(path.join(images_dir, 'zombie_die10.png')) ]
       
animations.extend(zombie_move)
animations.extend(zombie_attack)
animations.extend(zombie_die)

for anim in animations:
    anim.set_colorkey(monster_background)

