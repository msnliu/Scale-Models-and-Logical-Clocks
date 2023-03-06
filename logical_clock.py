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
        # Wait for a certain amount of time based on the tick rate
        time.sleep(1/self.tick_rate)
class VirtualMachine:
    def __init__(self, config, idx):
        self.host = config[0]
        self.ports = config[1:]
        self.id = idx
        self.clock = LamportClock(random.randint(1, 6))
        self.queue = []
        self.log_file = open(f"vm_{self.id}.log", "w")
    def receive_messages(self, conn):
        # Log the connection
        print(f"Connected to {conn.getpeername()}\n")
        while True:
            # Receive a message on this connection
            data = conn.recv(1024)
            if not data:
                break
            data_val, time_val = data.decode('ascii').split(",")
            # Add the received message to the local message queue
            self.queue.append((data_val, int(time_val)))
    def connect(self,ports):
        sockets = []
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, p))
            sockets.append(s) 
        return sockets
    def send_message(self, conn):
        # Get the current time from the logical clock
        time_val = self.clock.get_time()
        # Format the message to include the sender's ID and logical clock value
        message = f"{self.id},{time_val}"
        # Send the message on the connection
        conn.send(message.encode('ascii'))
        # Increment the logical clock
        self.clock.increment()
        # Log the sent message
        self.log_file.write(f"Machine {self.id} Sent message {message} at global time {time.time()} with current logical clock {time_val}\n")
        self.log_file.flush()
    def run(self,ports):
        sockets = self.connect(ports)
        while True:
            if len(self.queue) > 0:
                data_val, time_val = self.queue.pop(0)
                self.clock.update(int(time_val))
                self.log_file.write(f"Machine {self.id} received message from Machine {data_val} at global time {time.time()} with current logical clock {time_val} with current queue length : {len(self.queue)} \n")
                self.log_file.flush()
            else:
                rand_val = random.randint(1, 10)
                if rand_val == 1:
                    self.send_message(sockets[0])
                elif rand_val == 2:
                    self.send_message(sockets[1])
                elif rand_val == 3:
                    self.send_message(sockets[0])
                    self.clock.wait()
                    self.send_message(sockets[1])
                else:
                    self.clock.increment()
                    self.log_file.write(f"Machine {self.id} internal event at global time {time.time()} with logical clock updated {self.clock.get_time()}\n")
                    self.log_file.flush()
            self.clock.wait()
def init_machine(vm):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(vm.ports[0])
    HOST = str(vm.host)
    print(f"Starting server on port {PORT}")
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=vm.receive_messages, args=(conn,)).start()
        print(f"Connection accepted for vm {vm.id} at global time {time.time()} with logical clock {vm.clock.get_time()}\n")
def machine(config, idx):
    vm = VirtualMachine(config, idx)
    init_thread = threading.Thread(target=init_machine, args=(vm,))
    init_thread.start()
    # Add a delay to initialize the server-side logic on all processes
    time.sleep(1)
    # Extensible to multiple producers
    prod_thread = threading.Thread(target=vm.run, args=(config[2:],))
    prod_thread.start()
if __name__ == '__main__':
    localHost = "127.0.0.1"
    port1 = 2050
    port2 = 3050
    port3 = 4050
    config1 = [localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1, 0))
    config2 = [localHost, port2,port3, port1]
    p2 = Process(target=machine, args=(config2, 1))
    config3 = [localHost, port3,port1, port2 ]
    p3 = Process(target=machine, args=(config3, 2))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()




