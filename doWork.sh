#!/usr/bin/env bash

for condition in "condition1" "condition2" "condition3" "condition4" "condition5" "condition6" "condition7" "condition8" "condition9" "condition10"
do
    for time in {1..24}
    do
        mpirun -np 2 python ProbeSpace.py --out "Data/"$condition"/"$condition"_"$time".pkl" --condition $condition --time $time &
    done
done