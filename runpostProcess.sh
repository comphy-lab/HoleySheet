#!/bin/bash

#SBATCH -N 1
#SBATCH --partition=genoa
#SBATCH --ntasks-per-node=1

python3 VideoAsyBubbleinSheet.py