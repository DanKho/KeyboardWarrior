# Key_Wars_V1.py
# Creator - Danila Khomenko
""" V3 - 20/07/2019 - this program presents user with a static window containing the game layout; spawns aliens randomly; allows user to shoot at the alien;
scoreboard is now functional; aliens come with pre-set words above them.; generates laser beams moving towards the spawn location of current alien; each alien carries a random word on top of it;
laser shooting is now synchronized with typing.
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
user_score = 0
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
    "speed" : 0.2,
    "origin" : (),
    "id" : 0,
    "lives" : 0
}

AMMO = []
WORDLIST = ["Hello", "My name is Danila"]
# ====================================================FUNCTIONS=========================================================
# Create and spawn an alien widget in a random location
def  spawnAlien():
    global  widget_alien
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
    widget_alien = game_canvas.create_image(spawn_coords[0], spawn_coords[1], image=image_alien, anchor="c", tag = "alien")
    ALIEN_CONFIG["origin"]  =  game_canvas.coords(widget_alien)
    ALIEN_CONFIG["id"] = widget_alien

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
    alien_speed = ALIEN_CONFIG["speed"]
    # set the appropriate alien movement based upon its spawn location
    if spawn in ('spawn1', 'spawn2', 'spawn8'):
        if  x_pos < x_ea_c :
            game_canvas.move("alien",1.19* alien_speed,0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos <  y_ea_c:
            game_canvas.move("alien",0,1*alien_speed)
            y_pos = (game_canvas.coords(widget_alien))[1]

    elif spawn in ('spawn3', 'spawn4'):
        if  x_pos > x_ea_c :
            game_canvas.move("alien",-1.19*alien_speed,0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos <  y_ea_c:
            game_canvas.move("alien",0,1*alien_speed)
            y_pos = (game_canvas.coords(widget_alien))[1]

    elif spawn in ('spawn5', 'spawn6'):
        if x_pos  > x_ea_c:
            game_canvas.move("alien", -1.15*alien_speed, 0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos > y_ea_c:
            game_canvas.move("alien", 0, -1*alien_speed)
            y_pos = (game_canvas.coords(widget_alien))[1]

    else:
        if x_pos < x_ea_c:
            game_canvas.move("alien", 1.15*alien_speed, 0)
            x_pos = (game_canvas.coords(widget_alien))[0]
        if y_pos > y_ea_c:
            game_canvas.move("alien", 0, -1*alien_speed)
            y_pos = (game_canvas.coords(widget_alien))[1]

    game_canvas.after(speed)
    game_canvas.update()
    dist = math.sqrt((x_ea_c - x_pos)**2 + (y_ea_c - y_pos)**2) - 123
    if dist < 0.6:
        game_canvas.delete("bullet")
        game_canvas.delete("alien")
        AMMO = []
        return ("collision")

def spawnLaser():
    global widget_laser
    image_laser = tk.PhotoImage(file = image_laser_path)
    # Make a reference to image_laser in order to prevent garbage collection
    label = tk.Label(image = image_laser)
    label.image = image_laser
    label.pack()
    # create widget_laser on canvas
    widget_laser = game_canvas.create_image(x_ea_c, y_ea_c, image = image_laser, anchor = "c", tag = "bullet")
    AMMO.append(widget_laser)

def moveLaser():
    laser_speed = 9
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

    game_canvas.move("bullet", speed_x * laser_speed, speed_y * laser_speed)
    game_canvas.update()

def shootLaser():
    if 'widget_alien' in globals():
        if widget_alien in game_canvas.find_all():
            if len(AMMO) > 0:
                moveLaser()
                alienHit()

def  updateScore():
    game_canvas.delete("scoreboard")
    widget_score = game_canvas.create_text(610, 25, text="{}{}".format("Score: ", user_score), fill="white", font=text_score_style, tag="scoreboard")

def alienHit():
    global AMMO
    global  user_score
    alien_coords = game_canvas.coords(widget_alien)
    target_x = alien_coords[0]
    target_y = alien_coords[1]
    laser_coords = game_canvas.coords(AMMO[0])
    laser_x = laser_coords[0]
    laser_y = laser_coords[1]
    dist = math.sqrt((laser_x - target_x)**2 + (laser_y - target_y)**2) - 15
    if dist < 0:
        ALIEN_CONFIG["lives"] -= 1
        game_canvas.delete(AMMO[0])
        AMMO.remove((AMMO[0]))

    if ALIEN_CONFIG["lives"] == 0:
        AMMO = []
        game_canvas.delete(widget_laser)
        game_canvas.delete("alien")
        game_canvas.delete("bullet")
        user_score += 5
        ALIEN_CONFIG["speed"] += 0.1
        generateWord()
        updateScore()
        spawnAlien()
        textBox()

def checkSpelling(event):
    global current_word
    key = event.char
    if len(correct_letters) > 0:
        if key == correct_letters[0]:
            spawnLaser()
            correct_letters.remove(key)
            current_word = (current_word[1: len(current_word)])
            game_canvas.delete(word)
            textBox()

def generateWord():
    global current_word
    global correct_letters
    correct_letters = []
    current_word = random.choice(WORDLIST)
    for i in current_word:
        correct_letters.append(i)
    ALIEN_CONFIG["lives"] = len(correct_letters)

def textBox():
    global word
    alien_coords = game_canvas.coords(widget_alien)
    alien_x = alien_coords[0]
    alien_y = alien_coords[1]
    word = game_canvas.create_text(alien_x, alien_y-30, text = current_word, fill = "white",  font = text_score_style, anchor = "s", tag = "alien")

def updateEarthLives():
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
widget_score = game_canvas.create_text(610, 25 , text = "{}{}".format("Score: ", user_score), fill = "white",  font = text_score_style, tag = "scoreboard")

# Create  "Earth Lives" text widget
widget_lives = game_canvas.create_text(109,575, text = "{}{}".format("Earth Lives: ", user_lives), fill = "white", font = text_lives_style)

# Create "Wave"  text widget
widget_wave = game_canvas.create_text(630,574, text = "{}{}".format("Wave: ",  game_wave), fill = "white", font  = text_wave_style)


# Primary game flow
speed = 5
spawnAlien()
generateWord()
textBox()
while True:
    a = moveAlien()
    if a == ("collision"):
        AMMO = []
        spawnAlien()
        generateWord()
        textBox()
    game_canvas.bind("<Key>", checkSpelling)
    game_canvas.focus_set()
    shootLaser()





# Initialize the main canvas
root.mainloop()


"""
Notes:
- centre of Earth coords =  340, 295



"""