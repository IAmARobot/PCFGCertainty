mkdir Data/$1
for time in {1..23}
do
    mpirun -np 2 python ProbeSpace.py --out "Data/"$1"/"$1"_"$time".pkl" --condition $1 --time $time &
done
mpirun -np 2 python ProbeSpace.py --out "Data/"$1"/"$1"_24.pkl" --condition $1 --time 24
