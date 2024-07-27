#!/bin/bash

start="1010"
end="1016"

for i in `seq $start $end`;
do
echo $i
mkdir -p $i
cp bubbleinSheets_01 VideoBubbleinSheet.py $i
cp get* $i
done