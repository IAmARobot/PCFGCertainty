#!/usr/bin/env bash

for alpha in .67 .68 .69
do
    mpirun python BestFit.py --alpha $alpha &
done
