from tkinter import *
from tkinter import ttk
from TCP import Client
from threads import Threading

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
        self.resizable(False, False)

        # Use built-in style 'classic' for aesthetics
        self.style = ttk.Style(self)
        self.style.theme_use('classic')

        # Create a master container spanning the whole window. Everything goes in here
        master_container = Frame(self)
        master_container.pack(side='top', fill='both', expand=True)
        master_container.grid_columnconfigure(0, weight=1)
        master_container.grid_rowconfigure(0, weight=1)

        # dictionary that will contain each page in the trading app
        self.pages = {}

        # Tuple of existing pages
        pages = (LoginPage, PortfolioView, InvestmentPage, AccountCreation)
        # Loop over tuple
        for page in pages:
            starting_frame = page(master_container, self)
            self.pages[page] = starting_frame

            starting_frame.grid(row=0, column=0, sticky='nsew')

        self.display_frame(LoginPage)
        print(self.pages)

    def display_frame(self, cont):
        frame = self.pages[cont]
        frame.tkraise()


class LoginPage(ttk.Frame):

    # master is basically root
    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')
        # Container for attached frames

        self.pad_options = {'padx': 10, 'pady': 10, 'side': TOP}
        title = Label(self, text='Login Screen', font=TITLE_FONT)
        # title.columnconfigure(0, weight=1)
        # title.grid(row=0, column=6, **self.pad_options)
        title.pack(**self.pad_options)
        # title.grid(row=0, column=1, **self.pad_options, sticky='nsew')

        create_account_button = ttk.Button(self, text='Create_Account',
                                           command=lambda: controller.display_frame(AccountCreation))

        # TODO: Button should only proceed to login if login details correct. Login box either on page or window.
        login_button = ttk.Button(self, text='Login', command=lambda: controller.display_frame(PortfolioView))
        create_account_button.pack(**self.pad_options)
        login_button.pack(**self.pad_options)
        account_frame = Frame(self, width=100, height=50, bg='pink')
        account_frame.pack(**self.pad_options)

        user_name_entry = Entry(account_frame)
        password_entry = Entry(account_frame, show="*")
        user_name_entry.pack()

        password_entry.pack()


class AccountCreation(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')

        self.name_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()

        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='orange')
        self.pad_options = {'padx': 10, 'pady': 10, 'side': TOP}
        title = Label(self, text='Create your account', font=TITLE_FONT)
        title.pack(**self.pad_options)

        self.frame_options = {'master': self, 'width': 100, 'height': 50, 'bg': 'pink', 'padx': 10, 'pady': 10}

        # Create a LabelFrame for each field then use a loop to pack them
        names_frame = LabelFrame(**self.frame_options, text='Name')
        username_frame = LabelFrame(**self.frame_options, text='Username')
        password_frame = LabelFrame(**self.frame_options, text='Password')
        frame_list = [names_frame, username_frame, password_frame]
        for frame in frame_list:
            frame.pack()

        # Create an entry for each field, use a loop to pack them
        fname_entry = Entry(names_frame, textvariable=self.name_var)
        username_entry = Entry(username_frame, textvariable=self.username_var)
        password_enrtry = Entry(password_frame, textvariable=self.password_var, show='*')
        entry_list = [fname_entry, username_entry, password_enrtry]
        for entry in entry_list:
            entry.pack()

        # TODO: Create account button needs to send account info to server
        # Buttons to create the account and to go back.
        create_account = ttk.Button(self, text='CREATE', command=lambda: self.send_account_data())
        go_back = ttk.Button(self, text='Go Back', command=lambda: controller.display_frame(PortfolioView))
        create_account.pack()
        go_back.pack(side=BOTTOM, pady=10, padx=10)

    def send_account_data(self):
        client.send_message("CREATE ACCOUNT")


class PortfolioView(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')

        # Define style for this ttk frames
        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='orange')
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


def gui_app():
    app = Application()
    app.mainloop()


def main():
    Threading(gui_app(), True).start_thread()


if __name__ == '__main__':
    client = Client('localhost', 5000, 1024)
    # client.client_run()
    Threading(client.client_run(), True).start_thread()
    main()
