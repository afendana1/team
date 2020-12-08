import pygame
from pygame.draw import *
from random import randint
import numpy as np
import matplotlib as mp

loose=0
distance_to_mouse=0
zzz=0
WIDTH=1500
HEIGHT=1000
BULLETS=[]
hero_BULLETS=[]
physics_WALLS=[]
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
room_size=20
block_size=50
number_rooms_H=5
number_rooms_W=5
number_walls_H=number_rooms_H*room_size+1
number_walls_W=number_rooms_W*room_size+1
ROOMS=[]
WALLS=[]

for i in range(number_rooms_H):
        ROOMS.append([0]*number_rooms_W)
for i in range(number_walls_H):
        WALLS.append([0]*number_walls_H)

screen = pygame.display.set_mode(( WIDTH, HEIGHT))
class Map:
    def __init__(self):
        self.x=0
        self.y=0
    def change_coords(self):
        self.x=hero.x-WIDTH//2
        self.y=hero.y-HEIGHT//2
class Hero:
    'игрок'
    def __init__(self):
        self.hp=100
        self.x=WIDTH//2
        self.y=HEIGHT//2
        self.radius=25
        self.proect_Vx=0
        self.proect_Vy=0
        self.Vx=0
        self.Vy=0
        self.V=10
        self.right_arm_x=self.radius #рука откуда ведеться стрельба
        self.shooting = 0 #стреляет ли сейчас наш герой
        
        #способности героя:
        self.blink_cd=60
        self.last_use_blink=0

    def draw(self):
        circle(screen, (YELLOW), (round(self.x-my_map.x), round(self.y-my_map.y)), self.radius)
    def move(self):
        if self.proect_Vx**2 + self.proect_Vy**2 > 0:
            self.Vx=self.V*self.proect_Vx/(self.proect_Vx**2 + self.proect_Vy**2)**0.5
            self.Vy=self.V*self.proect_Vy/(self.proect_Vx**2 + self.proect_Vy**2)**0.5
            self.x+=self.Vx
            self.y+=self.Vy
    def calculate_speed(self):
         if self.proect_Vx**2 + self.proect_Vy**2 > 0:
            self.Vx=self.V*self.proect_Vx/(self.proect_Vx**2 + self.proect_Vy**2)**0.5
            self.Vy=self.V*self.proect_Vy/(self.proect_Vx**2 + self.proect_Vy**2)**0.5

                
                
class hero_Weapon:
    '''оружие героя'''
    def __init__(self):
        self.scatter=0
        self.shoot_side=1
        self.weapon_type="uzi"
        
        self.time_last_shoot_uzi=0
        self.time_next_shoot_uzi=1
        
        self.time_last_shoot_snipe=0
        self.time_next_shoot_snipe=45
        
        self.time_last_shoot_shock=0
        self.time_next_shoot_shock=5
        
        self.time_last_shoot_gun=0
        self.time_next_shoot_gun=5

    def SHOOT(self):
        '''стрельба героя'''
        if self.weapon_type == "uzi":
            if TIME>self.time_last_shoot_uzi+self.time_next_shoot_uzi:
                b=hero_Bullet()
                b.x=hero.x + hero.right_arm_x*self.shoot_side
                b.y=hero.y
                self.scatter=np.pi*randint(-10,10)/180 #вычисление угла разброса
                b.Vx=b.V*np.cos((np.arccos(mouse_proect_x)+self.scatter)) #разброс
                b.Vy=b.V*np.sin((np.arcsin(mouse_proect_y)+self.scatter)) #разброс
                hero_BULLETS.append(b)
                self.shoot_side=self.shoot_side*(-1) #нужно когда стрельба идет с двкх рук(например узи)
                self.time_last_shoot_uzi=TIME
                b.type="uzi"
        if self.weapon_type == "snipe":
            if TIME>self.time_last_shoot_snipe+self.time_next_shoot_snipe:
                b=hero_Bullet()
                b.x=hero.x + hero.right_arm_x
                b.y=hero.y
                b.radius=5
                b.type="snipe"
                b.Vx=b.V_snipe*mouse_proect_x
                b.Vy=b.V_snipe*mouse_proect_y
                hero_BULLETS.append(b)
                self.time_last_shoot_snipe=TIME
        if self.weapon_type == "shock":
            if TIME>self.time_last_shoot_shock+self.time_next_shoot_shock:
                for i in range(40):
                    b=hero_Bullet()
                    b.x=hero.x
                    b.y=hero.y
                    b.radius=4
                    b.type="shock"
                    b.Vx=30 * np.cos(2*np.pi*i/40)
                    b.Vy=30 * np.sin(2*np.pi*i/40)
                    hero_BULLETS.append(b)
                self.time_last_shoot_shock=TIME
        if self.weapon_type == "gun":
            if TIME>self.time_last_shoot_gun+self.time_next_shoot_gun:
                b=hero_Bullet()
                b.x=hero.x + hero.right_arm_x
                b.y=hero.y
                b.radius=3
                b.type="gun"
                b.Vx=b.V_snipe*mouse_proect_x
                b.Vy=b.V_snipe*mouse_proect_y
                hero_BULLETS.append(b)
                self.time_last_shoot_gun=TIME

    
class hero_Bullet:
    def __init__(self):
        self.x=0
        self.y=0
        self.Vx=0
        self.Vy=0
        self.V=20
        self.V_snipe=50
        self.radius=2
        self.type="uzi"
    def move(self):
        self.x+=self.Vx
        self.y+=self.Vy 
    def draw(self):
        circle(screen, (CYAN), (int(round(self.x-my_map.x)), int(round(self.y-my_map.y))),self.radius)
        
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
    def draw(self):    
        circle(screen, (self.color), (round(self.x-my_map.x), round(self.y-my_map.y)),round(self.radius))
        
          

        
    def SHOOT(self):
        '''стрельба врагов
            b.type=="melee" означает что атака ближнего боя
            пуля подобной атаки не рисуется, но нужна для проверки коллизии '''
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
        '''призыв одного моба другим'''
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
        
class Aim:
    '''прицел
     пока нормально не работает '''
    def __init__(self):
        self.x=0
        self.y=0
        self.size=4
        self.range=300
    def draw(self):

#         if distance_to(hero.x,hero.y,self.x,self.y)<self.range:
            
            rect(screen, (WHITE), (round(self.x-self.size//2),round(self.y-self.size//2), self.size, self.size), )
            self.mx=self.x
            self.my=self.y
#         else:         
#             rect(screen, (WHITE), (round(hero.x+self.range*mouse_proect_x),round(hero.y+self.range*mouse_proect_y), self.size, self.size), )
#             self.mx, self.my=round(hero.x+self.range*mouse_proect_x), round(hero.y+self.range*mouse_proect_y)
            
        
class Walls():
    def __init__(self):
        self.x=100
        self.y=100
        self.size=50
    def draw(self):
        rect(screen, (WHITE), (round(self.x-my_map.x),round(self.y-my_map.y), self.size, self.size), )
    
        
def distance_to(x1,y1,x2,y2):
    '''функция для опредения растояния'''
    return(((x1-x2)**2+(y1-y2)**2)**0.5)
def cos(x1,y1,x2,y2):
    return((x2-x1)/distance_to(x1,y1,x2,y2))
def sin(x1,y1,x2,y2):
    return((y2-y1)/distance_to(x1,y1,x2,y2))
def inter_arena(x,y):
    '''проверка нахождения внутри арены 
       True - внутри; False - снаружи'''
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
                hero_BULLETS.remove(h_b)
                if h_b.type == "shock":
                      e.hp -= 100
                if h_b.type =="uzi":
                    e.hp -= 20
                if h_b.type == "snipe":
                    e.hp -= 100
                if h_b.type == "gun":
                    e.hp -= 10
    for e in ENEMIES[:]:
        if e.hp <= 0:
            ENEMIES.remove(e)
    for h_b in hero_BULLETS: 
        for w in physics_WALLS:
             if check_wall_collision(w.x,w.y,w.size,h_b.x,h_b.y,h_b.radius) == True:
                hero_BULLETS.remove(h_b)
                    
    for b in BULLETS:  
        for w in physics_WALLS:
            if check_wall_collision(w.x,w.y,w.size,b.x,b.y,b.radius) == True:
                    BULLETS.remove(b)
    for b in BULLETS:
        if distance_to(b.x,b.y,hero.x,hero.y)<b.radius+hero.radius:
            BULLETS.remove(b)
#         if inter_arena(b.x,b.y)==False:
#             if b in BULLETS:
#                 BULLETS.remove(b) 
#     for h_b in hero_BULLETS:
#         if inter_arena(h_b.x,h_b.y)==False:
#             hero_BULLETS.remove(h_b)  
        
def draw():
    '''отрисовка всех объектов. '''
    
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
    for e in ENEMIES:
            e.action()
    for b in BULLETS:
        b.move()
    for h_b in hero_BULLETS:
        h_b.move()
    check_collision()
    draw()
    
def check_wall_collision(w_x,w_y,w_sz,x,y,r):
    if (x>w_x) and (x<w_x+w_sz) and (y<w_y+w_sz) and (y>w_y):
        return True
def check_wall_collision_x(w_x,w_y,w_sz,x,y,r,v):
    if (x+r<w_x+w_sz//2)and (x+v+r>=w_x) and (y<=w_y+w_sz+r) and (y>=w_y-r):
        return True
    if (x-r>w_x+w_sz//2)and (x+v-r<=w_x+w_sz) and (y<=w_y+w_sz+r) and (y>=w_y-r):
        return True
def check_wall_collision_y(w_x,w_y,w_sz,x,y,r,v):
    if (x>=w_x-r) and (x<=w_x+w_sz+r) and (y+v+r>=w_y) and (y+r<w_y+w_sz//2):
        return True
    if (x>=w_x-r) and (x<=w_x+w_sz+r) and (y+v-r<=w_y+w_sz) and (y-r>w_y+w_sz//2):
        return True
create_LABIRINT()
my_map=Map()
hero=Hero()
hero_weapon=hero_Weapon()
aim=Aim()
w=Walls()
physics_WALLS.append(w)
pygame.mouse.set_visible(False)
# тест
TIME=0
clock = pygame.time.Clock()
finished = False
pygame.init()

while not finished:
    clock.tick(FPS)
    TIME+=1
    
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
            mouse_proect_x=cos(hero.x,hero.y,event.pos[0]+my_map.x,event.pos[1]+my_map.y) #mouse_proect_x - cos угла между мышкой и героем
            mouse_proect_y=sin(hero.x,hero.y,event.pos[0]+my_map.x,event.pos[1]+my_map.y)  #mouse_proect_y-sin угла между мышкой и героем  
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
                
            if event.key == pygame.K_SPACE:
                if TIME>hero.blink_cd+hero.last_use_blink:
                    hero.x=aim.mx+my_map.x
                    hero.y=aim.my+my_map.y
                    hero.last_use_blink=TIME

                

    hero.move()      
    my_map.change_coords()
    step()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
