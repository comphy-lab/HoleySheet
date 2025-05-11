#!/bin/bash

start="1031"
end="1039"

for i in `seq $start $end`;
do
echo $i
mkdir -p $i
cp bubbleinSheets_03 $i
done
