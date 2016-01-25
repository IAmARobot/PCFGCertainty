#!/usr/bin/env bash

for alpha in .05 .1 .15 .2 .25 .3 .35 .4 .45 .5 .55 .6 .65 .7 .75 .8 .85 .9 .95 1
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
