# Key_Wars_V1.py
# Creator - Danila Khomenko
""" V1 - 30/07/2019 - this program presents user with a static window containing the game layout; spawns a single
                                      alien for a specified number of times.
"""
# IMPORTS
import tkinter as tk
import random

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
PROJECTILES = []
# ====================================================FUNCTIONS=========================================================
# Make the spawned alien move towards the earth widget
def move_alien(init_coords, alien_id, speed):
    global x_ea_c, y_ea_c, label
    print("id = ", alien_id)
    # Find the alien's x and y coordinates
    x_pos = init_coords[0]
    y_pos = init_coords[1]
    # find the spawn at which the alien has been created
    for key in ALIEN_SPAWN_LOCS:
        if ALIEN_SPAWN_LOCS[key] == tuple(init_coords):
            spawn = key
    # set the appropriate alien movement based upon its spawn location
    if spawn in ('spawn1', 'spawn2', 'spawn8'):
        while game_canvas.coords(widget_alien) != [x_ea_c,y_ea_c]:
            if  x_pos < x_ea_c :
                game_canvas.move(widget_alien,1.19,0)
                x_pos = (game_canvas.coords(widget_alien))[0]
            if y_pos <  y_ea_c:
                game_canvas.move(widget_alien,0,1)
                y_pos = (game_canvas.coords(widget_alien))[1]
            game_canvas.after(speed)
            game_canvas.update()

    elif spawn in ('spawn3', 'spawn4'):
        while game_canvas.coords(widget_alien) != [x_ea_c,y_ea_c]:
            if  x_pos > x_ea_c :
                game_canvas.move(widget_alien,-1.19,0)
                x_pos = (game_canvas.coords(widget_alien))[0]
            if y_pos <  y_ea_c:
                game_canvas.move(widget_alien,0,1)
                y_pos = (game_canvas.coords(widget_alien))[1]
            game_canvas.after(speed)
            game_canvas.update()

    elif spawn in ('spawn5', 'spawn6'):
        while game_canvas.coords(widget_alien) != [x_ea_c, y_ea_c]:
            if x_pos  > x_ea_c:
                game_canvas.move(widget_alien, -1.15, 0)
                x_pos = (game_canvas.coords(widget_alien))[0]
            if y_pos > y_ea_c:
                game_canvas.move(widget_alien, 0, -1)
                y_pos = (game_canvas.coords(widget_alien))[1]
            game_canvas.after(speed)
            game_canvas.update()

    else:
        while game_canvas.coords(widget_alien) != [x_ea_c, y_ea_c]:
            if x_pos < x_ea_c:
                game_canvas.move(widget_alien, 1.15, 0)
                x_pos = (game_canvas.coords(widget_alien))[0]
            if y_pos > y_ea_c:
                game_canvas.move(widget_alien, 0, -1)
                y_pos = (game_canvas.coords(widget_alien))[1]
            game_canvas.after(speed)
            game_canvas.update()
    game_canvas.delete(alien_id)

# Create and spawn an alien widget in a random location
def  spawnAlien():
    global label
    # Pick a random location from the ALIEN_SPAWN_LOCS dict
    random_pair = random.choice(list(ALIEN_SPAWN_LOCS.items()))
    spawn_coords = (350,0)
   # define image_alien
    image_alien = tk.PhotoImage(file= image_alien_path)
    # Make a reference to image_alien in order to prevent garbage collection
    label = tk.Label(image =  image_alien)
    label.image = image_alien
    label.pack()
    # create the alien widget on canvas
    widget_alien = game_canvas.create_image(spawn_coords[0], spawn_coords[1], image=image_alien, anchor="c")
    return widget_alien

def spawnLaser(event):
    print("Key pressed: ", repr(event.char))
    # define image_laser
    image_laser = tk.PhotoImage(file = image_laser_path)
    # Make a reference to image_laser in order to prevent garbage collection
    label = tk.Label(image = image_laser)
    label.image = image_laser
    label.pack()
    # create widget_laser on canvas
    widget_laser = game_canvas.create_image(x_ea_c, y_ea_c, image = image_laser, anchor = "c", tag = "bullet")
    shootLaser(widget_laser)

def shootLaser(widget_laser):
    widget_laser_loc = game_canvas.coords(widget_laser)
    laser_x = widget_laser_loc[0]
    laser_y = widget_laser_loc[1]
    while laser_y <=  main_window_height:
         game_canvas.move("bullet", 0, 1)
         laser_y = game_canvas.coords(widget_laser)[1]
         game_canvas.after(2)
         game_canvas.update()
    game_canvas.delete(widget_laser)

def  updateScore():
    pass

def  updateEarthLives():
    pass

def updateWave():
    pass
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
for i in range(100):
    widget_alien = spawnAlien()
    move_alien(game_canvas.coords(widget_alien), widget_alien, speed)






# Initialize the main canvas
root.mainloop()


"""
Notes:
- centre of Earth coords =  340, 295



"""