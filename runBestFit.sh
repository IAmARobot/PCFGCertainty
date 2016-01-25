#!/usr/bin/env bash

for alpha in .441 .442 .443 .444 .445 .446 .447 .448 .449 .450 .451 .452 .453 .454 .455 .456 .457 .458 .459 .460
do
    mpirun -np 2 python BestFit.py --alpha $alpha &
done
