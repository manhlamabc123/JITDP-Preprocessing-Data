#!/bin/bash

python merge.py \
    -project $1 \
    -details "part_1" "part_2" "part_3" "part_4"

python merge.py \
    -project $1 \
    -details "part_3" "part_4"