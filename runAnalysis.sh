#!/usr/bin/env bash
rm modelDataStudy1.csv
rm modelDataStudy2.csv
rm modelDataStudy3.csv

for condition in 1 2 3 4 5 6 7 8 9 10
do
    # Original
    mpirun -np 2 python CertaintyAnalysis.py --alpha .64 --beta 0 --condition $condition --input Study1Counts.csv --output modelDataStudy1.csv

    # One Shot
    mpirun -np 2 python CertaintyAnalysis.py --alpha .65 --beta .06 -s --condition $condition --input Study2Counts.csv --output modelDataStudy2.csv

    # Trial Certainty
    mpirun -np 2 python CertaintyAnalysis.py --alpha .64 --beta 0 --condition $condition --input Study3Counts.csv --output modelDataStudy3.csv &
done