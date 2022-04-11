import socket


class HTTPserver:
    def __init__(self, SERVER_HOST='0.0.0.0', SERVER_PORT=8000):
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        print('Listening on port %s ...' % self.SERVER_PORT)

    def run(self):
        while True:
            client_connection, client_address = self.server_socket.accept()
            request = client_connection.recv(1024).decode()
            response = 'HTTP/1.0 200 OK\n\nHello World'
            client_connection.sendall(response.encode())
            client_connection.close()


if __name__ == "__main__":
    server = HTTPserver()
    server.run()
