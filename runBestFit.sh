#!/usr/bin/env bash

for alpha in .64 .645 .65 .655 .66
do
    mpirun python BestFit.py --alpha $alpha &
done
