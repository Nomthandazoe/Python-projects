from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/zulu_words.csv")
    words = original_data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)
    current_card = random.choice(words)
    canvas.itemconfig(card_title, text="Zulu")
    canvas.itemconfig(card_word, text=current_card["Zulu"])
    canvas.itemconfig(card_background, image=front_image)
    flip_timer = screen.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card_background, image=back_image)


def known_card():
    words.remove(current_card)
    data = pandas.DataFrame(words)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


screen = Tk()
screen.title("Flash card")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = screen.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, font=("Ariel", 40))
card_word = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
unknown_word_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_word_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
known_word_button = Button(image=right_image, highlightthickness=0, command=known_card)
known_word_button.grid(row=1, column=1)

next_card()

screen.mainloop()
