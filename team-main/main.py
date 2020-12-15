import Constants
import Enemies
import Hero
import Labirint
import draw_images
import math_functions
import var


def spawner(x, y, chance):
    '''спавнер мобов'''
    if Labirint.randint(1, 100) < 40 / ((chance + 4) * 4)*(var.Hard)/10:
        if math_functions.distance_to(Hero.hero.x, Hero.hero.y, x, y) > Hero.hero.radius + 2 * Constants.block_size:
            e = Enemies.Enemy()
            rnd = Labirint.randint(1, 3)
            if rnd == 1:
                e.type = "soldier"
                e.range_to_move = 3250
                e.range_to_attack = 250
                e.color = Constants.MAGENTA
            if rnd == 2:
                e.type = "zombie"
                e.range_to_move = Hero.hero.radius * 1.2
                e.range_to_attack = Hero.hero.radius * 1.3
                e.color = Constants.GREEN
            if rnd == 3:
                e.type = "mage"
                e.range_to_move = 400
                e.range_to_attack = 300
                e.color = Constants.BLUE
            e.now_action = "move"
            e.x = x
            e.y = y
            Constants.ENEMIES.append(e)


def check_damage():
    '''
    проверка столкновний объектов и
    вылета за границы игрового поля
    '''
    for e in Constants.ENEMIES[:]:
        for h_b in Constants.hero_BULLETS:
            if math_functions.distance_to(h_b.x, h_b.y, e.x, e.y) < e.radius + h_b.radius:
                if h_b.type == "shock":
                    e.hp -= 100
                if h_b.type == "uzi":
                    e.hp -= 20
                if h_b.type == "snipe":
                    e.hp -= 100
                if h_b.type == "gun":
                    e.hp -= 20
                if h_b.type == "ice_sphere":
                    e.hp -= 30
                    e.slow = h_b.ice_slow
                    e.time_end_slow = h_b.time_slow_duration + Labirint.var.TIME
                if h_b.type == "fire_sphere":
                    sf = Hero.fire_floor_surfaces()
                    sf.x = h_b.x
                    sf.y = h_b.y
                    sf.time_for_destroy = Labirint.var.TIME + sf.time_exist
                    Constants.SURFACES.append(sf)
                Constants.hero_BULLETS.remove(h_b)

    for e in Constants.ENEMIES[:]:
        for sf in Constants.SURFACES:
            if max(e.x - sf.x, e.y - sf.y) < sf.radius:
                e.time_end_fire = Labirint.var.TIME + sf.tick_time
                e.fire_damage = sf.damage

    for e in Constants.ENEMIES[:]:
        if e.hp <= 0:
            d = Enemies.Dead()
            d.x = e.x
            d.y = e.y
            d.type = e.type
            d.time_for_destroy = Labirint.var.TIME + d.time_exist
            Constants.Deads.append(d)
            Constants.ENEMIES.remove(e)

    for w in Labirint.var.physics_WALLS:
        if w.can_collision == 1:
            for h_b in Constants.hero_BULLETS[:]:
                if math_functions.check_wall_collision(w.x, w.y, w.size, w.size, h_b.x, h_b.y, h_b.radius) == True:
                    if h_b.type == "fire_sphere":
                        sf = Hero.fire_floor_surfaces()
                        sf.x = h_b.x
                        sf.y = h_b.y
                        sf.time_for_destroy = Labirint.var.TIME + sf.time_exist
                        Constants.SURFACES.append(sf)
                    Constants.hero_BULLETS.remove(h_b)
                    continue
def check_collision():
    Labirint.var.number_enemies = 0
    for e in Constants.ENEMIES:
        Labirint.var.number_enemies += 1
    for r in Labirint.var.rooms_parameters:
        if math_functions.check_wall_collision(r.x + Constants.block_size, r.y + Constants.block_size, r.x_size - Constants.block_size, r.y_size - Constants.block_size,
                                               Hero.hero.x, Hero.hero.y, -Hero.hero.radius - 1) == True:
            if Labirint.var.number_enemies == 0:
                if r.can_spawn > 0:
                    for i in range(2, (r.y_size - Constants.block_size) // Constants.block_size):
                        for j in range(2, (r.x_size - Constants.block_size) // Constants.block_size):
                            spawner(j * Constants.block_size + r.x, i * Constants.block_size + r.y, r.can_spawn)
                    r.can_spawn -= 1

    for w in Labirint.var.physics_WALLS:
        if w.can_collision == 1:
            for b in Constants.BULLETS[:]:
                if math_functions.check_wall_collision(w.x, w.y, w.size, w.size, b.x, b.y, b.radius) == True:
                    Constants.BULLETS.remove(b)
    for b in Constants.BULLETS[:]:
        if math_functions.distance_to(b.x, b.y, Hero.hero.x, Hero.hero.y) < b.radius + Hero.hero.radius:
            Hero.hero.hp-=20
            Constants.BULLETS.remove(b)
            if Hero.hero.hp<=0:
                end_game()
            
        if math_functions.inter_arena(b.x, b.y) == False:
            if b in Constants.BULLETS:
                Constants.BULLETS.remove(b)



def draw():
    '''отрисовка всех объектов. '''
    Labirint.my_portal.draw()
    for sf in Constants.SURFACES:
        sf.draw()
    for d in Constants.Deads:
        d.draw()
    for b in Constants.BULLETS:
        b.draw()
    for c in var.Chests:
    	c.draw()
    for e in Constants.ENEMIES:
        e.draw()
    for item in var.Items:
    	item.draw()
    	
    Hero.hero.draw()
    for h_b in Constants.hero_BULLETS:
        h_b.draw()
    for d in Labirint.var.physics_WALLS:
        d.check()
    for w in Labirint.var.physics_WALLS:
        w.draw()
    Hero.aim.draw()
    Hero.healthbar.draw()


def step():
    '''
    функция совершающая действия каждый тик. 
    (так же вызывает остальные ежемоментные функции )
    '''
    
    for sf in Constants.SURFACES[:]:
        if var.TIME>sf.time_for_destroy:
            Constants.SURFACES.remove(sf)

    for e in Constants.ENEMIES:
        e.action()
    for d in Constants.Deads:
        if d.time_for_destroy < var.TIME:
            Constants.Deads.remove(d)

    for b in Constants.BULLETS:
        b.move()
    for h_b in Constants.hero_BULLETS:
        h_b.move()
    check_damage()   
    check_collision()
    var.number_enemies = 0
    for e in Constants.ENEMIES:
        var.number_enemies += 1
    draw()

def start_game():
	var.game_room="game"
	Hero.healthbar.color=Constants.GREEN
	Hero.hero.hp=100
	Hero.hero.x = Constants.number_walls_W * Constants.block_size // 2
	Hero.hero.y = Constants.number_walls_H * Constants.block_size // 2
	Labirint.my_portal.teleport()

def end_game():
	var.game_room="menu"
	draw_images.pygame.mouse.set_visible(True)
	Constants.ENEMIES.clear()
	Constants.BULLETS.clear()
	Constants.hero_BULLETS.clear()
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
	var.Hard=10

clock = draw_images.pygame.time.Clock()
finished = False
draw_images.pygame.init()

while not finished:
    clock.tick(Constants.FPS)
    Labirint.var.TIME += 1
    if var.game_room=="menu":
        Hero.play_button.draw()

    if var.game_room=="game":
	    #  движение :
	    if Hero.hero.shooting == 1:
	        Hero.hero_select_weapon.SHOOT()
	    keys = draw_images.pygame.key.get_pressed()
	    Hero.hero.proect_Vx = 0
	    Hero.hero.proect_Vy = 0
	    if keys[draw_images.pygame.K_a]:
	        Hero.hero.proect_Vx -= 1
	    if keys[draw_images.pygame.K_d]:
	        Hero.hero.proect_Vx += 1
	    if keys[draw_images.pygame.K_s]:
	        Hero.hero.proect_Vy += 1
	    if keys[draw_images.pygame.K_w]:
	        Hero.hero.proect_Vy -= 1
	    Hero.hero.calculate_speed()
	    if Hero.hero.proect_Vx ** 2 + Hero.hero.proect_Vy ** 2 != 0:
	        for w in Labirint.var.physics_WALLS:
	            if w.can_collision == 1:
	                if math_functions.check_wall_collision_x(w.x, w.y, w.size, Hero.hero.x, Hero.hero.y, Hero.hero.radius, Hero.hero.Vx) == True:
	                    Hero.hero.proect_Vx = 0
	                if math_functions.check_wall_collision_y(w.x, w.y, w.size, Hero.hero.x, Hero.hero.y, Hero.hero.radius, Hero.hero.Vy) == True:
	                    Hero.hero.proect_Vy = 0
    for event in draw_images.pygame.event.get():
        if event.type == draw_images.pygame.QUIT:
            finished = True
        if var.game_room=="menu":
            if event.type == draw_images.pygame.MOUSEBUTTONDOWN:
	            if event.button == 1:
	                if math_functions.check_wall_collision(Hero.play_button.x,Hero.play_button.y,Hero.play_button.x_size,Hero.play_button.y_size, event.pos[0],event.pos[1],3):
	                    draw_images.pygame.mouse.set_visible(False)
	                    start_game()

        if var.game_room=="game":

	        #       стрельба:
	        if event.type == draw_images.pygame.MOUSEBUTTONDOWN:
	            if event.button == 1:
	                Hero.hero.shooting = 1

	        if event.type == draw_images.pygame.MOUSEBUTTONUP:
	            if event.button == 1:
	                Hero.hero.shooting = 0
	        if event.type == draw_images.pygame.MOUSEMOTION:
	            var.mouse_projection_x = math_functions.cos(Hero.hero.x, Hero.hero.y, event.pos[0] + Hero.my_map.x,
	                                                             event.pos[1] + Hero.my_map.y)  # var.mouse_proect_x - cos угла между мышкой и героем
	            var.mouse_projection_y = math_functions.sin(Hero.hero.x, Hero.hero.y, event.pos[0] + Hero.my_map.x,
	                                                             event.pos[1] + Hero.my_map.y)  # var.mouse_proect_y-sin угла между мышкой и героем
	            Hero.aim.x, Hero.aim.y = event.pos[0], event.pos[1]  # кооринаты прицела

	            # переключение оружия:
        if event.type == draw_images.pygame.KEYDOWN:
            if event.key == draw_images.pygame.K_BACKSPACE:
        	    draw_images.pygame.quit()

            if var.game_room=="game":
	            if event.key == draw_images.pygame.K_1:
	            	if  Hero.hero_weapon2 == Hero.hero_select_weapon:
		                Hero.hero_weapon2 = Hero.hero_select_weapon
		                Hero.hero_select_weapon = Hero.hero_weapon1

	            if event.key == draw_images.pygame.K_2:
	            	if  Hero.hero_weapon1 == Hero.hero_select_weapon:
		                Hero.hero_weapon1 = Hero.hero_select_weapon
		                Hero.hero_select_weapon = Hero.hero_weapon2

	            if event.key == draw_images.pygame.K_SPACE:
	                if Labirint.var.TIME > Hero.hero.blink_cd + Hero.hero.last_use_blink:
	                    Hero.hero.x = Hero.aim.mx + Hero.my_map.x
	                    Hero.hero.y = Hero.aim.my + Hero.my_map.y
	                    Hero.hero.last_use_blink = Labirint.var.TIME
	            if event.key == draw_images.pygame.K_ESCAPE:    
        	        if var.game_room=="game":
        	            end_game()       
	            if event.key == draw_images.pygame.K_e:
	                if math_functions.distance_to(Hero.hero.x, Hero.hero.y, Labirint.my_portal.x, Labirint.my_portal.y) < Labirint.my_portal.radius - Hero.hero.radius:
	                    Labirint.my_portal.teleport()
	                else:
	                	for c in var.Chests:
	                		if math_functions.distance_to(Hero.hero.x,Hero.hero.y,c.x+c.size//2,c.y+c.size//2)<Hero.hero.radius*2:
	                			c.drop_item()
	                	for item in var.Items[:]:
	                		if math_functions.distance_to(Hero.hero.x,Hero.hero.y,item.x,item.y)<Hero.hero.radius*2: 
	                			item.take_weapon()
	                			var.Items.remove(item)



    if var.game_room=="game": 

	    Hero.hero.move()
	    Hero.my_map.change_coords()
	    step()
    draw_images.pygame.display.update()
    Constants.screen.fill(Constants.BLACK)
draw_images.pygame.quit()
