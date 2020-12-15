from random import randint

import pygame.draw

import math_functions
import Constants
import var
import Hero


class Rooms:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_size = 0
        self.y_size = 0
        self.can_spawn = 1


class Portal:
    def __init__(self):

        self.x = Constants.number_walls_W * Constants.block_size // 2
        self.y = Constants.number_walls_H * Constants.block_size // 2
        self.radius = 75

    def draw(self):
        pygame.draw.circle(Constants.screen, Constants.BLUE,
                           (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y)), self.radius)

    def teleport(self):
        s = 0
        for r in var.rooms_parameters:
            s += r.can_spawn
        if s == 0:
            for i in range(Constants.number_rooms_H):
                for j in range(Constants.number_rooms_W):
                    Constants.ROOMS[j][i] = 0
            for i in range(Constants.number_walls_H):
                for j in range(Constants.number_walls_W):
                    Constants.WALLS[j][i] = 0
            
            var.rooms_parameters.clear()
            var.physics_WALLS.clear()
            var.Chests.clear()
            var.Items.clear()
            var.Hard+=3
            create_LABIRINT()
        for i in range(Constants.number_walls_H):
            for j in range(Constants.number_walls_W):
                if Constants.WALLS[i][j] == 1:
                    w = Walls()
                if Constants.WALLS[i][j] == 3:
                    w = Doors()
                if Constants.WALLS[i][j] != 0:
                    w.x = j * Constants.block_size
                    w.y = i * Constants.block_size
                    w.size = Constants.block_size
                    var.physics_WALLS.append(w)


class Walls():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.can_collision = 1

    def draw(self):
        if math_functions.inter_arena(self.x, self.y) == True:
            pygame.draw.rect(Constants.screen, Constants.WHITE,
                             (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y), self.size, self.size), )

    def check(self):
        pass


class Doors():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.can_collision = 1

    def draw(self):
        if math_functions.inter_arena(self.x, self.y) == True:
            if self.can_collision == 1:
                pygame.draw.rect(Constants.screen, Constants.YELLOW,
                                 (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y), self.size, self.size), )

    def check(self):
        if var.number_enemies > 0:
            self.can_collision = 1
        if var.number_enemies == 0:
            self.can_collision = 0
class Droped_weapon():
	def __init__(self):
		self.type="uzi"
		self.x=0
		self.y=0
		self.radius=15
	def draw(self):
		pygame.draw.circle(Constants.screen, Constants.GREEN, (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y)), self.radius)
	def take_weapon(self):
		item = Droped_weapon()
		item.x = self.x
		item.y = self.y+self.radius*1.5
		item.type=Hero.hero_select_weapon.weapon_type
		var.Items.append(item)		
		Hero.hero_select_weapon.weapon_type=self.type


class Chest():
	def __init__(self):
		self.size=50
		self.x=0
		self.y=0
		self.can_drop=True
	def draw(self):
		pygame.draw.rect(Constants.screen, Constants.YELLOW,(round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y), self.size, self.size), )
	def drop_item(self):
		if self.can_drop:
			item = Droped_weapon()
			item.x = self.x+self.size//2
			item.y = self.y+(self.size+item.radius)*1.5
			rnd = randint(1,6)
			if rnd==1:
			   item.type= "uzi"

			if rnd==2:
			   item.type = "snipe"

			if rnd==3:
			    item.type = "shock"

			if rnd==4:
			    item.type = "gun"
			if rnd==5:
			    item.type = "ice_sphere"
			if rnd==6:
			    item.type = "fire_sphere"
			var.Items.append(item)
			self.can_drop = False


def labirint_constr(i, j, steps):
    if steps > 0:
        if Constants.ROOMS[i][j] != 1:
            steps -= 1
            Constants.ROOMS[i][j] = 1
        rnd = randint(1, 4)

        if rnd == 1:
            if i < Constants.number_rooms_H - 1:
                labirint_constr(i + 1, j, steps)
            else:
                labirint_constr(i, j, steps)

        if rnd == 2:
            if i > 0:
                labirint_constr(i - 1, j, steps)
            else:
                labirint_constr(i, j, steps)
        if rnd == 3:
            if j < Constants.number_rooms_W - 1:
                labirint_constr(i, j + 1, steps)
            else:
                labirint_constr(i, j, steps)
        if rnd == 4:
            if j > 0:
                labirint_constr(i, j - 1, steps)
            else:
                labirint_constr(i, j, steps)


def create_LABIRINT():
    # генерация комнат
    labirint_constr(2, 2, 7)

    # создание стен комнат
    for i in range(Constants.number_rooms_H):
        for j in range(Constants.number_rooms_W):
            if Constants.ROOMS[i][j] == 1:
                room_size_x = randint(1, 3)
                room_size_y = randint(1, 3)
                r = Rooms()
                r.x_size = (Constants.room_size - room_size_x * 2) * Constants.block_size
                r.y_size = (Constants.room_size - room_size_y * 2) * Constants.block_size
                r.x = (j * Constants.room_size + room_size_x) * Constants.block_size
                r.y = (i * Constants.room_size + room_size_y) * Constants.block_size
                r.can_spawn = randint(2, 3)
                if (i == 2) and (j == 2):
                    r.can_spawn = 0
                print(r.x, r.y, r.x_size, r.y_size, r.can_spawn)
                var.rooms_parameters.append(r)
                for k in range(room_size_y, Constants.room_size - room_size_y):
                    Constants.WALLS[i * Constants.room_size + k][j * Constants.room_size + room_size_x] = 1
                    Constants.WALLS[i * Constants.room_size + k][
                        j * Constants.room_size + Constants.room_size - room_size_x] = 1
                for k in range(room_size_x, Constants.room_size - room_size_x):
                    Constants.WALLS[i * Constants.room_size + room_size_y][j * Constants.room_size + k] = 1
                    Constants.WALLS[i * Constants.room_size + Constants.room_size - room_size_y][
                        j * Constants.room_size + k] = 1
    #     создание путей по оси x
    builder = -1
    for i in range(Constants.number_rooms_H):
        for j in range(Constants.number_rooms_W - 1):
            if (Constants.ROOMS[i][j] == 1) and (Constants.ROOMS[i][j + 1] == 1):
                for k in range(Constants.room_size):
                    if Constants.WALLS[i * Constants.room_size + Constants.room_size // 2][
                            j * Constants.room_size + Constants.room_size // 2 + k] == 1:
                        builder *= -1
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2][
                            j * Constants.room_size + Constants.room_size // 2 + k] = 3
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + 1][
                            j * Constants.room_size + Constants.room_size // 2 + k] = 3
                    if builder == 1:
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 - 1][
                            j * Constants.room_size + Constants.room_size // 2 + k] = 1
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + 2][
                            j * Constants.room_size + Constants.room_size // 2 + k] = 1
    #     создание путей по оси y
    builder = -1
    for j in range(Constants.number_rooms_H):
        for i in range(Constants.number_rooms_W - 1):
            if (Constants.ROOMS[i][j] == 1) and (Constants.ROOMS[i + 1][j] == 1):
                for k in range(Constants.room_size):
                    if Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + k][
                            j * Constants.room_size + Constants.room_size // 2] == 1:
                        builder *= -1
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + k][
                            j * Constants.room_size + Constants.room_size // 2] = 3
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + k][
                            j * Constants.room_size + Constants.room_size // 2 + 1] = 3
                    if builder == 1:
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + k][
                            j * Constants.room_size + Constants.room_size // 2 - 1] = 1
                        Constants.WALLS[i * Constants.room_size + Constants.room_size // 2 + k][
                            j * Constants.room_size + Constants.room_size // 2 + 2] = 1

    for j in range(Constants.number_rooms_H):
        for i in range(Constants.number_rooms_W ):
        	if (i!=2) and (j!=2):
        		if Constants.ROOMS[j][i]==1:
        			if randint(1,2) == 1:
        				c = Chest()
        				c.y = j*Constants.block_size*Constants.room_size+Constants.block_size*Constants.room_size//2
        				c.x = i*Constants.block_size*Constants.room_size+Constants.block_size*Constants.room_size//2
        				var.Chests.append(c)
        				print(i,j)



my_portal = Portal()
my_portal.teleport()