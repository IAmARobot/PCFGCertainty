#!/usr/bin/env bash
rm modelDataStudy1.csv
rm modelDataStudy2.csv
rm modelDataStudy3.csv
rm modelDataStudy4.csv

for condition in 1 2 3 4 5 6 7 8 9 10
do
    # Original
    mpirun python CertaintyAnalysis.py --alpha .640 --beta 0 --condition $condition --input Study1Counts.csv --output modelDataStudy1.csv &

    # One Shot
    mpirun python CertaintyAnalysis.py --alpha .655 --beta .066 -s --condition $condition --input Study2Counts.csv --output modelDataStudy2.csv &

    # Trial Certainty
    mpirun python CertaintyAnalysis.py --alpha .660 --beta 0 --condition $condition --input Study3Counts.csv --output modelDataStudy3.csv &

    # Continuous
    mpirun python CertaintyAnalysis.py --alpha .660 --beta 0 --condition $condition --input Study4Counts.csv --output modelDataStudy4.csv &
done