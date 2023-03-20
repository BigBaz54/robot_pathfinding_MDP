import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from game import Game
from mdp import Mdp
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1200x600")
grid_frame = ctk.CTkFrame(master=app, height=600, width=600)
grid_frame.grid(row=0, column=0)
settings_frame = ctk.CTkFrame(master=app, height=600, width=600, fg_color="#555555")
settings_frame.grid(row=0, column=1)
settings_frame.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

size = None
gamma = 0.9
tiles = []
tiles_type = None
game = None
mdp = None
values = None
policy = None

grass_color = "#2a3d23"
grass_hover_color = "#415e36"
robot_color = "#757575"
robot_hover_color = "#a0a0a0"
goal_color = "#a63d3c"
goal_hover_color = "#d95b5a"
swamp_color = "#3d2e11"
swamp_hover_color = "#5e4a2f"
firecamp_color = "#b05612"
firecamp_hover_color = "#d97a2e"

colors = [grass_color, robot_color, goal_color, swamp_color, firecamp_color]
hover_colors = [grass_hover_color, robot_hover_color, goal_hover_color, swamp_hover_color, firecamp_hover_color]
images = None
arrow_images = None
red_arrow_images = None


def switch_type(i, j):
    tiles_type[i, j] = (tiles_type[i, j] + 1) % 5
    tiles[i*size[1]+j].destroy()
    new_but = ctk.CTkButton(master=grid_frame, text='', height=600/size[0], width=600/size[1], corner_radius=0, border_color="black", border_width=1, command=lambda i=i, j=j: switch_type(i, j), image=images[tiles_type[i, j]], fg_color=colors[tiles_type[i, j]], hover_color=hover_colors[tiles_type[i, j]])
    tiles[i*size[1]+j] = new_but
    new_but.grid(row=i,column=j)

def update_gamma(value):
    global gamma
    gamma = round(value, 2)
    gamma_label.configure(text=(f"Gamma : {gamma}0" if len(str(gamma))==3 else f"Gamma : {gamma}"))

def update_images_size():
    global size
    global images
    global arrow_images
    global red_arrow_images
    max_size = max(size)
    grass_img = ctk.CTkImage(Image.open('img/grass.png'), size=(300/max_size, 300/max_size))
    robot_img = ctk.CTkImage(Image.open('img/robot.png'), size=(300/max_size, 300/max_size))
    goal_img = ctk.CTkImage(Image.open('img/goal.png'), size=(300/max_size, 300/max_size))
    swamp_img = ctk.CTkImage(Image.open('img/swamp.png'), size=(300/max_size, 300/max_size))
    firecamp_img = ctk.CTkImage(Image.open('img/firecamp.png'), size=(300/max_size, 300/max_size))
    up_arrow_img = ctk.CTkImage(Image.open('img/up_arrow.png'), size=(150/max_size, 150/max_size))
    right_arrow_img = ctk.CTkImage(Image.open('img/right_arrow.png'), size=(150/max_size, 150/max_size))
    down_arrow_img = ctk.CTkImage(Image.open('img/down_arrow.png'), size=(150/max_size, 150/max_size))
    left_arrow_img = ctk.CTkImage(Image.open('img/left_arrow.png'), size=(150/max_size, 150/max_size))
    red_up_arrow_img = ctk.CTkImage(Image.open('img/red_up_arrow.png'), size=(150/max_size, 150/max_size))
    red_right_arrow_img = ctk.CTkImage(Image.open('img/red_right_arrow.png'), size=(150/max_size, 150/max_size))
    red_down_arrow_img = ctk.CTkImage(Image.open('img/red_down_arrow.png'), size=(150/max_size, 150/max_size))
    red_left_arrow_img = ctk.CTkImage(Image.open('img/red_left_arrow.png'), size=(150/max_size, 150/max_size))
    images = [grass_img, robot_img, goal_img, swamp_img, firecamp_img]
    arrow_images = [up_arrow_img, right_arrow_img, down_arrow_img, left_arrow_img]
    red_arrow_images = [red_up_arrow_img, red_right_arrow_img, red_down_arrow_img, red_left_arrow_img]


def generate_grid(rows, columns):
    global size
    global tiles_type
    global tiles
    size = (rows, columns)
    update_images_size()
    tiles_type = np.zeros(size, dtype=int)
    if tiles != []:
        for tile in tiles:
            tile.destroy()
    tiles = []
    for i in range(size[0]):
        for j in range(size[1]):
            b = ctk.CTkButton(master=grid_frame, text='', height=600/size[0], width=600/size[1], corner_radius=0, border_color="black", border_width=1, command=lambda i=i, j=j: switch_type(i, j), image=images[tiles_type[i, j]], fg_color=colors[tiles_type[i, j]], hover_color=hover_colors[tiles_type[i, j]])
            tiles.append(b)
            b.grid(row=i,column=j)

def pathfind(goal_reward, swamp_reward, firecamp_reward):
    global game
    global mdp
    global values
    global policy 
    for tile in tiles:
        tile.configure(state="disabled")
    robot_pos = None
    goal_pos = None
    obstacles_pos = []
    firecamp_pos = []
    for i in range(size[0]):
        for j in range(size[1]):
            if tiles_type[i, j] == 1:
                robot_pos = (i, j)
            elif tiles_type[i, j] == 2:
                goal_pos = (i, j)
            elif tiles_type[i, j] == 3:
                obstacles_pos.append((i, j))
            elif tiles_type[i, j] == 4:
                firecamp_pos.append((i, j))
    game = Game(size, robot_pos, goal_pos, goal_reward, obstacles_pos, swamp_reward, firecamp_pos, firecamp_reward)
    mdp = Mdp(game, gamma)
    mdp.value_iteration()
    values = mdp.values
    policy = mdp.policy
    display_policy()

def display_policy():
    global tiles
    for tile in tiles:
        tile.destroy()
    tiles = []
    optimal_path = mdp.get_robot_path()[:-1]
    for i in range(size[0]):
        for j in range(size[1]):
            if (i,j) in optimal_path:
                b = ctk.CTkButton(master=grid_frame, state="disabled", text=f'V = {round(values[i*size[1]+j],1)}', height=600/size[0], width=600/size[1], corner_radius=0, border_color="black", border_width=1, fg_color=colors[tiles_type[i, j]], image=red_arrow_images[policy[i*size[1]+j]])
            else:   
                b = ctk.CTkButton(master=grid_frame, state="disabled", text=f'V = {round(values[i*size[1]+j],1)}', height=600/size[0], width=600/size[1], corner_radius=0, border_color="black", border_width=1, fg_color=colors[tiles_type[i, j]], image=arrow_images[policy[i*size[1]+j]])
            tiles.append(b)
            b.grid(row=i,column=j)


gamma_label = ctk.CTkLabel(master=settings_frame, text="Gamma : 0.90", font=('Helvetica', 20))
gamma_label.grid(row=0, column=0, columnspan=2, pady=(10,0))
slider = ctk.CTkSlider(master=settings_frame, from_=0, to=1, command=update_gamma, number_of_steps=100)
slider.grid(row=1, column=0, columnspan=2, pady=(5,0), padx=(20,20))

grid_label = ctk.CTkLabel(master=settings_frame, text="Grid settings", font=('Helvetica', 20))
grid_label.grid(row=2, column=0, columnspan=2, pady=(20,0))
rows_entry = ctk.CTkEntry(master=settings_frame, width=100, placeholder_text="Nb. of rows", font=('Helvetica', 13))
rows_entry.grid(row=3, column=0, padx=(5,0))
columns_entry = ctk.CTkEntry(master=settings_frame, width=100, placeholder_text="Nb. of columns", font=('Helvetica', 13))
columns_entry.grid(row=3, column=1, padx=(0,5))

reward_label = ctk.CTkLabel(master=settings_frame, text="Rewards settings", font=('Helvetica', 20))
reward_label.grid(row=4, column=0, columnspan=2, pady=(20,0))
goal_reward_entry = ctk.CTkEntry(master=settings_frame, width=100, placeholder_text="Goal reward", font=('Helvetica', 13))
goal_reward_entry.grid(row=5, column=0, padx=(5,0))
swamp_reward_entry = ctk.CTkEntry(master=settings_frame, width=100, placeholder_text="Swamp reward", font=('Helvetica', 13))
swamp_reward_entry.grid(row=5, column=1, padx=(0,5))
firecamp_reward_entry = ctk.CTkEntry(master=settings_frame, width=215, placeholder_text="Firecamp reward (optional)", font=('Helvetica', 13))
firecamp_reward_entry.grid(row=6, column=0, columnspan=2, pady=(5,0))

generate_grid_button = ctk.CTkButton(master=settings_frame, width=215, text="Generate grid", command=lambda: generate_grid(int(rows_entry.get()), int(columns_entry.get())))
generate_grid_button.grid(row=7, column=0, columnspan=2, pady=(5,0))

pathfind_button = ctk.CTkButton(master=settings_frame, width=215, text="Pathfind !", command=lambda: pathfind(int(goal_reward_entry.get()), int(swamp_reward_entry.get()), int(firecamp_reward_entry.get()) if firecamp_reward_entry.get() != "" else 0))
pathfind_button.grid(row=8, column=0, columnspan=2, pady=(5,10))

app.mainloop()