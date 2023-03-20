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
        self.__address = (self.__hostname, self.__port)
        # Define the socket
        self.__connection_socket = socket(AF_INET, SOCK_STREAM)

        # Allows the port number to be re-used upon application closure and prevents the 'socket in use' err
        self.__connection_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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

    def bind(self):
        self.__connection_socket.bind(self.__address)
        self.__connection_socket.listen(5)


class Client(TCP):

    def __init__(self, message):
        super().__init__()
        self.__connection_socket = socket(AF_INET, SOCK_STREAM)
        self.__message = message

    def establish_connection(self):
        self.__connection_socket.connect(TCP.get_address(self))

    def receive_message(self):
        return self.__connection_socket.recv(TCP.get_buffsize(self).decode())

    # This can probably be moved to TCP
    def send_message(self, message):
        self.__message = message
        self.__connection_socket.send(message.encode())

    # This can probably be moved to TCP
    def terminate_connection(self):
        self.__connection_socket.close()


class Server(TCP):

    def __init__(self, message):
        super().__init__()
        self.__connection_socket = socket(AF_INET, SOCK_STREAM)
        self.__mesage = message


print(help(Client))
