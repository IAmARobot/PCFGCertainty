#!/usr/bin/env bash

for condition in "condition1" "condition2" "condition3" "condition4" "condition5" "condition6" "condition7" "condition8" "condition9" "condition10"
do
    for time in {1..23}
    do
        mpirun -np 2 python ProbeSpace.py --out "Data/"$condition"/"$condition"_"$time".pkl" --condition $condition --time $time &
    done

    mpirun -np 2 python ProbeSpace.py --out "Data/"$condition"/"$condition"_24.pkl" --condition $condition --time 24
done

rm Data/allConditions.csv

for condition in "condition1" "condition2" "condition3" "condition4" "condition5" "condition6" "condition7" "condition8" "condition9" "condition10"
do
    python CertaintyAnalysis.py --read "Data/"$condition"/" --write "Data/allConditions.csv" --condition $condition &
done