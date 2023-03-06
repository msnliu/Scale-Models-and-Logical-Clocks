# Lamport Logical Clock

This is an implementation of the Lamport Logical Clock algorithm for distributed systems in Python. The code simulates a group of virtual machines that communicate with each other over sockets and use the Lamport algorithm to keep track of their logical clocks.

# Requirements
Python 3.7 or higher

multiprocessing, socket module

# How to Run

Clone this repository to your local machine.
Open a terminal window and navigate to the root directory of the cloned repository.
Run the following command to start the simulation:

> $ python logical_clock.py

The code will start three virtual machines on ports 2050, 3050, and 4050. Each virtual machine will communicate with the others using the Lamport algorithm to synchronize their logical clocks.

# Implementation Details
Each virtual machine is implemented as a separate process and runs on its own port. When a virtual machine receives a message from another virtual machine, it updates its logical clock based on the time stamp in the message. If a virtual machine has no messages to process, it generates an internal event and updates its logical clock accordingly.

The Lamport logical clock algorithm is implemented in the LamportClock class. Each virtual machine is represented by the VirtualMachine class. The init_machine function sets up the server-side logic for each virtual machine. The machine function initializes each virtual machine and starts the server-side and client-side logic.

# License
This code is licensed under the MIT License. See the LICENSE file for details.

# Contributors

Guangya Wan
Zongjun Liu