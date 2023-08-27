import tkinter as tk


class Eqs:
    def __init__(self, active_frame, info, win_width, win_height):
        self.active_frame = active_frame
        self.info = info
        self.win_width = win_width
        self.win_height = win_height

    def main(self):
        eqs = tk.Label(self.active_frame, bg="black", fg="deep sky blue", text="Eqs", font="Helvetica 12 bold")
        eqs.grid(row=0, column=0)
