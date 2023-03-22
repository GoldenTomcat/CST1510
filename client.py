from TCP import Client

if __name__ == '__main__':
    client = Client('localhost', 5000, 1024)
    client.client_run()

