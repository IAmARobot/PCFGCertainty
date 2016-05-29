#!/usr/bin/env bash

for alpha in .65 .66 .67 .68 .69 .7 .71 .72 .73 .74 .75 .76 .77 .78 .79
do
    mpirun -np 2 python BestFit.py -s --alpha $alpha &
done
