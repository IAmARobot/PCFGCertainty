#!/usr/bin/env bash

for alpha in .01 .02 .03 .04 .05 .06 .07 .08 .09 .10 .11 .12 .13 .14 .15 .16 .17 .18 .19 .20
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
