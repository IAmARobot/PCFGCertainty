#!/usr/bin/env bash
mkdir Data/$1

for alpha in .1 .2 .3 .4 .5 .6 .7 .8 .9
do
    python CertaintyAnalysis.py --read "Data/"$1"/" --write "Data/"$1"/"$1"_"$alpha".csv" --condition $1 --alpha $alpha &
done