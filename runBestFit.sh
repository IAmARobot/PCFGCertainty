#!/usr/bin/env bash

for alpha in .401 .402 .403 .404 .405 .406 .407 .408 .409 .410 .411 .412 .413 .414 .415 .416 .417 .418 .419 .420
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
