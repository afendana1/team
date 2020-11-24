import pygame
from pygame.draw import *
from random import randint
import numpy as np
import matplotlib as mp
pygame.init()
loose=0
distance_to_mouse=0
zzz=0
WIDTH=1000
HEIGHT=600
BULLETS=[]
hero_BULLETS=[]
ENEMIES=[]
FPS=30
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE =(255, 255, 255)
TIME=0
rnd=0
mouse_proect_x=0
mouse_proect_y=0

screen = pygame.display.set_mode(( WIDTH, HEIGHT))

class Hero:
    'игрок'
    def __init__(self):
        self.hp=100
        self.x=600
        self.y=100
        self.radius=25
        self.Vx=0
        
        self.scatter=0
        self.shoot_side=1
        self.weapon_type="uzi"
        self.time_last_shoot_uzi=0
        self.time_next_shoot_uzi=1
        self.time_last_shoot_snipe=0
        self.time_next_shoot_snipe=45
        self.time_last_shoot_uzi=0
        self.time_next_shoot_uzi=1
        
        self.blink_cd=60
        self.last_use_blink=0
    def move(self):       
        self.x+=self.Vx
    def draw(self):
        circle(screen, (YELLOW), (round(self.x), round(self.y)), self.radius)
    def SHOOT(self):
        if self.weapon_type == "uzi":
            if TIME>self.time_last_shoot_uzi+self.time_next_shoot_uzi:
                b=hero_Bullet()
                b.x=hero.x+mouse_proect_y*self.radius*self.shoot_side
                b.y=hero.y-mouse_proect_x*self.radius*self.shoot_side
                self.scatter=np.pi*randint(-10,10)/180
                b.Vx=b.V*np.cos((np.arccos(mouse_proect_x)+self.scatter))
                b.Vy=b.V*np.sin((np.arcsin(mouse_proect_y)+self.scatter))
                hero_BULLETS.append(b)
                self.shoot_side=self.shoot_side*(-1)
                self.time_last_shoot_uzi=TIME
                b.type="uzi"
        if self.weapon_type == "snipe":
            if TIME>self.time_last_shoot_snipe+self.time_next_shoot_snipe:
                b=hero_Bullet()
                b.x=self.x
                b.y=self.y
                b.radius=5
                b.type="snipe"
                b.Vx=b.V_snipe*mouse_proect_x
                b.Vy=b.V_snipe*mouse_proect_y
                hero_BULLETS.append(b)
                self.time_last_shoot_snipe=TIME
                
                
                
    
class hero_Bullet:
    def __init__(self):
        self.x=0
        self.y=0
        self.Vx=0
        self.Vy=0
        self.V=40
        self.V_snipe=100
        self.radius=2
        self.type="uzi"
    def move(self):
        self.x+=self.Vx
        self.y+=self.Vy 
        circle(screen, (CYAN), (round(self.x), round(self.y)),self.radius)
        
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
    def move(self):
        self.y+=self.V*sin(self.x,self.y,hero.x,hero.y)
        self.x+=self.V*cos(self.x,self.y,hero.x,hero.y)   
    def action(self):
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
        circle(screen, (self.color), (round(self.x), round(self.y)),round(self.radius))
        
          

        
    def SHOOT(self):
        if TIME > self.time_to_shoot*FPS+self.time_last_shoot:
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
            self.time_last_shoot=TIME
    def SPAWN(self):
        if TIME > self.time_to_spawn*FPS+self.time_last_spawn:
            e=Enemy()
            e.x=self.x+randint(50,100)*randint(-1,1)
            e.y=self.y+randint(50,100)*randint(-1,1)
            e.type="zombie"
            e.range_to_move = hero.radius*1.2
            e.range_to_attack = hero.radius*1.3
            e.radius=e.radius*0.75
            e.color=GREEN
            ENEMIES.append(e)
            self.time_last_spawn=TIME
        
class Bullet:
    
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
        if self.type!="melee":
            circle(screen, (RED), (round(self.x), round(self.y)),self.radius)
        self.x+=self.Vx
        self.y+=self.Vy
        
class Aim:
    def __init__(self):
        self.x=0
        self.y=0
        self.size=4
        self.range=300
    def draw(self):

        if distance_to(hero.x,hero.y,self.x,self.y)<self.range:
            
            rect(screen, (WHITE), (round(self.x-self.size//2),round(self.y-self.size//2), self.size, self.size), )
            self.mx=self.x
            self.my=self.y
        else:         
            rect(screen, (WHITE), (round(hero.x+self.range*mouse_proect_x),round(hero.y+self.range*mouse_proect_y), self.size, self.size), )
            self.mx, self.my=round(hero.x+self.range*mouse_proect_x), round(hero.y+self.range*mouse_proect_y)
            
        
        
        
def distance_to(x1,y1,x2,y2):
    '''функция для опредения растояния'''
    return(((x1-x2)**2+(y1-y2)**2)**0.5)
def cos(x1,y1,x2,y2):
    return((x2-x1)/distance_to(x1,y1,x2,y2))
def sin(x1,y1,x2,y2):
    return((y2-y1)/distance_to(x1,y1,x2,y2))
def inter_arena(x,y):
    inter_a=True
    if x>WIDTH:
        inter_a=False
    if x<0:
        inter_a=False
    if y>HEIGHT:
        inter_a=False
    if y<0:
        inter_a=False
    return(inter_a)
def spawner():
    '''спавнер мобов'''
    if randint(1,100)<100//FPS:
        e=Enemy()
        rnd=randint(1,2)
        if rnd == 1:
            e.x=randint(1,WIDTH)
            e.y=randint(0,1)*HEIGHT
        if rnd == 2:
            e.x=randint(0,1)*WIDTH
            e.y=randint(1,HEIGHT)
  
        rnd=randint(1,3)
        if rnd==1:
            e.type="soldier" 
            e.range_to_move = 350
            e.range_to_attack = 250
            e.color=MAGENTA
        if rnd==2:
            e.type="zombie"
            e.range_to_move = hero.radius*1.2
            e.range_to_attack = hero.radius*1.3
            e.color=GREEN
        if rnd==3:
            e.type="mage"
            e.range_to_move = 400
            e.range_to_attack = 300
            e.color=BLUE
        e.now_action="move"
        ENEMIES.append(e)
hero=Hero()
aim=Aim()
pygame.mouse.set_visible(False)
# тест
TIME=0
clock = pygame.time.Clock()
finished = False


while not finished:
         
    if zzz==1:
        hero.SHOOT()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
            hero.x-=5
    if keys[pygame.K_d]:
            hero.x+=5
    if keys[pygame.K_s]:
            hero.y+=5
    if keys[pygame.K_w]:
            hero.y-=5

       
    clock.tick(FPS)
    TIME+=1
    hero.draw()
    hero.move()
    spawner()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
      
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                    zzz=1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                     zzz=0
        if event.type == pygame.MOUSEMOTION:
            mouse_proect_x=cos(hero.x,hero.y,event.pos[0],event.pos[1])
            mouse_proect_y=sin(hero.x,hero.y,event.pos[0],event.pos[1]) 
                
            aim.x, aim.y = event.pos[0], event.pos[1]        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                hero.weapon_type="uzi"
                
            if event.key == pygame.K_2:
                hero.weapon_type="snipe"
           
            if event.key == pygame.K_SPACE:
                if TIME>hero.blink_cd+hero.last_use_blink:
                    hero.x=aim.mx
                    hero.y=aim.my
                    hero.last_use_blink=TIME

                
    for b in BULLETS:
        b.move()
        if distance_to(b.x,b.y,hero.x,hero.y)<b.radius+hero.radius:
            BULLETS.remove(b)
        if inter_arena(b.x,b.y)==False:
            if b in BULLETS:
                BULLETS.remove(b) 
    for h_b in hero_BULLETS:
        h_b.move()
        if inter_arena(h_b.x,h_b.y)==False:
            hero_BULLETS.remove(h_b)
            
        
    for e in ENEMIES:
        e.action()
        for h_b in hero_BULLETS:
            if distance_to(h_b.x,h_b.y,e.x,e.y)<e.radius+h_b.radius:
                if h_b.type=="uzi":
                    e.hp-=20
                if h_b.type=="snipe":
                    e.hp-=100
                hero_BULLETS.remove(h_b)
                if e.hp <= 0:
                    ENEMIES.remove(e)
    aim.draw()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
