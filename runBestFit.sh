#!/usr/bin/env bash

for alpha in .7 .8 .9 1
do
    mpirun python BestFit.py --alpha $alpha &
done
