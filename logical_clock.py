from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random

class LamportClock:
    def __init__(self, tick_rate):
        self.time = 0
        self.lock = threading.Lock()
        self.tick_rate = tick_rate
    
    def increment(self):
        with self.lock:
            self.time += 1
    
    def update(self, other_time):
        with self.lock:
            self.time = max(self.time, other_time) + 1
    
    def get_time(self):
        with self.lock:
            return self.time
    
    def wait(self):
        time.sleep(1/self.tick_rate)

class VirtualMachine:
    def __init__(self, config,idx):
        self.host = config[0]
        self.ports = config[1:]
        self.id = idx
        self.clock = LamportClock(random.randint(1, 6))
        self.queue = []
        self.log_file = open("vm_" + str(self.id) + ".log", "w")
    
    def connect(self):
        for port in self.ports:
            if port != self.ports[self.id]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # print(self.host)
                # print(port)
                s.connect((self.host, port))
                start_new_thread(self.receive_messages, (s,))
    
    def receive_messages(self, conn):
        print("consumer accepted connection" + str(conn) + "\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_val, time_val = data.decode('ascii').split(",")
            self.queue.append((data_val, int(time_val)))
            self.log_file.write("Received message " + data_val + " at global time " + str(time.time()) + " with logical clock " + str(time_val) + "\n")
            self.clock.update(int(time_val))
    
    def send_message(self, conn):
        code_val = str(self.id)
        time_val = self.clock.get_time()
        message = code_val + "," + str(time_val)
        conn.send(message.encode('ascii'))
        self.log_file.write("Sent message " + str(message) + " at global time " + str(time.time()) + " with logical clock " + str(time_val) + "\n")
        self.clock.increment()
    
    def run(self):
        self.connect()
        while True:
            if len(self.queue) > 0:
                data_val, time_val = self.queue.pop(0)
                self.log_file.write("Processed message " + data_val + " at global time " + str(time.time()) + " with logical clock " + str(time_val) + "\n")
                self.clock.update(int(time_val))
            else:
                rand_val = random.randint(1, 10)
                if rand_val == 1:
                    self.send_message(self.get_connection(self.ports[(self.id % 3) - 1]))
                elif rand_val == 2:
                    self.send_message(self.get_connection(self.ports[(self.id + 1) % 3]))
                elif rand_val == 3:
                    self.send_message(self.get_connection(self.ports[(self.id % 3) - 1]))
                    self.send_message(self.get_connection(self.ports[(self.id + 1) % 3]))
                else:
                    self.clock.increment()
                    self.log_file.write("Internal event at global time " + str(time.time()) + " with logical clock " + str(self.clock.get_time()) + "\n")
            self.clock.wait()
            
    def get_connection(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, port))
        return s

def init_machine(vm):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(vm.ports[vm.id])
    HOST = str(vm.host)
    print("starting server| port val:", PORT)
    s.bind((HOST,PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(vm.receive_messages, (conn,))
        vm.log_file.write("Connection accepted at global time " + str(time.time()) + " with logical clock " + str(vm.clock.get_time()) + "\n")
def machine(config,idx):
    vm = VirtualMachine(config, idx)
    log_file = vm.log_file
    global code
    # print(config)
    init_thread = Thread(target=init_machine, args=(vm,))
    init_thread.start()
    # add delay to initialize the server-side logic on all processes
    vm.clock.wait()
    # extensible to multiple producers
    prod_thread = Thread(target=vm.run, )
    prod_thread.start()


if __name__ == '__main__':
    localHost= "127.0.0.1"
    port1 = 2056
    port2 = 3056
    port3 = 4056
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1, 0))
    config2=[localHost, port1,port2, port3]
    p2 = Process(target=machine, args=(config2, 1))
    config3=[localHost, port1, port2,port3]
    p3 = Process(target=machine, args=(config3, 2))
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


