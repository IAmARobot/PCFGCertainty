#!/usr/bin/env bash

for beta in .5 1 1.5 2 2.5 3 3.5 4 4.5 5
do
    mpirun -np 2 python BestFit.py --alpha $1 --beta $beta &
done
