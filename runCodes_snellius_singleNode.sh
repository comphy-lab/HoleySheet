#!/bin/bash

#SBATCH -N 1
#SBATCH --partition=genoa
#SBATCH --ntasks-per-node=96
#SBATCH --job-name=3008
#SBATCH --time=24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-type=ALL
#SBATCH --mail-user=a.k.dixit@utwente.nl

source ~/.bash_shell

MAXlevel="9"
Oh="1"
Bo="0.05"
offset="0.3"
tmax="10"

srun -n 96 asyBubbleinSheets_v1 $MAXlevel $Oh $filmThick $tmax

#CC99='mpicc -std=c99' qcc -Wall -O2 -D_MPI=1 asyBubbleinSheets_v1.c -o asyBubbleinSheets_v1 -lm -disable-dimensions
