#!/bin/bash

# This script is designed to fetch the CPU temperature on a macOS system and output it in Fahrenheit.
# To run this script, make the file executable with 'chmod +x temperature.sh', and then run it with './temperature.sh'.

if ! command -v osx-cpu-temp &>/dev/null; then
    echo "osx-cpu-temp could not be found. Please install it using Homebrew with the command 'brew install osx-cpu-temp'."
    exit
fi

TEMP_C=$(osx-cpu-temp | grep -o '[0-9]*\.[0-9]*')

TEMP_F=$(echo "$TEMP_C * 9/5 + 32" | bc)

echo "$TEMP_F" F
