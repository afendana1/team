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

summon_move = [pygame.image.load(path.join(images_dir, 'summon_move1.png')),
               pygame.image.load(path.join(images_dir, 'summon_move2.png')),
               pygame.image.load(path.join(images_dir, 'summon_move3.png')),
               pygame.image.load(path.join(images_dir, 'summon_move4.png')),
               pygame.image.load(path.join(images_dir, 'summon_move5.png'))]

summon_attack = [pygame.image.load(path.join(images_dir, 'summon_attack1.png')),
                 pygame.image.load(path.join(images_dir, 'summon_attack2.png')),
                 pygame.image.load(path.join(images_dir, 'summon_attack3.png')),
                 pygame.image.load(path.join(images_dir, 'summon_attack4.png')),
                 pygame.image.load(path.join(images_dir, 'summon_attack5.png')),]

summon_die = [pygame.image.load(path.join(images_dir, 'summon_die1.png')),
              pygame.image.load(path.join(images_dir, 'summon_die2.png')),
              pygame.image.load(path.join(images_dir, 'summon_die3.png')),
              pygame.image.load(path.join(images_dir, 'summon_die4.png')),
              pygame.image.load(path.join(images_dir, 'summon_die5.png')),
              pygame.image.load(path.join(images_dir, 'summon_die6.png')),
              pygame.image.load(path.join(images_dir, 'summon_die7.png')),
              pygame.image.load(path.join(images_dir, 'summon_die8.png')),
              pygame.image.load(path.join(images_dir, 'summon_die9.png')),
              pygame.image.load(path.join(images_dir, 'summon_die10.png')),
              pygame.image.load(path.join(images_dir, 'summon_die11.png')),]

mage_move = [pygame.image.load(path.join(images_dir, 'monster_move1.png')), 
             pygame.image.load(path.join(images_dir, 'monster_move2.png')),
             pygame.image.load(path.join(images_dir, 'monster_move3.png')),
             pygame.image.load(path.join(images_dir, 'monster_move4.png'))]

mage_attack = [pygame.image.load(path.join(images_dir, 'monster_attack1.png')),
               pygame.image.load(path.join(images_dir, 'monster_attack2.png')),
               pygame.image.load(path.join(images_dir, 'monster_attack3.png')),
               pygame.image.load(path.join(images_dir, 'monster_attack4.png'))]

mage_die = [pygame.image.load(path.join(images_dir, 'monster_die1.png')),
            pygame.image.load(path.join(images_dir, 'monster_die2.png')),
            pygame.image.load(path.join(images_dir, 'monster_die3.png')),
            pygame.image.load(path.join(images_dir, 'monster_die4.png')),
            pygame.image.load(path.join(images_dir, 'monster_die5.png')),
            pygame.image.load(path.join(images_dir, 'monster_die6.png')),
            pygame.image.load(path.join(images_dir, 'monster_die7.png')),
            pygame.image.load(path.join(images_dir, 'monster_die8.png')),
            pygame.image.load(path.join(images_dir, 'monster_die9.png')),
            pygame.image.load(path.join(images_dir, 'monster_die10.png'))]

hero_stand = [pygame.image.load(path.join(images_dir, 'hero_stand1.png')),
              pygame.image.load(path.join(images_dir, 'hero_stand2.png')),
              pygame.image.load(path.join(images_dir, 'hero_stand3.png')),
              pygame.image.load(path.join(images_dir, 'hero_stand4.png'))]

hero_move = [pygame.image.load(path.join(images_dir, 'hero_walk1.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk2.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk3.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk4.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk5.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk6.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk7.png')),
             pygame.image.load(path.join(images_dir, 'hero_walk8.png')),]


for anim in chain(zombie_move, zombie_attack, zombie_die,
                  summon_move, summon_attack, summon_die,
                  mage_move, mage_attack, mage_die,
                  hero_stand, hero_move):
  anim.set_colorkey(Constants.monster_background)

