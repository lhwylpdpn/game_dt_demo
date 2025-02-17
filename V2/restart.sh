#!/bin/bash

pid=$(ps -ef | grep 'python3 -u demo_main.py' | grep -v 'grep' | awk '{print $2}')
if [ -n "$pid" ]; then
    echo "Killing process with PID $pid..."
    kill -9 $pid
else
    echo "No matching process found to kill."
fi

echo "Starting new process with nohup..."
nohup python3 -u demo_main.py &
