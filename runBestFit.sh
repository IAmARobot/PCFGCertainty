#!/usr/bin/env bash

for alpha in .60 .605 .610 .620 .625 .630 .635 .640 .645 .650 .655 .660 .665 .670 .675 .680 .685 .690
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
