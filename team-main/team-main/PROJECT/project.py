import Constants
import Enemies
import Hero
import Labirint
import draw_images
import math_functions
import var


class Walls():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.size = 50
        self.can_collision = 1

    def draw(self):
        if math_functions.inter_arena(self.x, self.y) == True:
            Hero.rect(Constants.screen, (Constants.WHITE), (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y), self.size, self.size), )

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
                Hero.rect(Constants.screen, (Constants.YELLOW), (round(self.x - Hero.my_map.x), round(self.y - Hero.my_map.y), self.size, self.size), )

    def check(self):
        if Labirint.var.number_enemies > 0:
            self.can_collision = 1
        if Labirint.var.number_enemies == 0:
            self.can_collision = 0


def spawner(x, y, chance):
    '''спавнер мобов'''
    if Labirint.randint(1, 100) < 40 / ((chance + 4) * 2):
        if math_functions.distance_to(Hero.hero.x, Hero.hero.y, x, y) > Hero.hero.radius + 2 * Constants.block_size:
            e = Enemies.Enemy()
            rnd = Labirint.randint(1, 3)
            if rnd == 1:
                e.type = "soldier"
                e.range_to_move = 350
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


def check_collision():
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

    Labirint.var.number_enemies = 0
    for e in Constants.ENEMIES:
        Labirint.var.number_enemies += 1
    for r in Labirint.var.rooms_parameters:
        if math_functions.check_wall_collision(r.x + Constants.block_size, r.y + Constants.block_size, r.x_size - Constants.block_size, r.y_size - Constants.block_size,
                                               Hero.hero.x, Hero.hero.y, -Hero.hero.radius - 1) == True:
            if Labirint.var.number_enemies == 0:
                if r.can_spawn > 0:
                    for i in range(1, (r.y_size - Constants.block_size) // Constants.block_size):
                        for j in range(1, (r.x_size - Constants.block_size) // Constants.block_size):
                            spawner(j * Constants.block_size + r.x, i * Constants.block_size + r.y, r.can_spawn)
                    r.can_spawn -= 1

    for w in Labirint.var.physics_WALLS:
        if w.can_collision == 1:
            for b in Constants.BULLETS[:]:
                if math_functions.check_wall_collision(w.x, w.y, w.size, w.size, b.x, b.y, b.radius) == True:
                    Constants.BULLETS.remove(b)
    for b in Constants.BULLETS:
        if math_functions.distance_to(b.x, b.y, Hero.hero.x, Hero.hero.y) < b.radius + Hero.hero.radius:
            Constants.BULLETS.remove(b)
        if math_functions.inter_arena(b.x, b.y) == False:
            if b in Constants.BULLETS:
                Constants.BULLETS.remove(b)
    for h_b in Constants.hero_BULLETS:
        if math_functions.inter_arena(h_b.x, h_b.y) == False:
            Constants.hero_BULLETS.remove(h_b)


def draw():
    '''отрисовка всех объектов. '''
    Labirint.my_portal.draw()
    for sf in Constants.SURFACES:
        sf.draw()
    for d in Constants.Deads:
        d.draw()
    for b in Constants.BULLETS:
        b.draw()
    for e in Constants.ENEMIES:
        e.draw()
    Hero.hero.draw()
    for h_b in Constants.hero_BULLETS:
        h_b.draw()
    for d in Labirint.var.physics_WALLS:
        d.check()
    for w in Labirint.var.physics_WALLS:
        w.draw()
    Hero.aim.draw()


def step():
    '''
    функция совершающая действия каждый тик. 
    (так же вызывает остальные ежемоментные функции )
    '''
    # spawner() 
    # for sf in SURFACES[:]:
    #     if var.TIME>sf.time_for_destroy:
    #         SURFACES.remove(sf)

    for e in Constants.ENEMIES:
        e.action()
    for d in Constants.Deads:
        if d.time_for_destroy < var.TIME:
            Constants.Deads.remove(d)

    for b in Constants.BULLETS:
        b.move()
    for h_b in Constants.hero_BULLETS:
        h_b.move()

    check_collision()
    var.number_enemies = 0
    for e in Constants.ENEMIES:
        var.number_enemies += 1
    draw()


draw_images.pygame.mouse.set_visible(False)
# тест
Labirint.var.TIME = 0
clock = draw_images.pygame.time.Clock()
finished = False
draw_images.pygame.init()

while not finished:
    clock.tick(Constants.FPS)
    Labirint.var.TIME += 1

    #  движение :
    if Hero.hero.shooting == 1:
        Hero.hero_weapon.SHOOT()
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
            if event.key == draw_images.pygame.K_1:
                Hero.hero_weapon.weapon_type = "uzi"

            if event.key == draw_images.pygame.K_2:
                Hero.hero_weapon.weapon_type = "snipe"

            if event.key == draw_images.pygame.K_3:
                Hero.hero_weapon.weapon_type = "shock"

            if event.key == draw_images.pygame.K_4:
                Hero.hero_weapon.weapon_type = "gun"
            if event.key == draw_images.pygame.K_5:
                Hero.hero_weapon.weapon_type = "ice_sphere"
            if event.key == draw_images.pygame.K_6:
                Hero.hero_weapon.weapon_type = "fire_sphere"

            if event.key == draw_images.pygame.K_SPACE:
                if Labirint.var.TIME > Hero.hero.blink_cd + Hero.hero.last_use_blink:
                    Hero.hero.x = Hero.aim.mx + Hero.my_map.x
                    Hero.hero.y = Hero.aim.my + Hero.my_map.y
                    Hero.hero.last_use_blink = Labirint.var.TIME
            if event.key == draw_images.pygame.K_e:
                if math_functions.distance_to(Hero.hero.x, Hero.hero.y, Labirint.my_portal.x, Labirint.my_portal.y) < Labirint.my_portal.radius - Hero.hero.radius:
                    Labirint.my_portal.teleport()

    Hero.hero.move()
    Hero.my_map.change_coords()
    step()
    draw_images.pygame.display.update()
    Constants.screen.fill(Constants.BLACK)
draw_images.pygame.quit()
