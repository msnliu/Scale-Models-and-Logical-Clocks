from multiprocessing import Process
import os
import socket
import threading
import time
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
    def __init__(self, config, idx):
        self.host = config[0]
        self.ports = config[1:]
        self.id = idx
        self.clock = LamportClock(random.randint(1, 6))
        self.queue = []
        self.log_file = open(f"vm_{self.id}.log", "w")
    
    def connect(self):
        for port in self.ports:
            if port != self.ports[self.id]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, port))
                threading.Thread(target=self.receive_messages, args=(s,)).start()
    
    def receive_messages(self, conn):
        print(f"Connected to {conn.getpeername()}\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_val, time_val = data.decode('ascii').split(",")
            self.queue.append((data_val, int(time_val)))
            self.log_file.write(f"Received message {data_val} at global time {time.time()} with logical clock {time_val}\n")
            self.log_file.flush()
            self.clock.update(int(time_val))
    
    def send_message(self, conn):
        code_val = str(self.id)
        time_val = self.clock.get_time()
        message = f"{code_val},{time_val}"
        conn.send(message.encode('ascii'))
        self.log_file.write(f"Sent message {message} at global time {time.time()} with logical clock {time_val}\n")
        self.log_file.flush()
        self.clock.increment()
    
    def run(self):
        self.connect()
        while True:
            if len(self.queue) > 0:
                data_val, time_val = self.queue.pop(0)
                self.log_file.write(f"Processed message {data_val} at global time {time.time()} with logical clock {time_val}\n")
                self.log_file.flush()
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
                    self.log_file.write(f"Internal event at global time {time.time()} with logical clock {self.clock.get_time()}\n")
                    self.log_file.flush()
            self.clock.wait()
            
    def get_connection(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, port))
        return s

def init_machine(vm):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(vm.ports[vm.id])
    HOST = str(vm.host)
    print(f"Starting server on port {PORT}")
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=vm.receive_messages, args=(conn,)).start()
        vm.log_file.write(f"Connection accepted at global time {time.time()} with logical clock {vm.clock.get_time()}\n")
        vm.log_file.flush()

def machine(config, idx):
    vm = VirtualMachine(config, idx)
    init_thread = threading.Thread(target=init_machine, args=(vm,))
    init_thread.start()
    # Add a delay to initialize the server-side logic on all processes
    vm.clock.wait()
    # Extensible to multiple producers
    prod_thread = threading.Thread(target=vm.run)
    prod_thread.start()

if __name__ == '__main__':
    localHost = "127.0.0.1"
    port1 = 2056
    port2 = 3056
    port3 = 4056
    config1 = [localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1, 0))
    config2 = [localHost, port1, port2, port3]
    p2 = Process(target=machine, args=(config2, 1))
    config3 = [localHost, port1, port2, port3]
    p3 = Process(target=machine, args=(config3, 2))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()




