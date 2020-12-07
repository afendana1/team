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
from Labirint import *

class Walls():
    def __init__(self):
        self.x=100
        self.y=100
        self.size=50
        self.can_collision=1
    def draw(self):
        if inter_arena(self.x,self.y)==True:
            rect(screen, (WHITE), (round(self.x-my_map.x),round(self.y-my_map.y), self.size, self.size), )
    def check(self):
    	pass

class Doors():
    def __init__(self):
        self.x=100
        self.y=100
        self.size=50
        self.can_collision=1
    def draw(self):
        if inter_arena(self.x,self.y)==True:
        	if self.can_collision==1:
        		rect(screen, (YELLOW), (round(self.x-my_map.x),round(self.y-my_map.y), self.size, self.size), )
    def check(self):
    	if var.number_enemies>0:    		
    		self.can_collision =1
    	if var.number_enemies==0:
    		self.can_collision=0



def spawner(x,y,chance):
    '''спавнер мобов'''
    if randint(1,100)<40/(chance+6):
    	if distance_to(hero.x,hero.y,x,y)>hero.radius+2*block_size:
	        e=Enemy()      
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
	        e.x=x
	        e.y=y
	        ENEMIES.append(e)


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
                e.time_end_fire=var.TIME+sf.tick_time
                e.fire_damage=sf.damage
               
    for e in ENEMIES[:]:
        if e.hp <= 0:
            ENEMIES.remove(e)
     
    for w in physics_WALLS:
    	for h_b in hero_BULLETS[:]:
             if check_wall_collision(w.x,w.y,w.size,w.size,h_b.x,h_b.y,h_b.radius) == True:
                if h_b.type == "fire_sphere":
                    sf=fire_floor_surfaces()
                    sf.x=h_b.x
                    sf.y=h_b.y
                    sf.time_for_destroy=var.TIME+sf.time_exist
                    SURFACES.append(sf)
                hero_BULLETS.remove(h_b)
                continue
    for r in var.Rooms_parametrs:
    	if check_wall_collision(r.x+block_size,r.y+block_size,r.x_size-block_size,r.y_size-block_size,hero.x,hero.y,-2*hero.radius) == True:
    		if var.number_enemies==0:
	    		if r.can_spawn >0:
		    		for i in range(1,(r.y_size-block_size)//block_size):
		    			for j in range(1,(r.x_size-block_size)//block_size):
		    				spawner(j*block_size+r.x,i*block_size+r.y,r.can_spawn)
		    		r.can_spawn-=1

                
                    
    
    for w in physics_WALLS:
    	for b in BULLETS[:]:  
            if check_wall_collision(w.x,w.y,w.size,w.size,b.x,b.y,b.radius) == True:
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
    for d in physics_WALLS:
    	d.check()
    for w in physics_WALLS:
        w.draw()

    aim.draw()
def step():
    '''функция совершающая действия каждый тик. 
    (так же вызывает остальные ежемоментные функции )'''
    # spawner() 
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
    var.number_enemies=0
    for e in ENEMIES:
    	var.number_enemies+=1    	
    draw()

    	

    


create_LABIRINT()
for i in range(number_walls_H):    
    for j in range(number_walls_W):
        if WALLS[i][j]==1:
            w=Walls()
        if WALLS[i][j]==3:
            w=Doors()
        if WALLS[i][j]!=0:   
            w.x=j*block_size
            w.y=i*block_size
            w.size=block_size
            physics_WALLS.append(w)
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
        	if w.can_collision==1:
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