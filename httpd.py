import os
import socket
import logging
import threading
import queue
import time
import random
import urllib.parse

from mimetypes import MimeTypes
from optparse import OptionParser
from datetime import datetime, timezone


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            time.sleep(random.randint(1, 10) / 100)  # джитер
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


def format_response(code, filename="", file_data=b"", head=False, content_length=0):
    """
    add headers Date, Server, Content-Length, Content-Type, Connection
    """
    headers = f'HTTP/1.0 {code}'.encode("utf-8") + b"\r\n"
    headers += f"Date:{datetime.now(timezone.utc)}".encode("utf-8") + b"\r\n"
    headers += "Server: DZ5".encode("utf-8") + b"\r\n"
    if not head:
        headers += f"Content-Length: {len(file_data)}".encode("utf-8") + b"\r\n"
    else:
        headers += f"Content-Length: {content_length}".encode("utf-8") + b"\r\n"
    mime = MimeTypes()
    mime_type = mime.guess_type(filename)
    if filename:
        if filename.endswith(".js"):  # mime type не верно определяется для js
            headers += "Content-Type: text/javascript".encode("utf-8") + b"\r\n"
        else:
            headers += f"Content-Type: {mime_type[0]}".encode("utf-8") + b"\r\n"
    headers += "Connection: close\n\n".encode("utf-8")
    if head:
        response = headers + b"\r\n\r\n"
    else:
        response = headers + file_data
    return response


def check_path(root, file_path):
    if r"/../" not in file_path:
        return True
    abs_file_path = os.path.abspath(os.path.realpath(file_path))
    for r, dirs, files in os.walk(root):
        for filename in files:
            if filename == abs_file_path:
                return True
    return False


def format_response_for_head(file_path):
    try:
        length = os.stat(f'{file_path}').st_size
        return format_response(code="200 OK", head=True, content_length=length)
    except FileNotFoundError:
        return format_response(code="404 File Not Found")


def format_response_for_get(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            filename = file_path.split(r"/")[-1]
            return format_response(code="200 OK", filename=filename, file_data=file_data)
    except (FileNotFoundError, NotADirectoryError, PermissionError, OSError) as exc:
        return format_response(code="404 File Not Found")


def format_filepath(file_path):
    if '?' in file_path:
        file_path = file_path.split('?')[0]
    if file_path.endswith(r"/"):
        file_path += "index.html"
    return file_path


def request_processing(root, request):
    if request.startswith("GET") or request.startswith("HEAD"):
        req_lines = request.split('\n')
        get_first_arg = req_lines[0].split(',')[0].split(' ', 1)[1].split(' HTTP')[0]
        if get_first_arg.startswith(r"/"):
            file_path = root + get_first_arg
            if not check_path(root, file_path):
                return format_response(code="403 Forbidden")
            file_path = format_filepath(file_path)
            if request.startswith("HEAD"):
                return format_response_for_head(file_path)
            return format_response_for_get(file_path)
        else:
            return format_response(code="404 File Not Found")
    else:
        return format_response(code="405 Method Not Allowed")


def get_data(client_connection):
    data = b''
    while True:
        new_data = client_connection.recv(1024)
        if not new_data:
            break
        data += new_data
        if b'\r\n\r\n' in data:
            break
    return data


def request_answer(root, client_connection, client_address):
    logging.info('Accept new connection from %s:%s...' % client_address)
    if isinstance(client_connection, socket.socket):
        data = get_data(client_connection)
        request = urllib.parse.unquote(data.decode('utf-8'))
        response = request_processing(root, request)
        if response:
            if len(response) > 1024:  # Большие данные передаются по частям
                while len(response) > 1024:
                    client_connection.sendall(response[0:1024])
                    response = response[1024:]
                if len(response):  # Если количество данных не кратно 1024 и после цикла что-то осталось
                    client_connection.sendall(response)
            else:
                client_connection.sendall(response)
        client_connection.close()


class HTTPserver:
    def __init__(self, root, host='0.0.0.0', port=8080, workers=2):
        self.host = host
        self.port = port
        self.workers = workers
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.root = root
        logging.info('Listening on port %s ...' % self.port)

    def run(self):
        thread_pool = ThreadPoolManger(self.workers)
        while True:
            client_connection, client_address = self.server_socket.accept()
            time.sleep(1)
            thread_pool.add_work(request_answer, *(self.root, client_connection, client_address))


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("-w", "--workers", action="store", type=int, default=2)
    op.add_option("-r", "--root", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPserver(root=opts.root, port=opts.port, workers=opts.workers)
    server.run()
