#!/usr/bin/env bash

for alpha in .51 .52 .53 .54 .55 .56 .57 .58 .59 .61 .62 .63 .64 .65 .66 .67 .68 .69
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
