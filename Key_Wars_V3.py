# Key_Wars_V1.py
# Creator - Danila Khomenko
""" V32- 10/07/2019 - this program presents user with a static window containing the game layout; spawns a single
                                      alien for a specified number of times; generates laser beams moving towards the spawn location of current alien.
"""
# IMPORTS
import tkinter as tk
import random
import math

# CONSTANTS
main_window_height = 600
main_window_width = 700
main_window_offset_x = 700
main_window_offset_y = 250
text_score_style = "ROBOTO", "20", "bold"
text_lives_style = "ROBOTO", "22", "bold"
text_wave_style = "ROBOTO", "22", "bold"
x_ea_c = 350
y_ea_c = 295
image_earth_path = "images/static/image_earth.png"
image_space_background_path =  "images/static/image_space_background.png"
image_sun_path =  "images/static/image_sun.png"
image_alien_path = "images/dynamic/aliens/1.png"
image_laser_path = "images/dynamic/image_laser_2.png"

# GLOBAL VARIABLES
user_score = 1111
user_lives = 3
game_wave = 3

# ARRAYS
ALIEN_SPAWN_LOCS = {
"spawn1" : (0,0),
"spawn2" :  (350,0),
"spawn3" :  (700,0),
"spawn4" :  (700,295),
"spawn5" :  (700,600),
"spawn6" :  (350,600),
"spawn7" :  (0,600),
"spawn8"  :  (0,295)
}

ALIEN_CONFIG = {
    "speed" : 2,
    "origin" : (),
    "id" : 0,
    "current_loc" : ()
}
# ====================================================FUNCTIONS=========================================================
# Make the spawned alien move towards the earth widget
def moveAlien():
    global x_ea_c, y_ea_c
    # Find the alien's x and y coordinates
    init_coords = ALIEN_CONFIG["origin"]
    x_pos = init_coords[0]
    y_pos = init_coords[1]
    widget_alien = ALIEN_CONFIG["id"]
    # find the spawn at which the alien has been created
    for key in ALIEN_SPAWN_LOCS:
        if ALIEN_SPAWN_LOCS[key] == tuple(init_coords):
            spawn = key
    # set the appropriate alien movement based upon its spawn location
    if spawn in ('spawn1', 'spawn2', 'spawn8'):
        if  x_pos < x_ea_c :
            game_canvas.move(widget_alien,1.19,0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos <  y_ea_c:
            game_canvas.move(widget_alien,0,1)
            y_pos = (game_canvas.coords(widget_alien))[1]

    elif spawn in ('spawn3', 'spawn4'):
        if  x_pos > x_ea_c :
            game_canvas.move(widget_alien,-1.19,0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos <  y_ea_c:
            game_canvas.move(widget_alien,0,1)
            y_pos = (game_canvas.coords(widget_alien))[1]

    elif spawn in ('spawn5', 'spawn6'):
        if x_pos  > x_ea_c:
            game_canvas.move(widget_alien, -1.15, 0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos > y_ea_c:
            game_canvas.move(widget_alien, 0, -1)
            y_pos = (game_canvas.coords(widget_alien))[1]

    else:
        if x_pos < x_ea_c:
            game_canvas.move(widget_alien, 1.15, 0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos > y_ea_c:
            game_canvas.move(widget_alien, 0, -1)
            y_pos = (game_canvas.coords(widget_alien))[1]

    game_canvas.after(speed)
    game_canvas.update()
    dist = math.sqrt((x_ea_c - x_pos)**2 + (y_ea_c - y_pos)**2) - 123
    if dist < 0.6:
        game_canvas.delete(widget_alien)
        return ("collision")
    ALIEN_CONFIG["current_loc"] = game_canvas.coords(widget_alien)

# Create and spawn an alien widget in a random location
def  spawnAlien():
    global ALIEN_CONFIG
    # Pick a random location from the ALIEN_SPAWN_LOCS dict
    random_pair = random.choice(list(ALIEN_SPAWN_LOCS.items()))
    spawn_coords = random_pair[1]
   # define image_alien
    image_alien = tk.PhotoImage(file= image_alien_path)
    # Make a reference to image_alien in order to prevent garbage collection
    label = tk.Label(image = image_alien)
    label.image = image_alien
    label.pack()
    # create the alien widget on canvas
    widget_alien = game_canvas.create_image(spawn_coords[0], spawn_coords[1], image=image_alien, anchor="c")
    ALIEN_CONFIG["origin"]  =  game_canvas.coords(widget_alien)
    ALIEN_CONFIG["id"] = widget_alien

def spawnLaser(event):
    #print("Key pressed: ", repr(event.char))
    global widget_laser
    image_laser = tk.PhotoImage(file = image_laser_path)
    # Make a reference to image_laser in order to prevent garbage collection
    label = tk.Label(image = image_laser)
    label.image = image_laser
    label.pack()
    # create widget_laser on canvas
    widget_laser = game_canvas.create_image(x_ea_c, y_ea_c, image = image_laser, anchor = "c", tag = "bullet")

def shootLaser():
    alien_spawn = tuple(ALIEN_CONFIG["origin"])
    dif_x = alien_spawn[0] - x_ea_c
    dif_y = alien_spawn[1] - y_ea_c
    for i in ALIEN_SPAWN_LOCS:
        if ALIEN_SPAWN_LOCS[i] == alien_spawn:
            alien_spawn_name = i
    if dif_x == 0:
        if dif_y < 1:
            speed_y = -1
        else:
            speed_y = 1
        speed_x = 0
    elif dif_y == 0:
        if dif_x < 1:
            speed_x = -1
        else:
            speed_x = 1

        speed_y = 0

    else:
        if alien_spawn_name == "spawn7":
            speed_y = abs(dif_y/dif_x)
        else:
            if dif_y < 0:
                speed_y = -abs(dif_y/dif_x)
            else:
                speed_y = dif_y / dif_x
        if dif_x < 0:
            speed_x = -1
        else:
            speed_x = 1

    game_canvas.move("bullet", speed_x, speed_y)
    game_canvas.update()

def  updateScore():
    pass

def  updateEarthLives():
    pass

def updateWave():
    pass

def shoot():
    if 'widget_laser' in globals():
        if widget_laser in game_canvas.find_all():
            shootLaser()

# ======================================================MAIN============================================================
# Main code

# Initialize main window
root = tk.Tk()
root.title("Key_Wars v1")
root.geometry("{}x{}+{}-{}".format(main_window_width, main_window_height, main_window_offset_x, main_window_offset_y))
root.configure(background = "green")

# Create the game canvas
game_canvas = tk.Canvas(root, width = main_window_width, height = main_window_height, bg = "blue")
game_canvas.pack()

# Create game background
image_space_background = tk.PhotoImage(file= image_space_background_path)
game_background = game_canvas.create_image(0, 0, image = image_space_background, anchor = 'c')

# Create earth widget
image_earth = tk.PhotoImage(file= image_earth_path)
widget_earth = game_canvas.create_image(350,300, image = image_earth, anchor = "c")

# Create sun widget
image_sun = tk.PhotoImage(file = image_sun_path)
widget_sun = game_canvas.create_image(0,0,image  =  image_sun, anchor = "nw")

# Create "Score" text widget
widget_score = game_canvas.create_text(610, 25 , text = "{}{}".format("Score: ", user_score), fill = "white",  font = text_score_style)

# Create  "Earth Lives" text widget
widget_lives = game_canvas.create_text(109,575, text = "{}{}".format("Earth Lives: ", user_lives), fill = "white", font = text_lives_style)

# Create "Wave"  text widget
widget_wave = game_canvas.create_text(630,574, text = "{}{}".format("Wave: ",  game_wave), fill = "white", font  = text_wave_style)



# Primitive game flow

speed = 10
spawnAlien()
while True:
    game_canvas.bind("<Key>", spawnLaser)
    game_canvas.focus_set()
    a = moveAlien()
    if a == ("collision"):
        spawnAlien()
    shoot()

# spawnLaser()



# Initialize the main canvas
root.mainloop()


"""
Notes:
- centre of Earth coords =  340, 295



"""