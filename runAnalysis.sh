#!/usr/bin/env bash
rm Data/allConditions.csv

for condition in "condition1" "condition2" "condition3" "condition4" "condition5" "condition6" "condition7" "condition8" "condition9" "condition10"
do
    mpirun -np 2 python CertaintyAnalysis.py --read "Data/"$condition"/" --write "Data/allConditions.csv" --condition $condition &
done