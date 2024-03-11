#!/bin/bash

# This script organizes files in a specified directory into subdirectories based on their file extensions.
# It creates four subdirectories: Images, Documents, Videos, and Others.
# Files with extensions jpg, jpeg, png, and gif are moved to Images.
# Files with extensions pdf, doc, docx, and txt are moved to Documents.
# Files with extensions mp4, mkv, avi, and mov are moved to Videos.
# All other files are moved to Others.
#
# To run this script, open a terminal and navigate to the directory containing the script.
# Then, run the script by typing `./file_organizer.sh`.
# You may need to make the script executable by running `chmod +x file_organizer.sh` before you can run it.

create_directory() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
  fi
}

move_file() {
  mv "$1" "$2" 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "Moved $1 to $2"
  else
    echo "Failed to move $1"
  fi
}

organize_files() {
  create_directory "Images"
  create_directory "Documents"
  create_directory "Videos"
  create_directory "Others"

  for file in *; do
    if [ -f "$file" ]; then
      extension="${file##*.}"

      case "$extension" in
      jpg | jpeg | png | gif)
        move_file "$file" "Images/"
        ;;
      pdf | doc | docx | txt)
        move_file "$file" "Documents/"
        ;;
      mp4 | mkv | avi | mov)
        move_file "$file" "Videos/"
        ;;
      *)
        move_file "$file" "Others/"
        ;;
      esac
    fi
  done
  echo "Files organized."
}

main() {
  echo "Enter the directory to organize:"
  read -r directory

  if [ ! -d "$directory" ]; then
    echo "Directory not found."
    exit 1
  fi

  cd "$directory" || exit

  organize_files
}

main
