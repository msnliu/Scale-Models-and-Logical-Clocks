import re
import os
import matplotlib.pyplot as plt
import sys

# Initialize an empty list to store the logical clock values from all files
all_logical_clock_values = []
machine_ids = []
tick_rates = []
all_jump_values = []
all_queue_lengths = []
# Loop through each file in the directory
for filename in os.listdir('.'):
    jump_values = []
    prev_logical_clock_value = None
    queue_lengths = []
    if filename.endswith('.log'):
        # Initialize an empty list to store the logical clock values from this file
        logical_clock_values = []
        machine_id = filename.split('_')[1]
        machine_ids.append(machine_id)
        tick_rate = filename.split('_')[2].split('.')[0]
        tick_rates.append(tick_rate)
        # Open the file for reading
        with open(filename, 'r') as f:
            # Loop through each line in the file
            for line in f:
                # Use a regular expression to find the current logical clock value in each line
                match = re.search(r'current logical clock: (\d+)', line)
                match2 = re.search(r'current queue length: (\d+)', line)
                if match:
                    # If a match is found, extract the value and append it to the list
                    logical_clock_value = int(match.group(1))
                    if prev_logical_clock_value is not None:
                        jump = logical_clock_value - prev_logical_clock_value
                        jump_values.append(jump)
                    # Update the previous value with the current value
                    prev_logical_clock_value = logical_clock_value
                    logical_clock_values.append(logical_clock_value)
                if(match2):
                    queue_value = int(match2.group(1))
                    queue_lengths.append(queue_value)

        # Append the logical clock values from this file to the list of all values
        all_logical_clock_values.append(logical_clock_values)
        all_jump_values.append(jump_values)
        all_queue_lengths.append(queue_lengths)
# Plot the logical clock values from all files using matplotlib
if __name__ == '__main__':
    output_dir = sys.argv[1]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.figure()
    for i, logical_clock_values in enumerate(all_logical_clock_values):
        plt.plot(logical_clock_values, label=f'Machine: {machine_ids[i]} with tick rates {tick_rates[i]}')
    plt.xlabel('Number of Instructions')
    plt.ylabel('Logical Clock Value')
    plt.legend()
    plt.savefig(output_dir+'/clock.png')

    plt.figure()
    for i, logical_clock_values in enumerate(all_jump_values):
        plt.plot(logical_clock_values, label=f'Machine: {machine_ids[i]} with tick rates {tick_rates[i]}')

    plt.xlabel('Number of Instructions')
    plt.ylabel('Jump in Logical Clock Value')
    plt.legend()
    plt.savefig(output_dir+'/jump.png')
    plt.figure()
    plt.boxplot(all_queue_lengths, labels = [f'Tick rates {tick_rates[i]}' for i in range(3)])
    plt.xlabel('Machine')
    plt.ylabel('Message Queue Length')
    plt.savefig(output_dir+'/queue.png')