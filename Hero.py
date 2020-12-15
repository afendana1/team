from random import randint

import numpy as np
from pygame.draw import *
import pygame

import Constants
import var
import draw_images

class Play_button:
	def __init__(self):
		self.x=Constants.WIDTH//6
		self.y=Constants.HEIGHT//4
		self.x_size=Constants.WIDTH//2
		self.y_size=Constants.HEIGHT//6
	def draw(self):
		rect(Constants.screen, Constants.GREEN, (self.x, self.y, self.x_size, self.y_size), )



class Aim:
    '''прицел
     пока нормально не работает '''

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 4
        self.range = 300

    def draw(self):
        rect(Constants.screen, Constants.WHITE, (round(self.x - self.size // 2), round(self.y - self.size // 2), self.size, self.size), )
        self.mx = self.x
        self.my = self.y


class Map:
    def __init__(self):
        self.x = 0
        self.y = 0

    def change_coords(self):
        self.x = hero.x + aim.x // 8 - Constants.WIDTH // 2
        self.y = hero.y + aim.y // 8 - Constants.HEIGHT // 2


class Hero:
    'игрок'
    def __init__(self):
        self.hp = 100
        self.x = Constants.number_walls_W * Constants.block_size // 2
        self.y = Constants.number_walls_H * Constants.block_size // 2
        self.radius = 25
        self.proect_Vx = 0
        self.proect_Vy = 0
        self.Vx = 0
        self.Vy = 0
        self.V = 10
        self.right_arm_x = self.radius  # рука откуда ведеться стрельба
        self.shooting = 0  # стреляет ли сейчас наш герой
        
        # анимация героя
        self.current_animation = [] 
        self.image_index = 0 
        self.anim_speed = 0

        # способности героя:
        self.blink_cd = 60
        self.last_use_blink = 0

    def draw(self):
        if self.proect_Vx != 0 or self.proect_Vy != 0:
            self.current_animation = draw_images.hero_move 
        else:
            self.current_animation = draw_images.hero_stand

        if self.image_index >= len(self.current_animation):
            self.image_index = 0
        self.image = self.current_animation[self.image_index]
        if (var.mouse_projection_x < 0) and (var.TIME>30):
            self.image = pygame.transform.flip(self.image, True, False)
        Constants.screen.blit(self.image, (self.x - my_map.x - 65, self.y - my_map.y - 80))

        if self.anim_speed >= 3:
            self.anim_speed = 0
        self.anim_speed += 1
        if self.anim_speed == 1:
            self.image_index += 1

    def move(self):
        if self.proect_Vx ** 2 + self.proect_Vy ** 2 > 0:
            self.Vx = self.V * self.proect_Vx / (self.proect_Vx ** 2 + self.proect_Vy ** 2) ** 0.5
            self.Vy = self.V * self.proect_Vy / (self.proect_Vx ** 2 + self.proect_Vy ** 2) ** 0.5
            self.x += self.Vx
            self.y += self.Vy

    def calculate_speed(self):
        if self.proect_Vx ** 2 + self.proect_Vy ** 2 > 0:
            self.Vx = self.V * self.proect_Vx / (self.proect_Vx ** 2 + self.proect_Vy ** 2) ** 0.5
            self.Vy = self.V * self.proect_Vy / (self.proect_Vx ** 2 + self.proect_Vy ** 2) ** 0.5


class hero_Weapon:
    '''оружие героя'''
    def __init__(self):
        self.scatter = 0
        self.shoot_side = 1
        self.weapon_type = "gun"

        self.time_last_shoot_uzi = 0
        self.time_next_shoot_uzi = 1

        self.time_last_shoot_snipe = 0
        self.time_next_shoot_snipe = 45

        self.time_last_shoot_shock = 0
        self.time_next_shoot_shock = 60

        self.time_last_shoot_gun = 0
        self.time_next_shoot_gun = 5

        self.time_next_shoot_ice_sphere = 10
        self.time_last_shoot_ice_sphere = 0
        self.time_slow_duration = 60
        self.slow = 0.5

        self.time_last_shoot_fire_sphere = 0
        self.time_next_shoot_fire_sphere = 20

    def SHOOT(self):
        '''стрельба героя'''
        if self.weapon_type == "uzi":
            if var.TIME > self.time_last_shoot_uzi + self.time_next_shoot_uzi:
                b = hero_Bullet()
                b.x = hero.x + hero.right_arm_x * self.shoot_side
                b.y = hero.y
                self.scatter = np.pi * randint(-10, 10) / 180  # вычисление угла разброса
                b.Vx = b.V * np.cos((np.arccos(var.mouse_projection_x) + self.scatter))  # разброс
                b.Vy = b.V * np.sin((np.arcsin(var.mouse_projection_y) + self.scatter))  # разброс
                Constants.hero_BULLETS.append(b)
                self.shoot_side = self.shoot_side * (-1)  # нужно когда стрельба идет с двкх рук(например узи)
                self.time_last_shoot_uzi = var.TIME
                b.type = "uzi"
        if self.weapon_type == "snipe":
            if var.TIME > self.time_last_shoot_snipe + self.time_next_shoot_snipe:
                b = hero_Bullet()
                b.x = hero.x + hero.right_arm_x
                b.y = hero.y
                b.radius = 5
                b.type = "snipe"
                b.Vx = b.V_snipe * var.mouse_projection_x
                b.Vy = b.V_snipe * var.mouse_projection_y
                Constants.hero_BULLETS.append(b)
                self.time_last_shoot_snipe = var.TIME
        if self.weapon_type == "shock":
            if var.TIME > self.time_last_shoot_shock + self.time_next_shoot_shock:
                for i in range(40):
                    b = hero_Bullet()
                    b.x = hero.x
                    b.y = hero.y
                    b.radius = 4
                    b.type = "shock"
                    b.Vx = 30 * np.cos(2 * np.pi * i / 40)
                    b.Vy = 30 * np.sin(2 * np.pi * i / 40)
                    Constants.hero_BULLETS.append(b)
                self.time_last_shoot_shock = var.TIME
        if self.weapon_type == "gun":
            if var.TIME > self.time_last_shoot_gun + self.time_next_shoot_gun:
                b = hero_Bullet()
                b.x = hero.x + hero.right_arm_x
                b.y = hero.y
                b.radius = 3
                b.type = "gun"
                b.Vx = b.V_snipe * var.mouse_projection_x
                b.Vy = b.V_snipe * var.mouse_projection_y
                Constants.hero_BULLETS.append(b)
                self.time_last_shoot_gun = var.TIME
        if self.weapon_type == "ice_sphere":
            if var.TIME > self.time_last_shoot_ice_sphere + self.time_next_shoot_ice_sphere:
                b = hero_Bullet()
                b.x = hero.x + hero.right_arm_x
                b.y = hero.y
                b.radius = 6
                b.type = "ice_sphere"
                b.Vx = b.V_sphere * var.mouse_projection_x
                b.Vy = b.V_sphere * var.mouse_projection_y
                Constants.hero_BULLETS.append(b)
                self.time_last_shoot_ice_sphere = var.TIME
        if self.weapon_type == "fire_sphere":
            if var.TIME > self.time_last_shoot_fire_sphere + self.time_next_shoot_fire_sphere:
                b = hero_Bullet()
                b.x = hero.x + hero.right_arm_x
                b.y = hero.y
                b.radius = 5
                b.type = "fire_sphere"
                b.Vx = b.V_sphere * var.mouse_projection_x
                b.Vy = b.V_sphere * var.mouse_projection_y
                Constants.hero_BULLETS.append(b)
                self.time_last_shoot_fire_sphere = var.TIME


class hero_Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.V = 20
        self.V_snipe = 40
        self.V_sphere = 15
        self.radius = 2
        self.type = "uzi"
        self.ice_slow = 0.5
        self.time_slow_duration = 60

    def move(self):
        self.x += self.Vx
        self.y += self.Vy

    def draw(self):
        circle(Constants.screen, (Constants.CYAN), (int(round(self.x - my_map.x)), int(round(self.y - my_map.y))), self.radius)


class fire_floor_surfaces:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 80
        self.damage = 10
        self.debaf_duration = 90
        self.tick_time = 15
        self.color = Constants.RED
        self.time_exist = 60
        self.time_for_destroy = 0

    def draw(self):
        circle(Constants.screen, (self.color), (int(round(self.x - my_map.x)), int(round(self.y - my_map.y))), self.radius)

class Healthbar:
    #Шкала отображения здоровья героя
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = Constants.GREEN
        self.height = Constants.HEIGHT / 20

    def draw(self):
        if 20 < hero.hp <= 50:
            self.color = Constants.YELLOW
        if hero.hp <= 20:
            self.color = Constants.RED
        self.lenth =(hero.hp /100)* (Constants.WIDTH / 7 )
        pygame.draw.rect(Constants.screen, (self.color), ((self.x, self.y), (self.lenth, self.height)))




play_button=Play_button()
my_map = Map()
hero = Hero()
hero_weapon1 = hero_Weapon()
hero_weapon2 = hero_Weapon()
hero_weapon1.weapon_type="uzi"
hero_select_weapon=hero_Weapon()
hero_select_weapon=hero_weapon1
aim = Aim()
healthbar = Healthbar()
