from kivy.logger import Logger
from threading import Thread
from sys import version_info
import socket
PY = version_info[0]
if PY == 3:
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty


class SimpleServer(object):
    max_clients = None
    port = None
    ip = None
    queue = Queue()
    clients = {}

    def start(self, ip='localhost', port=9995, max_clients=5):
        Logger.info(
            'SimpleServer: starting on ip: {} port: {} max_clients: {}'.format(
                ip, port, max_clients))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(max_clients)
        self.ip, self.port, self.max_clients = ip, port, max_clients
        self._add_client_handler()

    def _add_client_handler(self):
        ClientHandler(self, len(self.clients), self.sock)

    def read_queue(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            pass

    def _on_connect(self, client):
        self.on_connect(client)
        if len(self.clients) < self.max_clients:
            self._add_client_handler()

    def _on_disconnect(self, client):
        self.on_disconnect(client)
        del self.clients[client.id]

    def handle_message(self, client, data):
        self.queue.put([client, data])

    def on_connect(self, client):
        pass

    def on_disconnect(self, client):
        pass


class ClientHandler(object):
    active = False
    server = None
    thread = None
    conn = None
    addr = None
    id = None

    def __init__(self, server, id, sock):
        self.id, self.server = id, server
        self.update_server_clients()
        self.thread = Thread(target=self.handle_clients, args=(sock,))
        self.thread.daemon = True
        self.thread.start()

    def handle_clients(self, sock):
        self.active = True
        self.conn, self.addr = sock.accept()
        self.update_server_clients()
        self.server._on_connect(self)
        try:
            while self.active:
                data = self.conn.recv(4096)
                if not data or data == b'':

                    break
                if PY == 3:
                    data = str(data, 'utf-8')
                self.server.handle_message(self, data)
        except Exception as e:
            Logger.info('ClientHandler: handle_clients: {}'.format(e))

        self.active = False
        self.server._on_disconnect(self)

    def send_msg(self, msg):
        if PY == 3:
            msg = bytes(msg, 'utf-8')
        self.conn.sendall(msg)

    def update_server_clients(self):
        self.server.clients[self.id] = {
            'id': self.id, 'handler': self,
            'conn': self.conn, 'addr': self.addr}
