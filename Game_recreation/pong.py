# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initial position of ball
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240)/50, random.randrange(60, 180)/50]
    
    if direction == True:
        
        ball_vel[1] = - ball_vel[1]
        
    elif direction == False:
        
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = - ball_vel[1]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # random initiation of game
    ball_dir = random.randrange(0, 2)
    
    if ball_dir == 0:
        direction = True
            
    elif ball_dir == 1:
        direction = False
    
    spawn_ball(direction)
    # Initial paddles position
    
    paddle1_pos = (HEIGHT / 2.0 - HALF_PAD_HEIGHT)
    paddle1_vel = 0
    
    paddle2_pos = (HEIGHT / 2.0 - HALF_PAD_HEIGHT)
    paddle2_vel = 0
    
    # Initial score
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #Collision conditionals
    
    if ball_pos[1] <= BALL_RADIUS:
        
        ball_vel[1] = - ball_vel[1]
        
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        
        ball_vel[1] = - ball_vel[1]
        
    elif ball_pos[0] < (PAD_WIDTH + BALL_RADIUS):
        
        if ball_pos[1] <= paddle1_pos + PAD_HEIGHT and ball_pos[1] >= paddle1_pos:
            
            ball_vel[0] = - ball_vel[0] * 1.1
            
        else:
            score2 = int(score2)
            score2 += 1
            spawn_ball(True)
        
    elif ball_pos[0] > (WIDTH - PAD_WIDTH - BALL_RADIUS):
        
        if ball_pos[1] <= paddle2_pos + PAD_HEIGHT and ball_pos[1] >= paddle2_pos:
            
            ball_vel[0] = - ball_vel[0] * 1.1

        else: 
            score1 = int(score1)
            score1 += 1
            spawn_ball(False)
    
    # draw ball
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    if paddle1_pos <= 0:
        
        paddle1_vel = 0
        
    elif (paddle1_pos + PAD_HEIGHT) >= HEIGHT:
        
        paddle1_vel = 0
        
    elif paddle2_pos <= 0:
        
        paddle2_vel = 0
        
    elif (paddle2_pos + PAD_HEIGHT) >= HEIGHT:
        
        paddle2_vel = 0

    
    # draw paddles
    
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos), (HALF_PAD_WIDTH, (paddle1_pos+ PAD_HEIGHT)), PAD_WIDTH, "White")
    canvas.draw_line(((WIDTH - HALF_PAD_WIDTH), paddle2_pos), ((WIDTH - HALF_PAD_WIDTH), (paddle2_pos+ PAD_HEIGHT)), PAD_WIDTH, "White")
    

    # draw scores
    
    score1 = str(score1)
    score2 = str(score2)
    
    
    canvas.draw_text(score1, (200, 100), 40, "White")
    canvas.draw_text(score2, (400, 100), 40, "White")
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    acc = 4
    
    # Key handlers for paddle 1
    
    if key == simplegui.KEY_MAP["w"]:
        
        paddle1_vel -= acc
        
    elif key == simplegui.KEY_MAP["s"]:
        
        paddle1_vel += acc
        
    # Key handler for paddle 2        

    elif key == simplegui.KEY_MAP["up"]:
        
        paddle2_vel -= acc
        
    elif key == simplegui.KEY_MAP["down"]:
        
        paddle2_vel += acc

def keyup(key):
    
    global paddle1_vel, paddle2_vel
    
    # Key handlers for paddle 1
    
    if key == simplegui.KEY_MAP["w"]:
        
        paddle1_vel = 0
        
    elif key == simplegui.KEY_MAP["s"]:
        
        paddle1_vel = 0
    
    # Key handlers for paddle 2
    
    elif key == simplegui.KEY_MAP["up"]:
        
        paddle2_vel = 0
        
    elif key == simplegui.KEY_MAP["down"]:
        
        paddle2_vel = 0
    

# create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Reset", new_game, 150)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
