#!/usr/bin/env bash

for alpha in .05 .10 .15 .20 .25 .30 .35 .40 .45 .50 .55 .60 .65 .70 .75 .80 .85 .90 .95 1
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
