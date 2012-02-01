#!/bin/bash

FILES=~/Desktop/Jan31/*

for f in $FILES
do 
    echo "Processing $f file..."
    python ~/Documents/Pokerbots/TeamRepo/StephenBot/HandHistoryStatsCalculator.py "$f"

done
