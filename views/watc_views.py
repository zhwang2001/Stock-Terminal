import tkinter as tk


class Watc:
    def __init__(self, active_frame, info, win_width, win_height):
        self.active_frame = active_frame
        self.info = info
        self.win_width = win_width
        self.win_height = win_height

    def main(self):
        watc = tk.Label(self.active_frame, bg="black", fg="deep sky blue", text="Watc", font="Helvetica 12 bold")
        watc.grid(row=0, column=0)
