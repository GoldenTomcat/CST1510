from socket import *

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
        return self.__connection_socket.recv(TCP.get_buffsize(self)).decode()

    def send_message(self, message):
        self.__message = message
        self.get_socket().send(message.encode())


class Client(TCP):

    def init(self, hostname, port, buffsize):
        super().__init__(hostname, port, buffsize)

    def establish_connection(self):
        self.get_socket().connect(self.get_address())

    def client_run(self):
        self.establish_connection()

        while True:
            response = self.get_socket().recv(self.get_buffsize()).decode()
            print(response)

            message = input("Enter message: ")
            if message == 'end':
                break
            else:
                self.get_socket().send(message.encode())

        self.get_socket().close()


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
            client.send("test".encode())

            while True:
                message = client.recv(TCP.get_buffsize(self)).decode()
                if not message:
                    break
                print(f"{str(address)} says {str(message)}")
                message = input("send data: ")
                client.send(message.encode())

            client.close()


#print(help(Client))
