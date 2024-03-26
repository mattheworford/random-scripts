#!/bin/bash

# Prompt for private key
echo "Enter private key (in PEM format):"
read -r private_key

# Prompt for message
echo "Enter message to be encrypted:"
read -r message

# Encrypt message
encrypted=$(echo -n "$message" | openssl pkeyutl -encrypt -inkey <(echo "$private_key") -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 | base64)

# Print JWE
echo "JWE Encoded Message:"
jq -n --arg encrypted "$encrypted" '{"protected": "", "unprotected": "", "iv": "", "ciphertext": $encrypted, "tag": ""}'
