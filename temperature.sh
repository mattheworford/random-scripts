#!/bin/bash

# Check if osx-cpu-temp is installed
if ! command -v osx-cpu-temp &> /dev/null; then
    echo "osx-cpu-temp could not be found. Please install it using Homebrew with the command 'brew install osx-cpu-temp'."
    exit
fi

# Get the CPU temperature in Celsius
TEMP_C=$(osx-cpu-temp | grep -o '[0-9]*\.[0-9]*')

# Convert the temperature to Fahrenheit
TEMP_F=$(echo "$TEMP_C * 9/5 + 32" | bc)

echo $TEMP_F F