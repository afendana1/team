from random import randint

from Constants import *
import var
class Rooms:
    def __init__(self):
        self.x=0
        self.y=0
        self.x_size=0
        self.y_size=0
        self.can_spawn=1


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