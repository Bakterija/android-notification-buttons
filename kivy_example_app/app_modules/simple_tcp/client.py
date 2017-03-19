from sys import version_info
from threading import Thread
import socket
import sys
PY = version_info[0]
if PY == 3:
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty


class SimpleClient(object):
    active = False
    thread = None
    sock = None
    port = None
    ip = None
    queue = Queue()

    def connect(self, ip='localhost', port=9995):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.thread = Thread(target=self.recv_thread)
        self.thread.daemon = True
        self.thread.start()
        self.ip, self.port = ip, port
        self.on_connect()

    def disconnect(self):
        self.sock.send('')
        self.active = False

    def read_queue(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            pass

    def recv_thread(self):
        self.active = True
        while self.active:
            data = self.sock.recv(4096)
            if not data or data == b'':

                break
            if PY == 3:
                data = str(data, 'utf-8')
            self.queue.put(data)

        self.on_disconnect()

    def send(self, msg):
        if self.sock:
            if PY == 3:
                msg = bytes(msg, 'utf-8')
            self.sock.sendall(msg)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass
