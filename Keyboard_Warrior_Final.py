# Key_Wars_V1.py
# Creator - Danila Khomenko
""" V5 - 07/08/2019 - this program presents user with a static window containing the game layout; spawns aliens randomly; allows user to shoot at the alien;
scoreboard is now functional; aliens have random words above them; menu is now present and fully functional ; user data is stored in separate .txt files
"""
# IMPORTS
import tkinter as tk
import random
import math
import time

# ARRAYS
ALIEN_SPAWN_LOCS = {
"spawn1" : (0,0),
"spawn3" :  (700,0),
"spawn4" :  (700,295),
"spawn5" :  (700,600),
"spawn6" :  (350,600),
"spawn7" :  (0,600),
"spawn8"  :  (0,295)
}

worldlist_easy_path = "wordlist_easy.txt"
worldlist_medium_path = "wordlist_medium.txt"
worldlist_hard_path = "wordlist_hard.txt"
current_wordlist = worldlist_easy_path
# ====================================================FUNCTIONS=========================================================
def initializeGlobals():
    global main_window_height, main_window_width, main_window_offset_x, main_window_offset_y, text_score_style, text_lives_style, \
        text_wave_style, x_ea_c, y_ea_c, image_earth_path, image_space_background, image_space_background_path, image_sun_path, \
        image_alien_path, image_laser_path, user_score, user_lives, game_wave, letters_total, letters_correct, time_start, time_end, \
        total_words, speed, AMMO, ALIEN_CONFIG, image_turret_path, image_heart_path

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
    image_space_background_path = "image/static/image_space_background.png"
    image_turret_path = "images/static/image_turret.png"
    image_sun_path = "images/static/image_sun.png"
    image_laser_path = "images/dynamic/image_laser_2.png"
    image_heart_path = "images/static/image_heart.png"
    user_score = 0
    user_lives = 3
    game_wave = 1
    letters_total = 0
    letters_correct = 0
    time_start = 0
    time_end = 0
    total_words = 0
    speed = 0
    data = {}
    AMMO = []
    ALIEN_CONFIG = {
        "speed": 0.2,
        "origin": (),
        "id": 0,
        "lives": 0}

def mainMenu():
    global menu_space_background
    game_canvas.delete("all")
    # Create space  background
    menu_game_background = game_canvas.create_image(0, 0, image=image_space_background, anchor='c')
    widget_menu_sun = game_canvas.create_image(0,0,image  =  image_sun, anchor = "nw")
    widget_menu_box = game_canvas.create_rectangle(200, 138, 500, 387, fill = "black")
    widget_title_box = game_canvas.create_rectangle(220, 158, 480, 208, fill = "blue")
    widget_name = game_canvas.create_text(350, 185, text = "Keyboard warrior", fill = "yellow", font = ("ARIAL", "20", "bold"))


    button_start = tk.Button(game_canvas, text="New Game", anchor='c', font=("ROBOTO", 13, "bold"))
    button_start.configure(width=20, background="white",  overrelief="groove", command = restartGame)
    button_window = game_canvas.create_window(350, 248, window=button_start)

    button_stats = tk.Button(game_canvas, text="My stats", anchor='c', font=("ROBOTO", 13, "bold"))
    button_stats.configure(width=20, background="white",overrelief="groove", command = statsMenu)
    button_window = game_canvas.create_window(350, 298, window=button_stats)

    button_options = tk.Button(game_canvas, text="Settings", anchor='c', font=("ROBOTO", 13, "bold"))
    button_options.configure(width=20, background="white", overrelief="groove", command = settingsMenu)
    button_window = game_canvas.create_window(350, 348, window=button_options)

def statsMenu():
    global menu_space_background, data
    game_canvas.delete("all")
    with open("user_data.txt") as f:
        data ={}
        for line in f:
            (key, val) = line.split()
            data[key] = val
    max_score = data["score"]
    max_wave = data["wave"]
    max_accuracy = data["accuracy"]
    max_wpm = data["wpm"]
    menu_game_background = game_canvas.create_image(0, 0, image=image_space_background, anchor='c')
    widget_menu_sun = game_canvas.create_image(0,0,image  =  image_sun, anchor = "nw")
    widget_final_box = game_canvas.create_rectangle(160, 160, 540, 450, fill = "black")
    widget_final_score = game_canvas .create_text(350, 200 , text = "{}{}".format("Max score: ", max_score), fill = "#33D7FF",  font = text_score_style)
    widget_final_wave = game_canvas.create_text(350, 250, text="{}{}".format("Max wave reached: ", max_wave), fill="#33D7FF", font=text_wave_style)
    widget_final_accuracy = game_canvas.create_text(350, 300, text="{}{}{}".format("Accuracy: " , max_accuracy, "%"), fill="#33D7FF", font=text_wave_style)
    widget_final_wpm = game_canvas.create_text(350, 350, text="{}{}".format("Max WPM: " , max_wpm), fill="#33D7FF", font=text_wave_style)

    button_menu = tk.Button(game_canvas, text="Back to menu!", anchor='c', font = ("ROBOTO", 15, "bold"), command = mainMenu)
    button_menu.configure(width=20,background="white")
    button_window = game_canvas.create_window(350, 410, window = button_menu)

def statsUpdate(score, wave, accuracy, wpm):
    with open("user_data.txt") as f:
        data ={}
        for line in f:
            (key, val) = line.split()
            data[key] = val
        previous_score = int(data["score"])
        if previous_score < score:
            data["score"] = score
        previous_wave = int(data["wave"])
        if previous_wave < wave:
            data["wave"] = wave
        previous_accuracy = int(data["accuracy"])
        if previous_accuracy < accuracy:
            data["accuracy"] = accuracy
        previous_wpm = int(data["wpm"])
        if previous_wpm < wpm:
            data["wpm"] = wpm
    with open("user_data.txt", "w") as f:
        f.write("score {}".format(data["score"]))
        f.write("\n")
        f.write("wave {}".format(data["wave"]))
        f.write("\n")
        f.write("accuracy {}".format(data["accuracy"]))
        f.write("\n")
        f.write("wpm {}".format(data["wpm"]))
        f.close()

def settingsMenu():
    global menu_space_background
    game_canvas.delete("all")
    menu_game_background = game_canvas.create_image(0, 0, image=image_space_background, anchor='c')
    widget_menu_sun = game_canvas.create_image(0,0,image  =  image_sun, anchor = "nw")
    widget_final_box = game_canvas.create_rectangle(230, 130, 500, 350, fill="black")
    widget_game_over = game_canvas.create_text(350, 180, text="Level of difficulty", fill="white", font=  ("ROBOTO", "20", "bold underline"))

    button_continue = tk.Button(game_canvas, text="easy", anchor='c', font=("ROBOTO", 12, "bold"),command= lambda: setDifficulty("easy"))
    button_continue.configure(width=20, background="green")
    button_window = game_canvas.create_window(350, 240, window=button_continue)

    button_continue = tk.Button(game_canvas, text="medium", anchor='c', font=("ROBOTO", 12, "bold"),command= lambda: setDifficulty("medium"))
    button_continue.configure(width=20, background="orange")
    button_window = game_canvas.create_window(350, 280, window=button_continue)

    button_continue = tk.Button(game_canvas, text="hard", anchor='c', font=("ROBOTO", 12, "bold"), command= lambda: setDifficulty("hard"))
    button_continue.configure(width=20, background="red")
    button_window = game_canvas.create_window(350, 320, window=button_continue)

def setDifficulty(difficulty):
    global current_wordlist
    if difficulty == "easy":
        current_wordlst = worldlist_easy_path
    elif difficulty == "medium":
        current_wordlist = worldlist_medium_path
    elif difficulty == "hard":
        current_wordlist = worldlist_hard_path
    mainMenu()

def createGameLayout():
    global game_canvas, widget_sun, widget_score, widget_lives, widget_wave, root,  \
            image_earth, widget_earth, image_sun, image_space_background, image_turret, x_ea_c, y_ea_c, widget_life_1, widget_life_2, widget_life_3
    # Create game background
    game_background = game_canvas.create_image(0, 0, image = image_space_background, anchor = 'c')

    # Create earth widget
    widget_earth = game_canvas.create_image(350,300, image = image_earth, anchor = "c")

    # Create turret widget
    widget_turret = game_canvas.create_image(x_ea_c, y_ea_c, image = image_turret, anchor = "c")

    # Create sun widget
    widget_sun = game_canvas.create_image(0,0,image  =  image_sun, anchor = "nw")

    # Create "Score" text widget
    widget_score = game_canvas.create_text(610, 25 , text = "{}{}".format("Score: ", user_score), fill = "white",  font = text_score_style, tag = "scoreboard")

    # Create  "Earth Lives" text widget
    widget_lives = game_canvas.create_text(100,575, text = "{}".format("Earth Lives: "), fill = "white", font = text_lives_style, tag = "lives")

    # Create "Wave"  text widget
    widget_wave = game_canvas.create_text(630,574, text = "{}{}".format("Wave: ",  game_wave), fill = "white", font  = text_wave_style, tag = "wave")

    widget_life_1 = game_canvas.create_image((game_canvas.coords(widget_lives)[0])+110, game_canvas.coords(widget_lives)[1], image = image_heart, anchor = "c", tag = "life1")

    widget_life_2 = game_canvas.create_image((game_canvas.coords(widget_lives)[0])+155, game_canvas.coords(widget_lives)[1], image = image_heart, anchor = "c", tag = "life2")

    widget_life_3 = game_canvas.create_image((game_canvas.coords(widget_lives)[0])+200, game_canvas.coords(widget_lives)[1], image = image_heart, anchor = "c", tag = "life3")

    # Create word container widget
    widget_word_container = game_canvas.create_rectangle(200, 5, 500, 40, fill = "blue", tag = "container")

# Create and spawn an alien widget in a random location
def  spawnAlien():
    global  widget_alien
    global ALIEN_CONFIG, time_start
    # Pick a random location from the ALIEN_SPAWN_LOCS dict
    random_pair = random.choice(list(ALIEN_SPAWN_LOCS.items()))
    spawn_coords = random_pair[1]
    image_alien_path = "images/dynamic/aliens/{}.png".format(random.randint(1, 4))
   # define image_alien
    image_alien = tk.PhotoImage(file= image_alien_path)
    # Make a reference to image_alien in order to prevent garbage collection
    label = tk.Label(image = image_alien)
    label.image = image_alien
    label.pack()
    # create the alien widget on canvas
    widget_alien = game_canvas.create_image(spawn_coords[0], spawn_coords[1], image=image_alien, anchor="c", tag = "alien")
    ALIEN_CONFIG["origin"] = game_canvas.coords(widget_alien)
    ALIEN_CONFIG["id"] = widget_alien
    time_start += 1

# Make the spawned alien move towards the earth widget
def moveAlien():
    global x_ea_c, y_ea_c, user_lives
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
    if spawn in ('spawn1', 'spawn8'):
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

    game_canvas.after(10)
    game_canvas.update()
    dist = math.sqrt((x_ea_c - x_pos)**2 + (y_ea_c - y_pos)**2) - 123
    if dist < 0.6:
        game_canvas.delete("container_text")
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

def alienHit():
    global AMMO, user_score, total_words
    alien_coords = game_canvas.coords(widget_alien)
    target_x = alien_coords[0]
    target_y = alien_coords[1]
    laser_coords = game_canvas.coords(AMMO[0])
    laser_x = laser_coords[0]
    laser_y = laser_coords[1]
    dist = math.sqrt((laser_x - target_x)**2 + (laser_y - target_y)**2) - 15
    if dist < 0:
        updateWave()
        ALIEN_CONFIG["lives"] -= 1
        game_canvas.delete(AMMO[0])
        AMMO.remove((AMMO[0]))

    if ALIEN_CONFIG["lives"] == 0:
        AMMO = []
        game_canvas.delete("container_text")
        game_canvas.delete(widget_laser)
        game_canvas.delete("alien")
        game_canvas.delete("bullet")
        user_score += 5
        total_words += 1
        ALIEN_CONFIG["speed"] += 0.05
        generateWord()
        updateScore()
        spawnAlien()
        textBox()

def checkSpelling(event):
    global current_word, letters_correct, letters_total
    key = event.char
    if len(correct_letters) > 0:
        if key == correct_letters[0]:
            letters_correct += 1
            spawnLaser()
            correct_letters.remove(key)
            current_word = (current_word[1: len(current_word)])
            game_canvas.delete(word)
            textBox()
    letters_total += 1

def generateWord():
    global current_word, correct_letters
    correct_letters = []
    words = open("{}".format(current_wordlist)).read()
    current_word = random.choice(words.split("\n"))
    wordContainerUpdate()
    for i in current_word:
        correct_letters.append(i)
    ALIEN_CONFIG["lives"] = len(correct_letters)

def textBox():
    global word
    alien_coords = game_canvas.coords(widget_alien)
    alien_x = alien_coords[0]
    alien_y = alien_coords[1]
    word = game_canvas.create_text(alien_x, alien_y-40, text = current_word, fill = "white",  font = ("ROBOTO", "18", "bold"), anchor = "s", tag = "alien")


def updateEarthLives():
    if user_lives < 3:
        game_canvas.delete("life{}".format(user_lives+1))


def wordContainerUpdate():
    global current_word
    display_word = game_canvas.create_text(351, 21, text = current_word, fill="yellow",font=("ROBOTO", "14"), tag = "container_text")


def updateWave():
    global game_wave
    alien_speed = ALIEN_CONFIG["speed"]
    if alien_speed >= 0.4:
        game_wave = 2
    if alien_speed >= 0.8:
        game_wave = 3
    if alien_speed >= 1.2:
        game_wave = 4
    if alien_speed >= 1.6:
        game_wave = 5
    game_canvas.delete("wave")
    widget_wave = game_canvas.create_text(630, 574, text="{}{}".format("Wave: ", game_wave), fill="white",font=text_wave_style, tag="wave")

def updateScore():
    game_canvas.delete("scoreboard")
    widget_score = game_canvas.create_text(610, 25, text="{}{}".format("Score: ", user_score), fill="white", font=text_score_style, tag="scoreboard")


def gameOver():
    game_canvas.delete("container_text")
    game_canvas.delete("container")
    time_end = time.time()
    time_total = round(time_end - time_start)
    game_canvas.delete("alien", "bullet", widget_earth, widget_sun, "scoreboard", "lives",  "wave")
    widget_final_box = game_canvas.create_rectangle(200, 100, 500, 500, fill = "black")
    widget_game_over = game_canvas.create_text(350, 150, text = "Game Over!", fill = "red", font = text_score_style)
    widget_final_score = game_canvas .create_text(350, 200 , text = "{}{}".format("Final score: ", user_score), fill = "white",  font = text_score_style)
    widget_final_wave = game_canvas.create_text(350, 250, text="{}{}".format("Wave reached: ", game_wave), fill="white", font=text_wave_style)
    try:
        accuracy_score = round((letters_correct / letters_total) *100)
    except ZeroDivisionError:
        accuracy_score = 0
    widget_final_accuracy = game_canvas.create_text(350, 300, text="{}{}{}".format("Accuracy: " , accuracy_score, "%"), fill="white", font=text_wave_style)
    try:
        wpm = round(total_words / (time_total/60))
    except ZeroDivisionError:
        wpm = 0
    widget_final_wpm = game_canvas.create_text(350, 350, text="{}{}".format("WPM: " , wpm), fill="white", font=text_wave_style)

    button = tk.Button(game_canvas, text="Try again!", anchor='c', font = ("ROBOTO", 15, "bold"), command = restartGame)
    button.configure(width=20,background="white")
    button_window = game_canvas.create_window(350, 410, window = button)

    button = tk.Button(game_canvas, text="Menu", anchor='c', font = ("ROBOTO", 15, "bold"), command = mainMenu)
    button.configure(width=20,background="white")
    button_window = game_canvas.create_window(350, 460, window = button)

    statsUpdate(user_score, game_wave, accuracy_score, wpm)

def restartGame():
    global game_canvas
    game_canvas.delete("all")
    initializeGlobals()
    start_game()
# ======================================================MAIN============================================================
# Main code
    # Initialize main window
initializeGlobals()
root = tk.Tk()
root.title("Keyboard_Warrior")
root.geometry("{}x{}+{}-{}".format(main_window_width, main_window_height, main_window_offset_x, main_window_offset_y))
root.configure(background = "green")

# Create the game canvas
game_canvas = tk.Canvas(root, width=main_window_width, height=main_window_height, bg="blue")
game_canvas.pack()

image_space_background = tk.PhotoImage(file=image_space_background_path)
image_earth = tk.PhotoImage(file=image_earth_path)
image_sun = tk.PhotoImage(file=image_sun_path)
image_turret = tk.PhotoImage(file =  image_turret_path)
image_heart = tk.PhotoImage(file = image_heart_path)


# Primary game flow
def main():
    global time_start, user_lives, AMMO
    spawnAlien()
    generateWord()
    textBox()
    game_canvas.bind("<Key>", checkSpelling)
    game_canvas.focus_set()
    time_start = time.time()
    while user_lives > 0 :
        shootLaser()
        a = moveAlien()
        if a == ("collision"):
            user_lives -= 1
            updateEarthLives()
            AMMO = []
            spawnAlien()
            generateWord()
            textBox()
    gameOver()

def start_game():
    game_canvas.delete("all")
    createGameLayout()
    main()
# start_game()
mainMenu()
# Initialize the main canvas
root.mainloop()


