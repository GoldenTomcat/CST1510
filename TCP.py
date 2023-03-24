import socket
from socket import *
import threading
from database import *
from bs4 import BeautifulSoup
import requests

# HOST = 'Localhost'
#
# PORT = 5000
# BUFFSIZE = 1024


# ADDRESS = (HOST, PORT)

# connection = socket(AF_INET, SOCK_STREAM)
# connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#
# connection.bind(ADDRESS)
# connection.listen(5)
#
# while True:
#
#     print("Waiting for connection..........")
#     (client, address) = connection.accept()
#
#     client.send("TEST MESSAGE".encode())
#     client.close()


class TCP:

    def __init__(self, hostname, port, buffsize):
        # Define our constants
        self.__hostname = hostname
        self.__port = port
        self.__buffsize = buffsize
        self.__address = (hostname, port)
        # Define the socket
        self.__connection_socket = socket(AF_INET, SOCK_STREAM)

        # Allows the port number to be re-used upon application closure and prevents the 'socket in use' err
        self.__connection_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def get_socket(self):
        return self.__connection_socket

    def get_hostname(self):
        return self.__hostname

    def set_hostname(self, hostname):
        self.__hostname = hostname

    def get_port(self):
        return self.__port

    def set_port(self, port):
        self.__port = port

    def get_buffsize(self):
        return self.__buffsize

    def set_buffsize(self, buffsize):
        self.__buffsize = buffsize

    def get_address(self):
        return self.__address

    def receive_message(self):
        return self.get_socket().recv(self.get_buffsize()).decode()

    def send_message(self, message):
        self.__message = message
        self.get_socket().send(message.encode())


class Client(TCP):

    def init(self, hostname, port, buffsize):
        super().__init__(hostname, port, buffsize)

    def establish_connection(self):
        self.get_socket().connect(self.get_address())

    def client_run(self, message):
        client_sock = socket(AF_INET, SOCK_STREAM)
        address = ('localhost', 5000)
        client_sock.connect(address)
        # print(self.get_socket())
        # self.establish_connection()
        # print(self.get_socket())

        # while True:
        # self.get_socket().send(message.encode())
        client_sock.send(message.encode())
        response = client_sock.recv(self.get_buffsize()).decode()
        print(response)

            #message = input("Enter message: ")
            #message = 'test'
            # if message == 'end':
            #     break
            # else:
            #     self.get_socket().send(message.encode())
        # self.get_socket().shutdown(1)
        client_sock.close()
        return response


class Server(TCP):

    def __init__(self, hostname, port, buffsize):
        super().__init__(hostname, port, buffsize)
        self.__connection_socket = socket(AF_INET, SOCK_STREAM)

    def bind(self, clients):
        self.__connection_socket.bind(self.get_address())
        self.__connection_socket.listen(clients)

    def run(self):

        self.bind(5)

        while True:
            print('Waiting for connection......')
            (client, address) = self.__connection_socket.accept()
            print("Connection from" + str(address))
            #client.send("test_successful".encode())

            while True:
                message = client.recv(TCP.get_buffsize(self)).decode()
                if message[:6] == 'INSERT':
                    accounts.insert_record(message)
                    reply = 'records inserted'
                    client.send(str(reply).encode())

                elif message[:13] == 'SELECT EXISTS':
                    reply = accounts.custom_command(message)
                    print(f"Does it exist? {str(reply)}")
                    client.send(str(reply).encode())

                #accounts.custom_command(message)
                if not message:
                    break
                #accounts.set_query(message)

                # if message == "CREATE ACCOUNT":
                #     AccountDatabase.set_query(INSERT_ACCOUNT)
                # elif message == "LOGIN":
                #
                #     query = f"SELECT EXISTS(SELECT * FROM accounts WHERE username = '{username}' " \
                #             f"AND password = '{password}');"
                # elif message == 'MONEY IN':
                #     pass
                # elif message == 'MONEY OUT':
                #     pass
                # elif message == 'PORTFOLIO VIEW':
                #     pass
                # elif message == 'INVEST':
                #     pass

                print(f"{str(address)} says {str(message)}")
                #message = accounts.custom_command(message)
                print(type(message))
                # message = 'Received'
                #message = input("send data: ")
                #client.send(str(reply).encode())

            client.close()


class Scraper:

    def __init__(self, target_website):
        self.target_website = target_website
        self.target_website = requests.get("https://coinranking.com")
        self.soup = BeautifulSoup(self.target_website.text, 'html.parser')

    def name_plus_price(self):
        names = self.soup.find_all('a', attrs={'class': 'profile__link'})
        prices = self.soup.find_all('div', attrs={'class': 'valuta valuta--light'})

        #for name, price in zip(names, prices):
        x = [name.get_text().replace('\n', '') + price.get_text().replace('\n', '') for name, price in zip(names, prices)]
            #print(name.get_text() + price.get_text())
        #print(x)
        x_stripped = [s.strip() for s in x]
        print(x_stripped)


def scraper():
    scrape = Scraper("https://coinranking.com")
    scrape.name_plus_price()

def server_runtime():
    server = Server('localhost', 5000, 1024)
    server.run()


def main():
    accounts.create_database('accounts')
    # TODO: Limit accounts in gui to params of the sql table i.e max 20 char for name
    create_table_accounts = "CREATE TABLE accounts(accountId VARCHAR(20) NOT NULL, username VARCHAR(20) NOT NULL, " \
                            "password VARCHAR (20) NOT NULL, startMoney int NOT NULL);"

    accounts.set_query(create_table_accounts)
    print(accounts.get_query())

    accounts.create_table()
    t1 = scraper
    t2 = server_runtime
    threading.Thread(target=t1).start()
    threading.Thread(target=t2).start()
    # accounts.custom_command("SHOW DATABASES")


if __name__ == '__main__':
    accounts = AccountDatabase('localhost', 'root', '1234')
    # server = Server('localhost', 5000, 1024)
    main()
    # server.run()

#print(help(Client))
