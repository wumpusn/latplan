#!/bin/bash -x

set -e

parallel -j 4 python3 ::: \
         ./counter_*.py \
         ./digital_lightsout*.py \
         ./hanoi.py

for py in ./puzzle_*.py ; do
    $py
done


