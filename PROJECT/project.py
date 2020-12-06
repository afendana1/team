import pygame
from pygame.draw import *
from random import randint
import numpy as np
import matplotlib as mp
from Constants import *
import var
from math_functions import *
from Hero import *
from Enemies import *


class Walls():
    def __init__(self):
        self.x=100
        self.y=100
        self.size=50
    def draw(self):
        if inter_arena(self.x,self.y)==True:
            rect(screen, (WHITE), (round(self.x-my_map.x),round(self.y-my_map.y), self.size, self.size), )
    
        

def inter_arena(x,y):
    '''проверка нахождения внутри арены 
       True - внутри; False - снаружи'''
    inter_a=True
    if distance_to(x,y,hero.x,hero.y)>((WIDTH//2)**2+(HEIGHT//2)**2)**0.5*1.5:
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
def labirint_constr(i,j,steps):
    if steps>0:
        if ROOMS[i][j]!=1:
            steps-=1
            ROOMS[i][j]=1
        rnd=randint(1,4)
        
        if rnd==1:
            if i<number_rooms_H-1:
                labirint_constr(i+1,j,steps)
            else:
                labirint_constr(i,j,steps)
                
        if rnd==2:
            if i>0:
                labirint_constr(i-1,j,steps)
            else:
                labirint_constr(i,j,steps)
        if rnd==3:
            if j <number_rooms_W-1:
                labirint_constr(i,j+1,steps)
            else:
                labirint_constr(i,j,steps)
        if rnd==4:
            if j>0:
                labirint_constr(i,j-1,steps)
            else:
                labirint_constr(i,j,steps)


def create_LABIRINT():



# генерация комнат
    labirint_constr(2,2,7)

# создание стен комнат
    for i in range(number_rooms_H):
        for j in range(number_rooms_W):
            if ROOMS[i][j]==1:
                room_size_x=randint(1,3)
                room_size_y=randint(1,3)
                for k in range(room_size_y,room_size-room_size_y):
                    WALLS[i*room_size+k][j*room_size+room_size_x]=1
                    WALLS[i*room_size+k][j*room_size+room_size-room_size_x]=1
                for k in range(room_size_x,room_size-room_size_x):                
                    WALLS[i*room_size+room_size_y][j*room_size+k]=1
                    WALLS[i*room_size+room_size-room_size_y][j*room_size+k]=1
#     создание путей по оси x
    builder=-1          
    for i in range(number_rooms_H):
        for j in range(number_rooms_W-1):
            if (ROOMS[i][j]==1) and (ROOMS[i][j+1]==1):
                for k in range(room_size):
                    if WALLS[i*room_size+room_size//2][j*room_size+room_size//2+k]==1:
                        builder*=-1
                        WALLS[i*room_size+room_size//2][j*room_size+room_size//2+k]=3
                        WALLS[i*room_size+room_size//2+1][j*room_size+room_size//2+k]=3
                    if builder==1:
                        WALLS[i*room_size+room_size//2-1][j*room_size+room_size//2+k]=1
                        WALLS[i*room_size+room_size//2+2][j*room_size+room_size//2+k]=1
#     создание путей по оси y
    builder=-1          
    for j in range(number_rooms_H):
        for i in range(number_rooms_W-1):
            if (ROOMS[i][j]==1) and (ROOMS[i+1][j]==1):
                for k in range(room_size):
                    if WALLS[i*room_size+room_size//2+k][j*room_size+room_size//2]==1:
                        builder*=-1
                        WALLS[i*room_size+room_size//2+k][j*room_size+room_size//2]=3
                        WALLS[i*room_size+room_size//2+k][j*room_size+room_size//2+1]=3
                    if builder==1:
                        WALLS[i*room_size+room_size//2+k][j*room_size+room_size//2-1]=1
                        WALLS[i*room_size+room_size//2+k][j*room_size+room_size//2+2]=1
    for i in range(number_walls_H):    
        for j in range(number_walls_W):
            if WALLS[i][j]==1:
                w=Walls()
                w.x=j*block_size-number_walls_W*block_size//2+WIDTH//2
                w.y=i*block_size-number_walls_H*block_size//2+HEIGHT//2
                w.size=block_size
                physics_WALLS.append(w)
def check_collision():
    '''проверка столкновний объектов и
       вылета за границы игрового поля'''
    for e in ENEMIES[:]:
        for h_b in hero_BULLETS:
            if distance_to(h_b.x,h_b.y,e.x,e.y)<e.radius+h_b.radius:
                
                if h_b.type == "shock":
                      e.hp -= 100
                if h_b.type =="uzi":
                    e.hp -= 20
                if h_b.type == "snipe":
                    e.hp -= 100
                if h_b.type == "gun":
                    e.hp -= 20
                if h_b.type == "ice_sphere":
                    e.hp -= 30
                    e.slow=h_b.ice_slow
                    e.time_end_slow=h_b.time_slow_duration+var.TIME
                if h_b.type == "fire_sphere":
                    sf=fire_floor_surfaces()
                    sf.x=h_b.x
                    sf.y=h_b.y
                    sf.time_for_destroy=var.TIME+sf.time_exist
                    SURFACES.append(sf)
                hero_BULLETS.remove(h_b)

    for e in ENEMIES[:]:
        for sf in SURFACES:
            if distance_to(e.x,e.y,sf.x,sf.y)<sf.radius:
                e.time_end_fire=var.TIME+90
                e.fire_damage=20
               
    for e in ENEMIES[:]:
        if e.hp <= 0:
            ENEMIES.remove(e)
    for h_b in hero_BULLETS[:]: 
        for w in physics_WALLS:
             if check_wall_collision(w.x,w.y,w.size,h_b.x,h_b.y,h_b.radius) == True:
                if h_b.type == "fire_sphere":
                    sf=fire_floor_surfaces()
                    sf.x=h_b.x
                    sf.y=h_b.y
                    sf.time_for_destroy=var.TIME+sf.time_exist
                    SURFACES.append(sf)
                hero_BULLETS.remove(h_b)
                continue
                
                    
    for b in BULLETS:  
        for w in physics_WALLS:
            if check_wall_collision(w.x,w.y,w.size,b.x,b.y,b.radius) == True:
                    BULLETS.remove(b)
    for b in BULLETS:
        if distance_to(b.x,b.y,hero.x,hero.y)<b.radius+hero.radius:
            BULLETS.remove(b)
        if inter_arena(b.x,b.y)==False:
            if b in BULLETS:
                BULLETS.remove(b) 
    for h_b in hero_BULLETS:
        if inter_arena(h_b.x,h_b.y)==False:
            hero_BULLETS.remove(h_b)  
        
def draw():
    '''отрисовка всех объектов. '''
    for sf in SURFACES:
        sf.draw()
    for b in BULLETS:
        b.draw()

    for e in ENEMIES:
        e.draw()
    hero.draw()
    for h_b in hero_BULLETS:
        h_b.draw()
    for w in physics_WALLS:
        w.draw()
    aim.draw()
def step():
    '''функция совершающая действия каждый тик. 
    (так же вызывает остальные ежемоментные функции )'''
    spawner() 
    for sf in SURFACES[:]:
        if var.TIME>sf.time_for_destroy:
            SURFACES.remove(sf)

    for e in ENEMIES:
            e.action()
    for b in BULLETS:
        b.move()
    for h_b in hero_BULLETS:
        h_b.move()
    check_collision()
    draw()
    


create_LABIRINT()

pygame.mouse.set_visible(False)
# тест
var.TIME=0
clock = pygame.time.Clock()
finished = False
pygame.init()

while not finished:
    clock.tick(FPS)
    var.TIME+=1
    
     #  движение :
    if hero.shooting==1:
        hero_weapon.SHOOT()
    keys = pygame.key.get_pressed()
    hero.proect_Vx=0
    hero.proect_Vy=0
    if keys[pygame.K_a]:
            hero.proect_Vx-=1
    if keys[pygame.K_d]:
            hero.proect_Vx+=1
    if keys[pygame.K_s]:
            hero.proect_Vy+=1
    if keys[pygame.K_w]:
            hero.proect_Vy-=1
    hero. calculate_speed()
    if hero.proect_Vx**2+hero.proect_Vy**2!=0:
        for w in physics_WALLS:
            if check_wall_collision_x(w.x,w.y,w.size,hero.x,hero.y,hero.radius,hero.Vx)==True:
                hero.proect_Vx=0
            if check_wall_collision_y(w.x,w.y,w.size,hero.x,hero.y,hero.radius,hero.Vy)==True:
                hero.proect_Vy=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


            
            
#       стрельба:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                    hero.shooting=1

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                     hero.shooting=0
        if event.type == pygame.MOUSEMOTION:
            var.mouse_proect_x=cos(hero.x,hero.y,event.pos[0]+my_map.x,event.pos[1]+my_map.y) #var.mouse_proect_x - cos угла между мышкой и героем
            var.mouse_proect_y=sin(hero.x,hero.y,event.pos[0]+my_map.x,event.pos[1]+my_map.y)  #var.mouse_proect_y-sin угла между мышкой и героем  
            aim.x, aim.y = event.pos[0], event.pos[1]  #кооринаты прицела
            
            #переключение оружия:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                hero_weapon.weapon_type="uzi"
                
            if event.key == pygame.K_2:
                hero_weapon.weapon_type="snipe"
                
            if event.key == pygame.K_3:
                hero_weapon.weapon_type="shock"
                
            if event.key == pygame.K_4:
                hero_weapon.weapon_type="gun"
            if event.key == pygame.K_5:
                hero_weapon.weapon_type="ice_sphere"
            if event.key == pygame.K_6:
                hero_weapon.weapon_type="fire_sphere"

                
            if event.key == pygame.K_SPACE:
                if var.TIME>hero.blink_cd+hero.last_use_blink:
                    hero.x=aim.mx+my_map.x
                    hero.y=aim.my+my_map.y
                    hero.last_use_blink=var.TIME

                

    hero.move()      
    my_map.change_coords()
    step()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()