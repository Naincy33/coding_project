import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import os

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
draw_sound = pygame.mixer.Sound("draw.wav")

image_files = {
    "Rock": "rock.png",
    "Paper": "paper.png",
    "Scissors": "scissors.png"
}

choices = ["Rock", "Paper", "Scissors"]
player_score = 0
comp_score = 0
player_name = ""

LEADERBOARD_FILE = "leaderboard.txt"

def load_images():
    return {
        name: ImageTk.PhotoImage(Image.open(file).resize((120, 120)))
        for name, file in image_files.items()
    }

def update_leaderboard(winner):
    if not winner:
        return
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(winner + "\n")
    with open(LEADERBOARD_FILE, "r") as f:
        names = f.readlines()
    counts = {}
    for name in names:
        name = name.strip()
        counts[name] = counts.get(name, 0) + 1
    text = "🏆 Leaderboard:\n"
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        text += f"{k}: {v} wins\n"
    leaderboard_text.set(text)

def start_game(name):
    global player_name
    player_name = name
    name_window.destroy()
    main_game()

def play(player_choice):
    global player_score, comp_score
    click_sound.play()
    comp_choice = random.choice(choices)

    player_image.config(image=images[player_choice])
    comp_image.config(image=images[comp_choice])

    if player_choice == comp_choice:
        result.set("It's a Draw! 😐")
        draw_sound.play()
        update_leaderboard(None)
    elif (player_choice == "Rock" and comp_choice == "Scissors") or \
         (player_choice == "Paper" and comp_choice == "Rock") or \
         (player_choice == "Scissors" and comp_choice == "Paper"):
        result.set(f"{player_name} Wins! 🎉")
        win_sound.play()
        player_score += 1
        update_leaderboard(player_name)
    else:
        result.set("Computer Wins 😢")
        lose_sound.play()
        comp_score += 1
        update_leaderboard("Computer")

    score.set(f"{player_name}: {player_score}  |  Computer: {comp_score}")

def reset_game():
    global player_score, comp_score
    player_score = 0
    comp_score = 0
    score.set(f"{player_name}: 0  |  Computer: 0")
    result.set("")
    player_image.config(image='')
    comp_image.config(image='')

def main_game():
    global root, player_image, comp_image, result, score, leaderboard_text, images

    root = tk.Tk()
    root.title("Rock Paper Scissors Game 🎮")

    images = load_images()

    tk.Label(root, text="Rock Paper Scissors", font=("Arial", 20)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack()

    player_image = tk.Label(frame)
    player_image.grid(row=0, column=0, padx=20)

    comp_image = tk.Label(frame)
    comp_image.grid(row=0, column=1, padx=20)

    result = tk.StringVar()
    tk.Label(root, textvariable=result, font=("Arial", 16)).pack(pady=10)

    score = tk.StringVar()
    score.set(f"{player_name}: 0  |  Computer: 0")
    tk.Label(root, textvariable=score, font=("Arial", 14)).pack()

    leaderboard_text = tk.StringVar()
    leaderboard_label = tk.Label(root, textvariable=leaderboard_text, font=("Arial", 12), fg="blue")
    leaderboard_label.pack(pady=5)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    for choice in choices:
        tk.Button(btn_frame, text=choice, width=10, font=("Arial", 12),
                  command=lambda c=choice: play(c)).pack(side=tk.LEFT, padx=5)

    tk.Button(root, text="🔄 Reset Game", command=reset_game, bg="orange").pack(pady=10)

    update_leaderboard(None)
    root.mainloop()

# Name input window
name_window = tk.Tk()
name_window.title("Enter Your Name")

tk.Label(name_window, text="Enter your name:", font=("Arial", 14)).pack(pady=10)
name_entry = tk.Entry(name_window, font=("Arial", 12))
name_entry.pack(pady=5)

def confirm_name():
    name = name_entry.get().strip()
    if name:
        start_game(name.capitalize())

tk.Button(name_window, text="Start Game", command=confirm_name, bg="lightgreen").pack(pady=10)

name_window.mainloop()
