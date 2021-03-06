import pygame

import Hero
import draw_images
import math_functions
import Constants


class Enemy:
    '''
    здесь содержаться все типы врагов и их поведение
    soldier - обычный стрелок
    zombie - милишник
    mage - маг, призывающий микрочеликов
    '''
    def __init__(self):
        self.range_to_attack = 400
        self.range_to_move = 500
        self.hp = 100
        self.x = 500
        self.y = 500
        self.radius = 25
        self.V = 3
        self.now_action = "move"
        self.time_to_shoot = 1.5
        self.time_to_spawn = 3
        self.time_last_shoot = 0
        self.time_last_spawn = 0
        self.type = "none"
        self.slow = 0
        self.time_get_slow = 0
        self.last_fire_tick = 0
        self.next_fire_tick = 15
        self.time_end_fire = 0
        self.fire_damage = 0
        self.image_index = 0
        self.Vx = 0
        self.current_animation = []
        self.anim_speed = 0

    def move(self):
        self.y += self.V * math_functions.sin(self.x, self.y, Hero.hero.x, Hero.hero.y) * (1 - self.slow)
        self.x += self.V * math_functions.cos(self.x, self.y, Hero.hero.x, Hero.hero.y) * (1 - self.slow)
        self.Vx = self.V * math_functions.cos(self.x, self.y, Hero.hero.x, Hero.hero.y) * (1 - self.slow)

    def action(self):
        if self.time_end_fire > Hero.var.TIME:
            if Hero.var.TIME > self.last_fire_tick + self.next_fire_tick:
                self.last_fire_tick = Hero.var.TIME
                self.hp -= self.fire_damage

        if self.slow != 0:
            if Hero.var.TIME > self.time_end_slow:
                self.slow = 0
        if self.now_action == "move":
            self.move()
        if self.now_action == "attack":
            self.SHOOT()
            if self.type == "mage":
                self.SPAWN()

        if math_functions.distance_to(self.x, self.y, Hero.hero.x, Hero.hero.y) > self.range_to_move:
            self.now_action = "move"
        if math_functions.distance_to(self.x, self.y, Hero.hero.x, Hero.hero.y) < self.range_to_attack:
            self.now_action = "attack"

    def draw(self):
        if self.type == "mage":
            if self.now_action == "move":
                self.current_animation = draw_images.mage_move
            if self.now_action == "attack":
                self.current_animation = draw_images.mage_attack

        if self.type == "zombie":
            if self.now_action == "move":
                self.current_animation = draw_images.zombie_move
            if self.now_action == "attack":
                self.current_animation = draw_images.zombie_attack

        if self.type == "soldier":
            if self.now_action == "move":
                self.current_animation = draw_images.summon_move
            if self.now_action == "attack":
                self.current_animation = draw_images.summon_attack

        if self.image_index >= len(self.current_animation):
            self.image_index = 0
        self.image = self.current_animation[self.image_index]
        if math_functions.cos(self.x, self.y, Hero.hero.x, Hero.hero.y) < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        Constants.screen.blit(self.image, (self.x - Hero.my_map.x - 25, self.y - Hero.my_map.y - 25))

        if self.anim_speed >= 3:
            self.anim_speed = 0
        self.anim_speed += 1
        if self.anim_speed == 1:
            self.image_index += 1

    def SHOOT(self):
        '''
        стрельба врагов
        b.type=="melee" означает что атака ближнего боя
        пуля подобной атаки не рисуется, но нужна для проверки коллизии
        '''
        if Hero.var.TIME > self.time_to_shoot * Constants.FPS + self.time_last_shoot:
            b = Bullet()
            if self.type == "soldier":
                b.type = "medium"
                b.V = 12
                b.radius = 10
            if self.type == "mage":
                b.type = "fireball"
                b.V = 6
                b.radius = 20
            if self.type == "zombie":
                b.V = 15
                b.type = "melee"
            b.x = self.x
            b.y = self.y
            b.Vy += b.V * math_functions.sin(self.x, self.y, Hero.hero.x, Hero.hero.y)
            b.Vx += b.V * math_functions.cos(self.x, self.y, Hero.hero.x, Hero.hero.y)
            Constants.BULLETS.append(b)
            b.radius = 10
            self.time_last_shoot = Hero.var.TIME

    def SPAWN(self):
        '''призыв одного моба другим'''
        if Hero.var.TIME > self.time_to_spawn * Constants.FPS + self.time_last_spawn:
            e = Enemy()
            e.x = self.x + Hero.randint(50, 100) * Hero.randint(-1, 1)
            e.y = self.y + Hero.randint(50, 100) * Hero.randint(-1, 1)
            e.type = "zombie"
            e.range_to_move = Hero.hero.radius * 1.2
            e.range_to_attack = Hero.hero.radius * 1.3
            e.radius = e.radius * 0.75
            e.color = Constants.GREEN
            Constants.ENEMIES.append(e)
            self.time_last_spawn = Hero.var.TIME


class Dead:
    '''
    класс трупов для
    анимации смерти врагов
    '''

    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = "none"
        self.time_for_destroy = 0
        self.time_exist = 30
        self.image_index = 0
        self.anim_speed = 0
        self.current_animation = []

    def draw(self):
        if self.type == "zombie":
            self.current_animation = draw_images.zombie_die
        if self.type == "mage":
            self.current_animation = draw_images.mage_die  
        if self.type == "soldier":
            self.current_animation = draw_images.summon_die

                
        if self.image_index >= len(self.current_animation):
            return
        self.image = self.current_animation[self.image_index]
        if math_functions.cos(self.x, self.y, Hero.hero.x, Hero.hero.y) < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        Constants.screen.blit(self.image, (self.x - Hero.my_map.x - 25, self.y - Hero.my_map.y - 25))

        if self.anim_speed >= 3:
            self.anim_speed = 0
        self.anim_speed += 1
        if self.anim_speed == 1:
            self.image_index += 1


class Bullet:
    '''пули ВРАГОВ'''

    def __init__(self):
        self.type = "medium"
        self.x = 0
        self.y = 0
        self.speed = 30
        self.V = 10
        self.Vy = 0
        self.Vx = 0
        self.radius = 1
        self.exist = 1

    def move(self):
        self.x += self.Vx
        self.y += self.Vy

    def draw(self):
        if self.type != "melee":
            pygame.draw.circle(Constants.screen, Constants.RED,
                               (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y)), self.radius)
