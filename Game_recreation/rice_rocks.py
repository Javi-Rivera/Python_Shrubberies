# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
high_score = 0
lives = 3
time = 0
started = False

rock_group = set([])
explosion_group = set([])
missile_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 60)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.3)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.3)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.3)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.3)

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(canvas, process_set):
    
    for sprite in process_set:
        sprite.draw(canvas)
        sprite.update()
        
    for sprite in set(process_set):
        if sprite.deletion():
            process_set.remove(sprite)
            return True

#HELPER FUNCTION FOR SPRITE / SHIP COLLISION
def group_collide(group_set, other_object):
    
    for i in set(group_set):
        if i.collide(other_object):
            if lives == 1:
                #EXPLOSION ANIMATION FOR SHIP AT 0 LIVES.
                an_explosion = Sprite(other_object.pos, other_object.vel, other_object.angle, 0, explosion_image, explosion_info, explosion_sound)
                explosion_group.add(an_explosion)
                group_set.remove(i)
                return True
            else:
                group_set.remove(i)
                return True

#HELPER FUNCTION FOR SPRITE COLLISION     
def group_collide2(group_set, other_object):
    
    for i in set(group_set):
        if i.sprite_collide(other_object):
            group_set.remove(i)
            return True

#HELPER FUNCTION FOR SPRITE COLLISION     
def group_group_collide(group_set1, group_set2):
    global score
    
    for i in set(group_set1):
        if group_collide2(group_set2, i):
            group_set1.remove(i)
            score += 20
            
            an_explosion = Sprite(i.pos, i.vel, i.angle, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            
            return True
            
# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    #METHOD FOR SHOOTING MISSILES    
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    #METHOD TO STOP ROCKS FROM SPAWNING ON SHIP
    def spawn_collide(self, other_object):
        
        return dist(self.pos, other_object.pos) <= 2 * other_object.radius + 30
    
    #METHOD FOR COLLIDE BETWEEN ROCKS / SHIP
    def collide(self, other_object):
        
        return dist(self.pos, other_object.pos) <= 2 * other_object.radius
    
    #METHOD FOR COLLIDE BETWEEN ROCKS / MISSILES
    def sprite_collide(self, other_object):
        
        return dist(self.pos, other_object.pos) <= other_object.radius
    
    def draw(self, canvas):
        
        if self.animated:
            current_center = [self.image_size[0]/2 + self.age * self.image_size[0], self.image_size[1]/2]
            canvas.draw_image(self.image, current_center, self.image_size, self.pos, self.image_size) 
            
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
    
    #METHOD FOR REMOVING OLD MISSILES
    def deletion(self):
        if self.age >= self.lifespan:
            return True
                
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        timer2.start()
        constant_shot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
    elif key == simplegui.KEY_MAP['space']:
        timer2.stop()
        
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        

def draw(canvas):
    global time, started, lives, rock_group, missile_group, score, high_score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("High Score: " + str(high_score), [620, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text("Score: " + str(score), [620, 80], 22, "White")

    #CODE TO RESTART GAME
    if group_collide(rock_group, my_ship):
        lives -= 1
        if lives == 0:
            if score > high_score:
                high_score = score
                score = 0
            
            started = False
            soundtrack.rewind()
            rock_group = set([])
            missile_group = set([])
            lives = 3
            
              
    # draw ship and sprites
    my_ship.draw(canvas)
    
    #DRAW HANDLER FOR ROCK + MISSILE GROUP
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    #COLLIDE PHYSICS FOR ROCK + MISSILE GROUPS
    group_group_collide(rock_group, missile_group)

    # update ship and sprites
    my_ship.update()
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())


        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, score
    
    if started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.randint(-score/200, score/200), random.randint(-score/200, score/200)]
        rock_avel = random.random() * .2 - .1
        
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)

        if not a_rock.spawn_collide(my_ship) and len(rock_group) < 12:
            rock_group.add(a_rock)

#TIMER HANDLER FOR MACHINE GUN TURRET
def constant_shot():
    my_ship.shoot()

        
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)

group_collide(rock_group, my_ship)
group_group_collide(rock_group, missile_group)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#TIMER FOR ROCK SPAWN / MACHINE GUN TURRET
timer = simplegui.create_timer(600.0, rock_spawner)
timer2 = simplegui.create_timer(200.0, constant_shot)


# get things rolling
timer.start()
frame.start()
