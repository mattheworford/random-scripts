#!/bin/bash

# This script generates and prints a random password of a given length.
# It prompts the user to enter the length of the password and then generates a
# random string of the following characters: A-Z, a-z, 0-9, and the following
# special characters: !@#$%^&*()_+{}[].
# To run this script, make the file executable with 'chmod +x
# password_generator.sh', and then run it with './password_generator.sh'.

generate_password() {
  local length=$1
  LC_ALL=C tr -dc 'A-Za-z0-9!@#$%^&*()_+{}[]' </dev/urandom | head -c "$length"
}

read -r -p "Enter the length of the password: " password_length

password=$(generate_password "$password_length")

echo "Generated password: $password"
