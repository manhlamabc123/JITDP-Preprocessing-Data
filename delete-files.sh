#!/bin/bash

# Specify the directory you want to search
root_directory="/home/manh/Documents/Data/splited-tan-dataset"

# Use the find command to list all directories under the root directory
# -type d: indicates we're looking for directories
# -maxdepth 1: limits the search to only one level (i.e., immediate subdirectories)
for folder in $(find "$root_directory" -maxdepth 1 -type d); do
    # Extract and print just the folder name
    folder_name=$(basename "$folder")
    echo "$folder_name"

    # Change the working directory to the current folder
    cd "$folder"

    # Perform the desired operations in this directory
    find . -type f ! -name "*part*" -exec rm {} \;
    mkdir features
    mv *.csv features/

    # Return to the root directory for the next iteration
    cd "$root_directory"
done
