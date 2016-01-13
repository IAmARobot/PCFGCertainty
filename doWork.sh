#!/usr/bin/env bash
mkdir Data/$1

for alpha in .1 .2 .3 .4 .5 .6 .7 .8 .9
for time in {1..23}
do
    mpirun -np 2 python ProbeSpace.py --out "Data/"$1"/"$1"_"$time"_"$alpha".pkl" --condition $1 --time $time --alpha $alpha &
done

mpirun -np 2 python ProbeSpace.py --out "Data/"$1"/"$1"_24.pkl" --condition $1 --time 24 --alpha $alpha

done