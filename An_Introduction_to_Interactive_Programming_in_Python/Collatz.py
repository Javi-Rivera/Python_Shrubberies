import simplegui

n = 217

def collatz():
    
    global n
    
    if (n % 2) == 0:
        n = n/2
        
    else:
        n = (n*3) + 1

def tick():
    
    global n
    
    print n
    
    if  n > 1:
        
        collatz()
        
    else:
        
        timer.stop()
    
    
    
timer = simplegui.create_timer(1000, tick)
timer.start()