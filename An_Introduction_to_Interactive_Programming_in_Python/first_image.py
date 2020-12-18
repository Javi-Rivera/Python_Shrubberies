import simplegui
# Global Variables
WIDTH = 800
HEIGHT = 600
in_pos = [WIDTH / 2, HEIGHT / 2]
vel = [1, 1]
# define Functions:
# import image
image = simplegui.load_image("https://i.imgur.com/GvqZIGE.jpg")
image_width = image.get_width()
image_height = image.get_height()
ast_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid.png")
ast_width = 95
ast_height = 93
ast_certer = [ast_width / 2, ast_height / 2]
ast_size = [ast_width, ast_height]

# Draw image

def draw(canvas):
    
    global in_pos
    
    canvas.draw_image(image, [image_width / 2, image_height / 2], [image_width, image_height], 
                     (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    in_pos[0] += vel[0]
    in_pos[1] += vel[1]
    
    if in_pos[0] >= WIDTH:
        vel[0] = - vel[0]
    elif in_pos[0] <= 0:
        vel[0] = - vel[0]
    elif in_pos[1] >= HEIGHT:
        vel[1] = - vel[1]
    elif in_pos[1] <= 0:
        vel[1] = - vel[1]
    
    canvas.draw_image(ast_image, (ast_certer), (ast_size), (in_pos), (ast_size))
# Create Frame
frame = simplegui.create_frame("First Image", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.start()