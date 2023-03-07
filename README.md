# Introduction

This code implements a simple version of the Lamport clock algorithm using Python's multiprocessing and threading libraries. The Lamport clock is a logical clock algorithm that is used to order events in a distributed system. This code simulates a distributed system consisting of three virtual machines that communicate with each other over a network. Each virtual machine maintains a local logical clock, which is used to order the events that occur on that machine. The code records the messages sent and received by each machine, as well as the local clock values for each machine at different times.

# Requirements

Python 3.x
multiprocessing library
threading library


# How to Run

Clone this repository to your local machine.
Open a terminal window and navigate to the root directory of the cloned repository.
Run the following command to start the simulation:

> $ python logical_clock.py

The code will start three virtual machines on ports 2050, 3050, and 4050. Each virtual machine will communicate with the others using the Lamport algorithm to synchronize their logical clocks.

# Implementation Details
Each virtual machine is implemented as a separate process and runs on its own port. When a virtual machine receives a message from another virtual machine, it updates its logical clock based on the time stamp in the message. If a virtual machine has no messages to process, it generates an internal event and updates its logical clock accordingly.

The Lamport logical clock algorithm is implemented in the LamportClock class. Each virtual machine is represented by the VirtualMachine class. The init_machine function sets up the server-side logic for each virtual machine. The machine function initializes each virtual machine and starts the server-side and client-side logic.

# Output format

The code records the messages sent and received by each virtual machine, as well as the local clock values for each machine at different times. The output is saved in separate log files for each machine (vm_0.log, vm_1.log, and vm_2.log).

The log files contain the following information:

Messages sent and received by the machine, along with the global time, the logical clock value of the sender, and the logical clock value of the receiver at the time the message was sent or received.
Internal events that occur on the machine, along with the global time and the logical clock value of the machine at the time the event occurred.

# Limitation 

This code implements a simple version of the Lamport clock algorithm and has a number of limitations. Some of the limitations are:

The code assumes that the virtual machines are running on the same physical machine and communicate with each other over a network. In a real distributed system, the machines would be running on separate physical machines and communicate with each other over a network.
The code does not implement any fault tolerance or error handling mechanisms. In a real distributed system, fault tolerance and error handling would be essential.
The code does not implement any optimizations to reduce the number of messages exchanged between the machines. In a real distributed system, optimizing the message exchange is critical to performance.

# License
This code is licensed under the MIT License. See the LICENSE file for details.

# Contributors

Guangya Wan
Zongjun Liu