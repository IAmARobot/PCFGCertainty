#!/usr/bin/env bash
rm modelData.csv

for condition in 1 2 3 4 5 6 7 8 9 10
do
    # Original
    mpirun -np 2 python CertaintyAnalysis.py --alpha .64 --beta 0 --condition $condition &

    # One Shot
    #mpirun -np 2 python CertaintyAnalysis.py --alpha .65 --beta .06 -s --condition $condition &

    # Trial Certainty
    #mpirun -np 2 python CertaintyAnalysis.py --alpha .64 --beta 0 --condition $condition &
done