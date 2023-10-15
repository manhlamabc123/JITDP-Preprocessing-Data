#!/bin/bash

# Specify the directory you want to search
root_directory="/home/manh/Documents/Data/tan-dataset-new/divided_data"

# List of folder names to process
details=("part_1" "part_2" "part_3" "part_4" "part_5")

# Use the find command to list all directories under the root directory
# -type d: indicates we're looking for directories
# -maxdepth 1: limits the search to only one level (i.e., immediate subdirectories)
for folder in $(find "$root_directory" -type d -maxdepth 1); do
    # Extract and print just the folder name
    folder_name=$(basename "$folder")
    echo "$folder_name"

    # Check if the folder_name is in the list of details to process
    for detail in "${details[@]}"; do

        echo "Processing $detail"

        bash preprocess.sh $folder_name $detail

    done

done
