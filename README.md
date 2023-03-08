# Introduction

This code implements a simple version of the Lamport clock algorithm using Python's multiprocessing and threading libraries. The Lamport clock is a logical clock algorithm that is used to order events in a distributed system. This code simulates a distributed system consisting of three virtual machines that communicate with each other over a network. Each virtual machine maintains a local logical clock, which is used to order the events that occur on that machine. The code records the messages sent and received by each machine, as well as the local clock values for each machine at different times.

# Requirements

* Python 3.x
* multiprocessing library
* threading library


# How to Run

Clone this repository to your local machine.
Open a terminal window and navigate to the root directory of the cloned repository.
Run the following command to start the simulation:

> $ python logical_clock.py 6 10

The code will start three virtual machines on ports 3 random ports between 2000 to 20000.6,10 here means the upperbound for the clock rates and Code for internal events respectively. Using a value smaller then 6 implies a smaller range of tick_rates. Using a value smaller than 10 means a lower probability of internal events(thus more send message happening) Each virtual machine will communicate with the others using the Lamport algorithm to synchronize their logical clocks.

# Implementation Details

* The LamportClock class represents a logical clock that can be used to synchronize events in a distributed system.

* The VirtualMachine class represents a virtual machine that can communicate with other virtual machines and has a logical clock to keep track of events. The run method of the VirtualMachine class is the main function that controls the behavior of the virtual machine. The virtual machine connects to other virtual machines using the connect method and sends messages using the send_message method. The virtual machine also receives messages using the receive_messages method.

* The init_machine function initializes the server-side logic on the virtual machine by setting up a socket to listen for incoming connections and starting a thread to handle incoming messages.

* The machine function creates and runs a virtual machine with the specified configuration and ID. It starts a thread to initialize the server-side logic on the virtual machine and another thread to run the virtual machine.

* In the main section of the code, three virtual machines are created with different configurations and started using Python's multiprocessing library. The join method is used to wait for all processes to complete.

# Output format

The code records the messages sent and received by each virtual machine, as well as the local clock values for each machine at different times. The output is saved in separate log files for each machine follow by their ids and lock rates (vm_0_1.log, vm_1_5.log, and vm_2_4.log).

The log files contain the following information:

Messages sent and received by the machine, along with the global time, the logical clock value of the sender, and the logical clock value of the receiver at the time the message was sent or received.
Internal events that occur on the machine, along with the global time and the logical clock value of the machine at the time the event occurred.

# Experiments

We have three bash files and viz.py to help us run the experiments required.

* viz.py: The code reads multiple log files in the current directory and extracts information such as logical clock values, queue lengths, and the jump in logical clock values between successive lines in each file. The code then plots the logical clock values, the jump values, and the queue lengths using Matplotlib.
* plot.sh In summary, this Bash script automates the process of running the logical_clock.py and viz.py scripts multiple times with different output paths, and clears the log files after each run. This can be useful for testing and analyzing the performance of the scripts under different conditions.
* plot_small_internal.sh &  plot_small_tickrate.sh: In summary, these Bash script are simiar to above except we run with different settings of probability of internal events and tick rates.

Note that we set running time be 1 min and run 5 fives for each bash, but you can play around with the parameter.

See different ourput folder for the results plot.

# Limitation 

This code implements a simple version of the Lamport clock algorithm and has a number of limitations. Some of the limitations are:

* The code assumes that the virtual machines are running on the same physical machine and communicate with each other over a network. In a real distributed system, the machines would be running on separate physical machines and communicate with each other over a network.
* The code does not implement any fault tolerance or error handling mechanisms. In a real distributed system, fault tolerance and error handling would be essential.
* The code does not implement any optimizations to reduce the number of messages exchanged between the machines. In a real distributed system, optimizing the message exchange is critical to performance.
# Contributors

* Guangya Wan
* Zongjun Liu