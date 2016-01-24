#!/usr/bin/env bash

for alpha in .41 .42 .43 .44 .45 .46 .47 .48 .49
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
