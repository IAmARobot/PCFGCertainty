#!/usr/bin/env bash

for alpha in .1 .2 .3 .4 .5 .6 .7 .8 .9 1
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
