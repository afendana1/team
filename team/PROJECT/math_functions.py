import Hero
from Constants import *
def distance_to(x1,y1,x2,y2):
    '''функция для опредения растояния'''
    return(((x1-x2)**2+(y1-y2)**2)**0.5)
def cos(x1,y1,x2,y2):
    return((x2-x1)/distance_to(x1,y1,x2,y2))
def sin(x1,y1,x2,y2):
    return((y2-y1)/distance_to(x1,y1,x2,y2))
def check_wall_collision(w_x,w_y,w_sz_x,w_sz_y,x,y,r):
    if (x+r>w_x) and (x-r<w_x+w_sz_x) and (y-r<w_y+w_sz_y) and (y+r>w_y):
        return True
def check_wall_collision_x(w_x,w_y,w_sz,x,y,r,v):
    if (x+r<w_x+w_sz//2) and (x+v+r>=w_x) and (y<=w_y+w_sz+r) and (y>=w_y-r):
        return True
    if (x-r>w_x+w_sz//2) and (x+v-r<=w_x+w_sz) and (y<=w_y+w_sz+r) and (y>=w_y-r):
        return True
def check_wall_collision_y(w_x,w_y,w_sz,x,y,r,v):
    if (x>=w_x-r) and (x<=w_x+w_sz+r) and (y+v+r>=w_y) and (y+r<w_y+w_sz//2):
        return True
    if (x>=w_x-r) and (x<=w_x+w_sz+r) and (y+v-r<=w_y+w_sz) and (y-r>w_y+w_sz//2):
        return True

def inter_arena(x,y):
    '''проверка нахождения внутри арены 
       True - внутри; False - снаружи'''
    inter_a=True
    if distance_to(x,y,Hero.hero.x,Hero.hero.y)>((WIDTH//2)**2+(HEIGHT//2)**2)**0.5*1.5:
        inter_a=False        
    return(inter_a)