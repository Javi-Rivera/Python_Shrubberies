# template for "Stopwatch: The Game"

import simplegui

# define global variables

t = 0 
x = 0
y = 0 
timer_running = False # counter variable to prevent multiple 
                    # stop counts at the same stop.

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    
    minutes = t // 600 # Calculate A.
    
    seconds = (t/10) % 60
    
    seconds_b = seconds // 10 # Calculate B
    seconds_c = seconds % 10 # Calculate C
        
    milliseconds = t % 10 # Calculate D
    
    return("%d:%d%d.%d" %(minutes, seconds_b, seconds_c, milliseconds))

    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    
    # Start the timer
    
    global timer_running
    
    timer.start()
    
    timer_running = True
    
def stop():
    
    # Stop the timer    
    global x, y, timer_running
    
    timer.stop()
    
    # Points and global tries counters
    if timer_running == True:
        
        y += 1

        if (t % 10 == 0):

            x += 1

    timer_running = False

    return(x, y)
        
def reset():
    
    # Resets the timer and the counters of the game    
    global t, x, y
    
    t = 0
    x = 0
    y = 0
    
    timer.stop()


# define event handler for timer with 0.1 sec interval

def interval():
    
    # Function that increments the counter when the timer starts.
    global t
    
    t += 1
    
    print t
    
    

# define draw handler

def draw(canvas):
    
    global t, x, y
    
    counter = "%d/%d" %(x, y)
    
    canvas.draw_text(format(t), [60, 100], 40, "white")
    canvas.draw_text(counter, [140, 30], 20, "Yellow")    
    
# create frame

frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, interval)

# register event handlers

frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Reset", reset, 150)

# start frame

frame.start()

# Please remember to review the grading rubric
