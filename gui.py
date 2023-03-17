import tkinter as tk
from tkinter import *
from tkinter import ttk

TITLE_FONT = ("Arial", 28)


class Application(Tk):

    """Initialising Tkinter. This class initialises the root of Tkinter
    for the creation of the main window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.title(f"Trading App")
        self.geometry(f"700x650+900+350")
        # keep geometry 700x650
        # self.configure(background='#f78d63')

        # Use built-in style 'classic'
        self.style = ttk.Style(self)
        self.style.theme_use('classic')

        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='Purple')

        master_container = Frame(self)
        master_container.pack(side='top', fill='both', expand=True)
        master_container.grid_columnconfigure(0, weight=1)
        master_container.grid_rowconfigure(0, weight=1)

        # dictionary that will contain each page in the trading app
        self.pages = {}

        starting_frame = AccountPage(master_container, self)
        self.pages[AccountPage] = starting_frame

        starting_frame.grid(row=0, column=0, sticky='nsew')

        self.display_frame(AccountPage)

    def display_frame(self, cont):
        frame = self.pages[cont]
        frame.tkraise()


class AccountPage(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        # Container for attached frames

        self.pad_options = {'padx': 0, 'pady': 10}
        title = Label(self, text='Login Screen', font=TITLE_FONT)
        title.pack(**self.pad_options)
        # title.grid(row=0, column=1, **self.pad_options, sticky='nsew')



if __name__ == '__main__':
    app = Application()
    app.mainloop()
