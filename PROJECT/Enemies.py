import pygame
from pygame.draw import *
from random import randint
import numpy as np
import matplotlib as mp

from Constants import *
import var
from math_functions import *
from Hero import *

class Enemy:
    '''здесь содержаться все типы врагов и их поведение
    soldier - обычный стрелок
    zombie - милишник
    mage - маг, призывающий микрочеликов

    
    '''
    def __init__(self):

        self.hp=100
        self.x=500
        self.y=500
        self.radius=25
        self.V=3
        self.now_action="move"
        self.time_to_shoot=1.5
        self.time_to_spawn=3
        self.time_last_shoot=0
        self.time_last_spawn=0
        self.type="soldier"
        self.slow=0
        self.time_get_slow=0
        self.last_fire_tick=0
        self.next_fire_tick=15
        self.time_end_fire=0
        self.fire_damage=0

    def move(self):
        self.y+=self.V*sin(self.x,self.y,hero.x,hero.y)*(1-self.slow)
        self.x+=self.V*cos(self.x,self.y,hero.x,hero.y)*(1-self.slow)   
    def action(self):
        if self.time_end_fire>var.TIME:
            if var.TIME>self.last_fire_tick+self.next_fire_tick:
                self.last_fire_tick=var.TIME
                self.hp-=self.fire_damage


        if self.slow !=0:
            if var.TIME>self.time_end_slow:
                self.slow = 0
        if self.now_action == "move":
            self.move()
        if self.now_action == "attack":
            self.SHOOT()
            if self.type == "mage":
                self.SPAWN()
            
        if distance_to(self.x,self.y,hero.x ,hero.y )>self.range_to_move:
            self.now_action="move"
        if distance_to(self.x,self.y,hero.x ,hero.y )<self.range_to_attack:
            self.now_action="attack"
    def draw(self):    
        circle(screen, (self.color), (round(self.x-my_map.x), round(self.y-my_map.y)),round(self.radius))
        
          

        
    def SHOOT(self):
        '''стрельба врагов
            b.type=="melee" означает что атака ближнего боя
            пуля подобной атаки не рисуется, но нужна для проверки коллизии '''
        if var.TIME > self.time_to_shoot*FPS+self.time_last_shoot:
            b = Bullet()
            if self.type=="soldier":
                b.type="medium"
                b.V=12
                b.radius=10
            if self.type=="mage":
                b.type="fireball"
                b.V=6
                b.radius=20
            if self.type=="zombie":
                b.V=15
                b.type="melee"
            b.x = self.x
            b.y = self.y
            b.Vy+=b.V*sin(self.x,self.y,hero.x,hero.y)
            b.Vx+=b.V*cos(self.x,self.y,hero.x,hero.y)
            BULLETS.append(b)
            b.radius=10
            self.time_last_shoot=var.TIME
    def SPAWN(self):
        '''призыв одного моба другим'''
        if var.TIME > self.time_to_spawn*FPS+self.time_last_spawn:
            e=Enemy()
            e.x=self.x+randint(50,100)*randint(-1,1)
            e.y=self.y+randint(50,100)*randint(-1,1)
            e.type="zombie"
            e.range_to_move = hero.radius*1.2
            e.range_to_attack = hero.radius*1.3
            e.radius=e.radius*0.75
            e.color=GREEN
            ENEMIES.append(e)
            self.time_last_spawn=var.TIME
        
class Bullet:
    '''пули ВРАГОВ'''
    def __init__(self):
        self.type="medium"
        self.x=0
        self.y=0
        self.speed = 30
        self.V=10
        self.Vy=0
        self.Vx=0
        self.radius=1
        self.exist=1  
    def move(self):
        self.x+=self.Vx
        self.y+=self.Vy
    def draw(self):
        if self.type!="melee":
            circle(screen, (RED), (round(self.x-my_map.x), round(self.y-my_map.y)),self.radius)
        

        
