#!/bin/bash

#SBATCH -N 1
#SBATCH --partition=genoa
#SBATCH --ntasks-per-node=32
#SBATCH --time=2:00:00
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out

source ~/.bash_shell

Oh=("1.00E-03" "3.00E-03" "6.00E-03" "1.00E-02" "3.00E-02" "6.00E-02" "1.00E-01")

start_data=1010
start=1015
end=1016

for (( i=start; i<=end; i++ )); do
    dir=$i
    index=$((i - start_data))  
    cd $dir || { echo "Failed to change directory to $dir"; exit 1; }
    
    python3 VideoBubbleinSheet.py --Oh ${Oh[index]} &
    
    cd ../
done

wait

for (( i=start; i<=end; i++ )); do
    dir=$i/Video
    cd $dir || { echo "Failed to change directory to $dir"; exit 1; }
    
    rm -f *.mp4
    mkvids $i.mp4 &
    
    cd ../../
done

wait
