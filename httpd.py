import socket
import logging
import threading
import queue
import time
import random

from optparse import OptionParser
from datetime import datetime, timezone


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            time.sleep(random.randint(1, 10))  # джитер
            if self.work_queue.empty():
                continue
            else:
                func, args = self.work_queue.get()
                func(*args)
                self.work_queue.task_done()


class ThreadPoolManger:
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


class HTTPserver:
    def __init__(self, root, host='0.0.0.0', port=8080, workers=2):
        self.host = host
        self.port = port
        self.workers = workers
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.workers)
        self.root = root
        logging.info('Listening on port %s ...' % self.port)

    def send_answer(self, client_connection, client_address):
        logging.info('Accept new connection from %s:%s...' % client_address)
        if type(client_connection) == socket.socket and "fd=-1" not in str(client_connection):
            request = client_connection.recv(1024).decode()
            response = self.request_processing(request)
            client_connection.sendall(response.encode('utf-8'))
            client_connection.close()

    def run(self):
        thread_pool = ThreadPoolManger(self.workers)
        while True:
            client_connection, client_address = self.server_socket.accept()
            time.sleep(1)
            thread_pool.add_work(self.send_answer, *(client_connection, client_address))

    def request_processing(self, request):
        """
        !!!!!! Нужна поддержка регулярок
        """
        print(f"request {request} ")
        if request.startswith("GET") or request.startswith("HEAD"):
            req_lines = request.split('\n')
            get_first_arg = req_lines[0].split()[1]

            if get_first_arg.startswith(r"/"):
                if get_first_arg.startswith(r"/private_dir"):
                    return self.format_response(code="403 Forbidden")
                file_path = self.root + get_first_arg
                if '?' in file_path:
                    file_path = file_path.split('?')[0]
                try:
                    if file_path.endswith(r"/"):
                        file_path += "index.html"
                    try:
                        with open(file_path, 'r') as f:
                            file_data = f.read()
                            filename = file_path.split(r"/")[-1]
                            print(f"LOG filename {filename}")
                            return f'{self.format_response(code="200 OK", filename=filename, file_data=file_data)}'
                    except UnicodeDecodeError:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            filename = file_path.split(r"/")[-1]
                            return f'{self.format_response(code="200 OK", filename=filename, file_data=str(file_data))}'
                except FileNotFoundError:
                    return self.format_response(code="404 File Not Found")
            else:
                return 'HTTP/1.0 404 File Not Found'
        else:
            return self.format_response(code="405 Method Not Allowed")

    @staticmethod
    def format_response(code, filename="", file_data=""):
        """
        add headers Date, Server, Content-Length, Content-Type, Connection
        """
        response = f'HTTP/1.0 {code} \n'
        response += f"Date:{datetime.now(timezone.utc)}\n"
        response += "Server: DZ5\n"
        response += f"Content-Length: {len(file_data.encode('utf-8'))}\n"
        print(f"LOG2 {filename}  {filename.endswith('.html')}")
        if filename.endswith(".html"):
            response += "Content-Type: text/html\n"
        elif filename.endswith(".css"):
            response += "Content-Type: text/css\n"
        elif filename.endswith(".js"):
            response += "Content-Type: text/javascript\n"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            response += "Content-Type: image/jpeg\n"
        elif filename.endswith(".png"):
            response += "Content-Type: image/png\n"
        elif filename.endswith(".gif"):
            response += "Content-Type: image/gif\n"
        elif filename.endswith(".swf"):
            response += "Content-Type: application/x-shockwave-flash\n"
        response += "Connection: close\n\n"
        response += file_data
        print(f"LOG3 {response}")
        return response


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8000)
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("-w", "--workers", action="store", type=int, default=2)
    op.add_option("-r", "--root", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPserver(root=opts.root, port=opts.port, workers=opts.workers)
    server.run()
