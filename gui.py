from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from TCP import Client
from threads import *
import random

# Constants for font style + TCP
TITLE_FONT = ("Arial", 28)


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
        self.controller = controller

        self.pad_options = {'padx': 10, 'pady': 10, 'side': TOP}
        title = Label(self, text='Login Screen', font=TITLE_FONT)
        # title.columnconfigure(0, weight=1)
        # title.grid(row=0, column=6, **self.pad_options)
        title.pack(**self.pad_options)
        # title.grid(row=0, column=1, **self.pad_options, sticky='nsew')

        create_account_button = ttk.Button(self, text='Create_Account',
                                           command=lambda: controller.display_frame(AccountCreation))

        # TODO: Button should only proceed to login if login details correct. Login box either on page or window.
        # login_button = ttk.Button(self, text='Login', command=lambda: controller.display_frame(PortfolioView))
        login_button = ttk.Button(self, text='Login', command=lambda: self.login_button_check(self.controller))

        create_account_button.pack(**self.pad_options)
        login_button.pack(**self.pad_options)
        account_frame = Frame(self, width=100, height=50, bg='pink')
        account_frame.pack(**self.pad_options)

        self.login_username = StringVar()
        self.login_password = StringVar()
        self.username_get = self.login_username.get()

        user_name_entry = Entry(account_frame, textvariable=self.login_username)
        password_entry = Entry(account_frame, show="*", textvariable=self.login_password)
        user_name_entry.pack()

        password_entry.pack()

    def login_button_check(self, controller):
        username = self.login_username.get()

        password = self.login_password.get()
        query = f"SELECT EXISTS(SELECT * FROM accounts WHERE username = '{username}' " \
                f"AND password = '{password}');"
        reply = client.client_run(query)
        print(f"DEBUG REPLY: {reply}")
        print("DEBUG", client)
        if str(reply) == "(1,)":
            print("success")
            controller.display_frame(PortfolioView)
        else:
            print("Incorrect Login details")
            messagebox.showinfo("Bad login", "Bad Login Details")


class AccountCreation(ttk.Frame):
    """TTK Frame for creation of account"""

    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')

        self.starting_money_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()

        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='orange')
        self.pad_options = {'padx': 10, 'pady': 10, 'side': TOP}
        title = Label(self, text='Create your account', font=TITLE_FONT)
        title.pack(**self.pad_options)

        self.frame_options = {'master': self, 'width': 100, 'height': 50, 'bg': 'pink', 'padx': 10, 'pady': 10}

        # Create a LabelFrame for each field then use a loop to pack them
        starting_money_frame = LabelFrame(**self.frame_options, text='Money to invest')
        username_frame = LabelFrame(**self.frame_options, text='Username')
        password_frame = LabelFrame(**self.frame_options, text='Password')
        frame_list = [starting_money_frame, username_frame, password_frame]
        for frame in frame_list:
            frame.pack()

        # Create an entry for each field, use a loop to pack them
        starting_money_entry = Entry(starting_money_frame, textvariable=self.starting_money_var)
        username_entry = Entry(username_frame, textvariable=self.username_var)
        password_enrtry = Entry(password_frame, textvariable=self.password_var, show='*')
        entry_list = [starting_money_entry, username_entry, password_enrtry]
        for entry in entry_list:
            entry.pack()

        # Buttons to create the account and to go back.
        create_account = ttk.Button(self, text='CREATE', command=lambda: self.send_account_data())
        go_back = ttk.Button(self, text='Go Back', command=lambda: controller.display_frame(LoginPage))
        create_account.pack()
        go_back.pack(side=BOTTOM, pady=10, padx=10)

    def send_account_data(self):
        account_id = random.randint(1, 100)
        username = self.username_var.get()
        password = self.password_var.get()
        start_cash = self.starting_money_var.get()
        query = f"INSERT INTO accounts (accountId, username, password, startMoney) values " \
                f"({account_id}, '{username}', '{password}', {start_cash})"
        client.client_run(query)


class PortfolioView(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')

        self.account_id = StringVar()

        # Define style for this ttk frames
        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='orange')
        self.pad_options = {'padx': 10, 'pady': 10}
        title = Label(self, text='Portfolio', font=TITLE_FONT)
        title.pack(**self.pad_options)

        self.frame_options = {'master': self, 'width': 200, 'height': 350, 'bg': 'pink', 'padx': 10, 'pady': 10}
        self.transactions_frame = LabelFrame(**self.frame_options, text='Transactions Key: (Transaction ID, AccountID, '
                                                                        'currency, date of purchase, quantity, cost')
        self.transactions_frame.pack(fill='both')
        self.details = Message(self.transactions_frame, text='Refresh me!',
                               font=('arial', 10), aspect=150, width=100)
        self.details.pack()

        account_id_frame = LabelFrame(self, width=150, height=50, bg='pink',
                                      **self.pad_options, text='Enter Account number')
        account_id_frame.pack()
        account_id_entry = Entry(account_id_frame, textvariable=self.account_id)
        account_id_entry.pack(**self.pad_options)

        refresh_button = ttk.Button(self, text='Refresh', command=lambda: self.refresh_button_press())
        refresh_button.pack(**self.pad_options)

        invest = ttk.Button(self, text='Invest', command=lambda: controller.display_frame(InvestmentPage))
        invest.pack(**self.pad_options, side=BOTTOM)
        go_back = ttk.Button(self, text='Go Back', command=lambda: controller.display_frame(LoginPage))
        go_back.pack(side=BOTTOM, pady=10, padx=10)

    def refresh_button_press(self):
        account_id = self.account_id.get()
        print("ACCOUNT ID DEBUG:", account_id)
        query = f"SELECT * FROM transactions WHERE accountId='{account_id}';"
        print("QUERY DEBUG:", query)
        reply = client.client_run(query)
        print(f"DEBUG REPLY: {reply}")
        print("DEBUG", client)
        self.details.destroy()
        self.details = Message(self.transactions_frame, text=reply,
                               font=('arial', 10), aspect=250)
        self.details.pack()


class InvestmentPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, style='Window_Styles.TFrame')

        master_style = ttk.Style()
        master_style.configure("Window_Styles.TFrame", background='orange')

        self.buy_ammount = IntVar()
        self.coin_selection = StringVar()
        self.account_number = StringVar()


        self.pad_options = {'padx': 10, 'pady': 10}
        title = Label(self, text='Invest', font=TITLE_FONT)
        title.pack(**self.pad_options)
        self.investment_frame = LabelFrame(self, width=150, height=250, bg='pink', text='cryptocurrencies')
        self.investment_frame.pack(self.pad_options, fill='both')
        self.message_options = {'master': self.investment_frame, 'font':
            ('arial', 10), 'aspect': 250}

        self.crypto = Message(**self.message_options, text='Refresh me!')

        self.crypto.pack(**self.pad_options)

        refresh_button = ttk.Button(self, text='Refresh', command=lambda: self.refresh_button_press())
        refresh_button.pack(**self.pad_options)
        buy_frame = LabelFrame(self, width=100, height=250, bg='pink', text='Buying')
        buy_frame.pack(**self.pad_options)
        amount_label = Label(buy_frame, text='Amount')
        amount_label.pack()
        buy_entry = Entry(buy_frame, textvariable=self.buy_ammount)
        coin_entry = Entry(buy_frame, textvariable=self.coin_selection)
        buy_entry.pack(**self.pad_options)
        coin_label = Label(buy_frame, text='Coin')
        coin_label.pack(**self.pad_options)
        coin_entry.pack(**self.pad_options)
        account_label = Label(buy_frame, text='AccountId')
        account_label.pack(**self.pad_options)
        account_entry = Entry(buy_frame, textvariable=self.account_number)
        account_entry.pack(**self.pad_options)
        buy_button = ttk.Button(self, text='Buy', command=lambda: self.buy_button())
        buy_button.pack(**self.pad_options)

        go_back = ttk.Button(self, text='Go Back', command=lambda: controller.display_frame(PortfolioView))
        go_back.pack(side=BOTTOM, pady=10, padx=10)

    def refresh_button_press(self):
        query = f"SELECT * FROM coins;"
        print("QUERY DEBUG:", query)
        reply = client.client_run(query)
        print(f"DEBUG REPLY: {reply}")
        print("DEBUG", client)

        self.crypto = Message(self.investment_frame, text=reply,
                              font=('arial', 10), aspect=250)
        self.crypto.pack()

        query = f"SELECT * FROM coins"
        reply = client.client_run(query)
        print("DEBUG COINS SHOW:", reply)
        self.coin_info = reply

    def buy_button(self):
        amount = self.buy_ammount.get()
        coin = self.coin_selection.get()
        transaction_id = random.randint(1, 100)
        account = self.account_number.get()
        cost = "27812.15"
        date = "27/03/2022"
        query = f"INSERT INTO transactions (transactionId, accountId, currency, datePurchase, " \
                f"quantity, cost) values ({transaction_id}, {account}, '{coin}', '{date}', {amount}, {cost});"

        client.client_run(query)


def gui_app():
    app = Application()
    app.mainloop()


# def client_networking():
# client = Client('localhost', 5000, 1024)
# client.client_run()


def main():
    t1 = gui_app
    # t2 = client_networking
    threading.Thread(target=t1).start()
    # threading.Thread(target=t2, daemon=True).start()


if __name__ == '__main__':
    client = Client('localhost', 5000, 1024)
    # client.client_run()
    main()
