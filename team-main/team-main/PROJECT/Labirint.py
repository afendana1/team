from random import randint

from math_functions import*
from Constants import *
import var
import Hero
class Rooms:
    def __init__(self):
        self.x=0
        self.y=0
        self.x_size=0
        self.y_size=0
        self.can_spawn=1

class Portal:
    def __init__(self):

        self.x=number_walls_W*block_size//2
        self.y=number_walls_H*block_size//2
        self.radius=75
    def draw(self):
        circle(screen, (BLUE), (round(self.x-Hero.my_map.x), round(self.y-Hero.my_map.y)), self.radius)
    def teleport(self):
        s=0
        for r in var.Rooms_parametrs:
            s+= r.can_spawn
        if s==0:
            for i in range(number_rooms_H):
                for j in range(number_rooms_W):
                    ROOMS[j][i]=0
            for i in range(number_walls_H):
                for j in range(number_walls_W):
                    WALLS[j][i]=0

            var.Rooms_parametrs.clear()
            var.physics_WALLS.clear()       
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
                    var.physics_WALLS.append(w)

class Walls():
    def __init__(self):
        self.x=100
        self.y=100
        self.size=50
        self.can_collision=1
    def draw(self):
        if inter_arena(self.x,self.y)==True:
            rect(screen, (WHITE), (round(self.x-Hero.my_map.x),round(self.y-Hero.my_map.y), self.size, self.size), )
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
                rect(screen, (YELLOW), (round(self.x-Hero.my_map.x),round(self.y-Hero.my_map.y), self.size, self.size), )
    def check(self):
        if var.number_enemies>0:            
            self.can_collision =1
        if var.number_enemies==0:
            self.can_collision=0



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
                r=Rooms()
                r.x_size=(room_size-room_size_x*2)*block_size
                r.y_size=(room_size-room_size_y*2)*block_size
                r.x=(j*room_size+room_size_x)*block_size
                r.y=(i*room_size+room_size_y)*block_size
                r.can_spawn=randint(2,3)
                if (i==2) and (j ==2):
                    r.can_spawn=0
                print(r.x,r.y,r.x_size,r.y_size,r.can_spawn)
                var.Rooms_parametrs.append(r)
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
my_portal=Portal()
my_portal.teleport()
