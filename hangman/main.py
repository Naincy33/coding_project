import tkinter as tk
from tkinter import PhotoImage
import random



WORD_POOL = [
    'banana', 'keyboard', 'elephant', 'umbrella', 'notebook', 'freedom',
    'dragon', 'internet', 'mystery', 'wizard', 'penguin', 'jungle',
    'python', 'moonlight', 'backpack', 'glasses', 'laptop', 'sunshine',
    'bicycle', 'mountain', 'hangman', 'language', 'fantasy', 'rocket',
    'firefly', 'shadow', 'adventure', 'galaxy', 'pirate', 'treasure',
    'window', 'blanket', 'coffee', 'castle', 'desert', 'tornado'
]


WORDS = random.sample(WORD_POOL, 10)

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game with Images")

        self.images = [PhotoImage(file=f"hangman{i}.png") for i in range(7)]
        self.word = random.choice(WORDS)
        self.missed = []
        self.correct = []

        self.setup_gui()

    def setup_gui(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        self.word_label = tk.Label(self.root, text="_ " * len(self.word), font=("Arial", 24))
        self.word_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack()

        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, command=lambda l=letter: self.guess_letter(l.lower()))
            btn.grid(row=i // 9, column=i % 9)
            self.letter_buttons[letter] = btn

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Play Again", command=self.reset_game)
        self.reset_button.pack(pady=10)
        self.reset_button.pack_forget()

        self.update_display()

    def update_display(self):
        self.image_label.config(image=self.images[len(self.missed)])
        display = " ".join([l if l in self.correct else "_" for l in self.word])
        self.word_label.config(text=display)

    def guess_letter(self, letter):
        self.letter_buttons[letter.upper()]["state"] = "disabled"

        if letter in self.word:
            self.correct.append(letter)
        else:
            self.missed.append(letter)

        self.update_display()
        self.check_game_over()

    def check_game_over(self):
        if all(l in self.correct for l in self.word):
            self.status_label.config(text=f"You won! Word was '{self.word}'")
            self.disable_all_buttons()
        elif len(self.missed) == 6:
            self.status_label.config(text=f"You lost! Word was '{self.word}'")
            self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.letter_buttons.values():
            btn["state"] = "disabled"
        self.reset_button.pack()

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.missed.clear()
        self.correct.clear()
        self.status_label.config(text="")
        self.reset_button.pack_forget()
        for btn in self.letter_buttons.values():
            btn["state"] = "normal"
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
