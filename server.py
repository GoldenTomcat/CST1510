from TCP import Server

if __name__ == '__main__':
    server = Server('localhost', 5000, 1024)
    server.run()
