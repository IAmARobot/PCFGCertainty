#!/usr/bin/env bash
mkdir Data/$1
rm Data/allConditions.csv

for condition in "condition1" "condition2" "condition3" "condition4" "condition5" "condition6" "condition7" "condition8" "condition9" "condition10"
do
    for alpha in .1 .2 .3 .4 .5 .6 .7 .8 .9
    do
        python CertaintyAnalysis.py --read "Data/"$condition"/" --write "Data/allConditions.csv" --condition $condition --alpha $alpha &
    done
done