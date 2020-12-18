# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

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
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris_blend.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([10,10], [20, 20], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(rock_group, canvas):
    
    sprite_group = rock_group
    
    for sprite in sprite_group:

        if sprite.update():
            rock_group.remove(sprite)
        else:
            sprite.draw(canvas)

def group_collide(rock_group, other_object):
    
    collide_rock = rock_group
    collision = False
    for rock in collide_rock:
        
        collide = rock.collide(other_object)
        if collide:

            rock_group.remove(rock)
            collision = True
    return collision

def group_group_collide(rock_group, missile_group):
    
    global score
    
    missile_group_bk = missile_group
    
    for missile in missile_group_bk:
        
        if group_collide(rock_group, missile):
            
            score += 1
            missile_group.remove(missile)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.vel_inc = 0.05
        self.friccion = 0.02
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def thrust(self):
        
        if self.thrust == False:
            
            self.thrust = True

        else: 

            self.thrust = False
        
        
    def draw(self,canvas):

        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):

        # Angle Update
        
        self.angle += self.angle_vel

        # Position Update
        
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1] 
        
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        # Thrust Update
        
        self.forward = angle_to_vector(self.angle)
        
        if self.thrust:

            self.image_center[0] = self.image_size[0] + self.image_size[0] / 2
            ship_thrust_sound.play()
                           
            my_ship.vel[0] += my_ship.forward[0] * self.vel_inc * 2
            my_ship.vel[1] += my_ship.forward[1] * self.vel_inc * 2
                            
        else:
            
            self.image_center[0] = self.image_size[0] / 2
            ship_thrust_sound.rewind()

            # Friction Update
        
            self.vel[0] *= (1 - self.friccion)
            self.vel[1] *= (1 - self.friccion)
            
    def shoot(self):
        
        global missile_group
        
        self.mis_pos = [0, 0]
        
        # Missile Position
        self.mis_pos[0] = self.pos[0] + self.radius * self.forward[0] 
        self.mis_pos[1] = self.pos[1] + self.radius * self.forward[1]
        
        # Missile Velocity
        self.mis_vel = [0, 0]
        
        self.mis_pos[0] += self.mis_vel[0] 
        self.mis_pos[1] += self.mis_vel[1] 
        
        self.mis_vel[0] += self.vel[0] + self.forward[0] * 4
        self.mis_vel[1] += self.vel[1] + self.forward[1] * 4
        a_missile = Sprite(self.mis_pos, self.mis_vel, self.angle, 0, missile_image, missile_info, True, missile_sound) 
        missile_group.add(a_missile)
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, lifespan = None, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.animated = info.get_animated()
        self.age = 0
        if lifespan:
            self.lifespan = info.get_lifespan()
        else:
            self.lifespan = None
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        
        # Position Update
        
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1] 

        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT

        # Rotation Update
        
        self.angle += self.angle_vel
        if self.lifespan != None:
            self.age += 1
            if self.age >= self.lifespan:
                return True
            else:
                return False
        
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= (self.radius + other_object.radius):
            return True
        
        else:
            return False
        
def keydown(key):
    
    if key == simplegui.KEY_MAP["right"]:
       
        my_ship.angle_vel += my_ship.vel_inc
        
    elif key == simplegui.KEY_MAP["left"]:
        
        my_ship.angle_vel -= my_ship.vel_inc
        
    elif key == simplegui.KEY_MAP["up"]:
                
        my_ship.thrust = True
    
    elif key == simplegui.KEY_MAP["space"]:
        
        my_ship.shoot()        
    
def keyup(key):
    
    if key == simplegui.KEY_MAP["right"]:
        
        my_ship.angle_vel = 0
        
    elif key == simplegui.KEY_MAP["left"]:
        
        my_ship.angle_vel = 0
        
    elif key == simplegui.KEY_MAP["up"]:
        
        my_ship.thrust = False

# mouseclick handlers that reset UI and conditions whether splash image is drawn

def click(pos):
    
    global started, soundtrack, lives, score

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()


def draw(canvas):
    
    global time, a_rock, rock_group, lives, started, score, soundtrack
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives", [10, 20], 20, "White")
    canvas.draw_text("%d" %lives, [10, 40], 20, "White")
    canvas.draw_text("Score" %(score), [720, 20], 20, "White")
    canvas.draw_text("%d" %(score), [720, 40], 20, "White")
    # draw ship and sprites
    my_ship.draw(canvas)

    process_sprite_group(rock_group, canvas)
    
    if group_collide(rock_group, my_ship):
        
        lives -= 1

    group_group_collide(rock_group, missile_group)
    
    process_sprite_group(missile_group, canvas)    
    
    # update ship and sprites
    my_ship.update()
    
    # draw splash screen if not started
    if not started:
        
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    if lives == 0:
        
        started = False
        rock_group = set([])
        soundtrack.rewind()
        
# timer handler that spawns a rock    
def rock_spawner():
    
    global a_rock, rock_group, started, my_ship, score

    if started == True:

        position = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        lower = -0.1 
        upper = 0.1 
        rang = upper - lower

        if score == 0:
            velocity = [random.random()* rang + lower, random.random()* rang + lower]
        
        else:
            velocity = [(random.random()* rang + lower) * (score), (random.random()* rang + lower) * (score)]
        
        ang_vel = random.random() * 0.2 - 0.1 
        
        my_ship_x = my_ship.pos[0] + my_ship.radius
        my_ship_negx = my_ship.pos[0] - my_ship.radius
        my_ship_y = my_ship.pos[1] + my_ship.radius
        my_ship_negy = my_ship.pos[1] - my_ship.radius

        if my_ship_negx <= position[0] >= my_ship_x and my_ship_negy <= position[1] >= my_ship_y:
        
            pass
            # collision avoided
        
        else:    
            if len(rock_group) <= 11:
                a_rock = Sprite(position, velocity, 0, ang_vel, asteroid_image, asteroid_info)
                rock_group.add(a_rock)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
missile_group = set([])
rock_group = set([])
#a_missile = Sprite([-1, -1], [0,0], 0, 0, missile_image, missile_info, None)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()