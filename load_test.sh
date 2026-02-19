#!/bin/bash
# Sends random requests to your app to generate dashboard data
echo "Generating traffic... Press Ctrl+C to stop"
while true; do
    curl -s http://localhost:5000/health > /dev/null
    curl -s http://localhost:5000/metrics > /dev/null
    curl -s http://localhost:5000/simulate/error > /dev/null
    curl -s http://localhost:5000/simulate/slow > /dev/null
    sleep 0.5
done