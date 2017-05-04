#!/usr/bin/env bash

for condition in 1 2 3 4 5 6 7 8 9 10
do
    for time in {0..23}
    do
        mpirun -np 2 python ProbeSpace.py --out "Data/"$condition"/"$condition"_"$time".pkl" --condition $condition --time $time &
    done
done