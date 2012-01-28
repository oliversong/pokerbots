#!/bin/bash

i='asdf asdf blah1 asd blah2 asdf blah3.txt'
regex='.+ (\w+) .+ (\w+) .+ (\w+)\.txt'
if [[ $i =~ $regex ]]; then
  echo "it matches"
  i=1
  n=${#BASH_REMATCH[*]}
  echo $n
  while [[ $i -lt $n ]]
  do
    echo " capture[$i]: ${BASH_REMATCH[$i]}"
    let i++
  done
else
  echo "no match"
fi

