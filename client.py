import datetime
import os
import socket
import time
from threading import Thread

import psutil
import win32gui



class Metrics:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.value = None
        self.is_running = False

    def start_collect(self):
        self.is_running = True
        while self.is_running:
            self.value = self.func()

    def get_current_state(self):
        return self.name, self.value

    def cleanup(self):
        self.value = None

    def stop_collect(self):
        self.is_running = False


metrics1 = Metrics("Mouse position", win32gui.GetCursorInfo)
metrics2 = Metrics("Used memory", psutil.Process(os.getpid()).memory_percent)

t1 = Thread(target=metrics1.start_collect)
t2 = Thread(target=metrics2.start_collect)

t1.start()
t2.start()

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))
    data = f"Time: {datetime.datetime.now().time()}\n"
    name, value = metrics1.get_current_state()
    data += f"{name} {value[2][0]},{value[2][1]}\n"
    name,value=metrics2.get_current_state()
    data += f"{name} {value*100:.2f}%\n"
    print(f"try to send: \n{data}")
    sock.send(data.encode('utf-8'))
    sock.close()
    time.sleep(15)