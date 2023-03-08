from multiprocessing import Process
import os
import socket
import threading
import time
import random
import sys

class LamportClock:
    def __init__(self, tick_rate):
        self.time = 0
        self.lock = threading.Lock()
        self.tick_rate = tick_rate
    
    def increment(self):
        """Increment the clock by 1."""
        with self.lock:
            self.time += 1
    
    def update(self, other_time):
        """Update the clock with the maximum value of other_time and the current time."""
        with self.lock:
            self.time = max(self.time, other_time) + 1
    
    def get_time(self):
        """Get the current time on the clock."""
        with self.lock:
            return self.time
    
    def wait(self):
        """Wait for a certain amount of time based on the tick rate."""
        time.sleep(1/self.tick_rate)


class VirtualMachine:
    def __init__(self, config, idx):
        self.host = config[0]
        self.ports = config[3:]
        self.id = idx
        self.clock = LamportClock(random.randint(1, config[1]))
        self.internal_upper = config[2]
        self.queue = []
        self.log_file = open(f"vm_{self.id}_{self.clock.tick_rate}.log", "w")
    
    def receive_messages(self, conn):
        """Receive messages on a connection and add them to the message queue."""
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
        """Connect to the other machines on the specified ports."""
        sockets = []
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, p))
            sockets.append(s) 
        return sockets
    
    def send_message(self, conn):
        """Send a message on the specified connection and update the clock."""
        # Get the current time from the logical clock
        time_val = self.clock.get_time()
        # Format the message to include the sender's ID and logical clock value
        message = f"{self.id},{time_val}"
        # Send the message on the connection
        conn.send(message.encode('ascii'))
        # Increment the logical clock
        self.clock.increment()
        # Log the sent message
        self.log_file.write(f"Machine {self.id} Sent message {message} at global time {time.time()} with current logical clock: {self.clock.get_time()}\n")
        self.log_file.flush()
    
    def run(self,ports):
        """Run the virtual machine."""
        sockets = self.connect(ports)
        while True:
            if len(self.queue) > 0:
                # If there are messages in the queue, process them
                data_val, time_val = self.queue.pop(0)
                self.clock.update(int(time_val))
                self.log_file.write(f"Machine {self.id} received message from Machine {data_val} whose logical clock time when sending the message is {time_val} at global time {time.time()}. Current logical clock: {self.clock.get_time()} with current queue length: {len(self.queue)}\n")
                self.log_file.flush()
            else:
                # Otherwise, randomly send a message, wait, or increment the clock
                rand_val = random.randint(1,self.internal_upper)
                if rand_val == 1:
                    self.send_message(sockets[0])
                elif rand_val == 2:
                    self.send_message(sockets[1])
                elif rand_val == 3:
                    # If rand_val is 3, send a message to the first machine, wait for a fixed amount of time, and then send a message to the second machine
                    self.send_message(sockets[0])
                    self.clock.wait()
                    self.send_message(sockets[1])
                else:
                    # If rand_val is greater than 3, increment the clock and log an internal event
                    self.clock.increment()
                    self.log_file.write(f"Machine {self.id} internal event at global time {time.time()} with current logical lock: {self.clock.get_time()}\n")
                    self.log_file.flush()
        # Wait for a certain amount of time based on the tick rate
            self.clock.wait()
def init_machine(vm):
    """Initialize the server-side logic on the virtual machine."""
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
    """Create and run a virtual machine with the specified configuration and ID."""
    vm = VirtualMachine(config, idx)
    init_thread = threading.Thread(target=init_machine, args=(vm,))
    init_thread.start()
    # Add a delay to initialize the server-side logic on all processes
    time.sleep(1)
    # Extensible to multiple producers
    prod_thread = threading.Thread(target=vm.run, args=(config[4:],))
    prod_thread.start()


if __name__ == '__main__':
    # Set up the configurations for the virtual machines
    clock_rate_upper,internal_event_upper = int(sys.argv[1]),int(sys.argv[2])
    localHost = "127.0.0.1"
    integers = list(range(2000, 20001))

# Choose three random integers from the list without repeating
    random_integers = random.sample(integers, k=3)
    port1 = random_integers[0]
    port2 = random_integers[1]
    port3 = random_integers[2]
    # Create and start a process for each virtual machine
    config1 = [localHost, clock_rate_upper,internal_event_upper,port1, port2, port3]
    p1 = Process(target=machine, args=(config1, 0))
    config2 = [localHost, clock_rate_upper,internal_event_upper,port2,port3, port1]
    p2 = Process(target=machine, args=(config2, 1))
    config3 = [localHost, clock_rate_upper,internal_event_upper,port3,port1, port2 ]
    p3 = Process(target=machine, args=(config3, 2))

    # Wait for all processes to complete

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()




