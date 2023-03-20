import tkinter as tk
from tkinter import *
from tkinter import ttk

# Constants for font style + TCP
TITLE_FONT = ("Arial", 28)
HOST = 'Localhost'
PORT = 5001


class Application(Tk):

    """Initialising Tkinter. This class initialises the root of Tkinter
    for the creation of the main window"""

    # Removed *args and **kwargs for now (idk why I put them in in the first place)

    def __init__(self):
        super().__init__()

        # Basic definitions for the main Application window
        self.title(f"Trading App")
        self.geometry(f"700x650+900+350")
        # keep geometry 700x650
        # self.configure(background='#f78d63')

        # Use built-in style 'classic' for aesthetics
        self.style = ttk.Style(self)
        self.style.theme_use('classic')

        # Created a style using ttk for a purple background
        # TODO: Utilise the style and probably change the colour
        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='Purple')

        # Create a master container spanning the whole window. Everything goes in here
        master_container = Frame(self)
        master_container.pack(side='top', fill='both', expand=True)
        master_container.grid_columnconfigure(0, weight=1)
        master_container.grid_rowconfigure(0, weight=1)

        # dictionary that will contain each page in the trading app
        self.pages = {}

        # Tuple of existing pages
        pages = (AccountPage, PortfolioView, InvestmentPage)
        # Loop over tuple
        for page in pages:

            starting_frame = page(master_container, self)
            self.pages[page] = starting_frame

            starting_frame.grid(row=0, column=0, sticky='nsew')

        self.display_frame(AccountPage)

    def display_frame(self, cont):
        frame = self.pages[cont]
        frame.tkraise()


class AccountPage(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        # Container for attached frames

        self.pad_options = {'padx': 0, 'pady': 10, 'sticky': 'ew'}
        title = Label(self, text='Login Screen', font=TITLE_FONT)
        title.columnconfigure(0, weight=1)
        title.grid(row=0, column=6, **self.pad_options)
        # title.grid(row=0, column=1, **self.pad_options, sticky='nsew')

        Create_Account = ttk.Button(self, text='Create_Account', command=None)

        # TODO: Button should only proceed to login if login details correct. Login box either on page or window.
        login = ttk.Button(self, text='Login', command=lambda: controller.display_frame(PortfolioView))
        Create_Account.grid(row=5, column=1, **self.pad_options)
        login.grid(row=5, column=2, **self.pad_options)


class PortfolioView(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.pad_options = {'row': 0, 'column': 6, 'padx': 0, 'pady': 10, 'sticky': 'ew'}
        title = Label(self, text='Portfolio', font=TITLE_FONT)
        title.grid(**self.pad_options)
        invest = ttk.Button(self, text='Invest', command=lambda: controller.display_frame(InvestmentPage))
        invest.grid(row=5, column=1, padx=0, pady=10, sticky='ew')


class InvestmentPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.pad_options = {'row': 0, 'column': 6, 'padx': 0, 'pady': 10, 'sticky': 'ew'}
        title = Label(self, text='Invest', font=TITLE_FONT)
        title.grid(**self.pad_options)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
