#!/bin/bash

#SBATCH -N 1
#SBATCH --partition=genoa
#SBATCH --ntasks-per-node=32
#SBATCH --job-name=1010
#SBATCH --time=24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-type=ALL
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out
#SBATCH --mail-user=a.k.dixit@utwente.nl

source ~/.bash_shell

MAXlevel="9"
Oh=("1.00E-03" "3.00E-03" "6.00E-03" "1.00E-02" "3.00E-02" "6.00E-02" "1.00E-01")
Bo="0.001"
tmax="200"
start_data=1010

start=1015
end=1016

for (( i=start; i<=end; i++ )); do
    index=$((i - start_data))
    dir=$i
    
    cd $dir || { echo "Failed to change directory to $dir"; exit 1; }
    
    srun -n 16 --gres=cpu:16 --exclusive bubbleinSheet_01 $MAXlevel ${Oh[index]} $Bo $tmax &
    
    cd ../
done

wait

#CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 bubbleinSheet_01.c -o bubbleinSheet_01 -lm -disable-dimensions
#CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 asyBubbleinSheet_01.c -o asyBubbleinSheet_01 -lm -disable-dimensions
#srun -n 96 asyBubbleinSheets_v1 $MAXlevel $Oh $offset $tmax
