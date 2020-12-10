from itertools import chain
from os import path

import pygame

import Constants

images_dir = path.join(path.dirname(__file__), 'images')

zombie_move = [pygame.image.load(path.join(images_dir, 'zombie_move1.png')),
               pygame.image.load(path.join(images_dir, 'zombie_move2.png')),
               pygame.image.load(path.join(images_dir, 'zombie_move3.png')),
               pygame.image.load(path.join(images_dir, 'zombie_move4.png')),
               pygame.image.load(path.join(images_dir, 'zombie_move5.png'))]

zombie_attack = [pygame.image.load(path.join(images_dir, 'zombie_attack1.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack2.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack3.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack4.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack5.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack6.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack7.png')),
                 pygame.image.load(path.join(images_dir, 'zombie_attack8.png'))]

zombie_die = [pygame.image.load(path.join(images_dir, 'zombie_die1.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die2.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die3.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die4.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die5.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die6.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die7.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die8.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die9.png')),
              pygame.image.load(path.join(images_dir, 'zombie_die10.png'))]

for anim in chain(zombie_move, zombie_attack, zombie_die):
    anim.set_colorkey(Constants.monster_background)
