#!/usr/bin/env bash
rm modelData.csv

for condition in 1 2 3 4 5 6 7 8 9 10
do
    mpirun -np 2 python CertaintyAnalysis.py --condition $condition &
done