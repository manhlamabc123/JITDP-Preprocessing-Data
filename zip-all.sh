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

    # Skip the 'php-src' folder
    if [ "$folder_name" == "php-src" ]; then
        continue
    fi

    # Return to the root directory for the next iteration
    cd "$root_directory"

    # Zip the folder_name
    zip -r "$folder_name.zip" "$folder_name"

    # Return to the root directory for the next iteration
    cd "$root_directory"
done
