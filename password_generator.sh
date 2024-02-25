#!/bin/bash

# Function to generate a random password
generate_password() {
  local length=$1
  LC_ALL=C tr -dc 'A-Za-z0-9!@#$%^&*()_+{}[]' </dev/urandom | head -c "$length"
}

# Prompt the user to enter the length of the password
read -r -p "Enter the length of the password: " password_length

# Call the function and store the generated password
password=$(generate_password "$password_length")

# Print the generated password
echo "Generated password: $password"
