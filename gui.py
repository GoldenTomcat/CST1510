from tkinter import *


class Application(Tk):

    """Initialising Tkinter"""

    def __init__(self, x, y, position, title):
        super().__init__()
        self.title(f"{title}")
        self.geometry(f"{x}x{y}+{position}")
        # keep geometry 700x650
        self.configure(background='#f78d63')


if __name__ == '__main__':
    app = Application(700, 650, '900+350', 'Trading App')
    app.mainloop()