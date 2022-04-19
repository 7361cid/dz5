import socket
import logging
import threading
import queue
import time
import random

from optparse import OptionParser


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
                func, args = self.work_queue.get()   #block = False
   #             print(f"func run {func} args {args}  args[0] {args[0]}")
                func(*args)
                self.work_queue.task_done()


class ThreadPoolManger:
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):
            print("ThreadPoolManger")
            thread = WorkThread(self.work_queue)
            thread.start()
 #           thread.join()     # Возможная причина блокировки

    def add_work(self, func, *args):
        self.work_queue.put((func, args))
     #   print(f"add_work {list(self.work_queue.queue)}")

class HTTPserver:
    def __init__(self, root, host='0.0.0.0', port=8000, workers=2):
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
        request = client_connection.recv(1024).decode()
        response = self.request_processing(request)
        client_connection.sendall(response.encode())
        client_connection.close()

    def run(self):
        print("HTTPserver run")
        client_connection, client_address = self.server_socket.accept()
        thread_pool = ThreadPoolManger(self.workers)  #  BLOCKING??????????????
        while True:
            time.sleep(1)
            print("HTTPserver run3")
            thread_pool.add_work(self.send_answer, *(client_connection, client_address))


    def request_processing(self, request):
        return 'HTTP/1.0 200 OK\n\nHello World'


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
