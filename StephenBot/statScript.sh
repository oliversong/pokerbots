#!/bin/bash

FILES=$1/*.txt
#~/Desktop/Jan31/*.txt

for f in $FILES
do 
    echo "Processing $f file..."
    python HandHistoryStatsCalculator.py "$f"

done
