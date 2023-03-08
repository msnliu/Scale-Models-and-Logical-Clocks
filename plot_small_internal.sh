#!/bin/bash

# This Bash script runs the `logical_clock.py` script with arguments 6 and 10, runs the `viz.py` script with a unique output path, clears all log files, and repeats the process 5 times. The script uses the `gtimeout` command to limit the execution time of `logical_clock.py` to 1 minute.

# Loop through 5 iterations of the process
for i in {1..5}; do
    # Print the current iteration number
    echo "Iteration $i"
    # Run `logical_clock.py` with arguments 6 and 10, and a timeout of 1 minute
    gtimeout 1m python3 logical_clock.py 6 5
    # Run `viz.py` with a unique output path based on the iteration number
    python viz.py output_internal_$i
    # Clear all log files
    rm -f *.log
done