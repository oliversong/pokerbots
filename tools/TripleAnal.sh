#! /bin/bash
#   lulz I am mature
#   usage: bash TripleAnal.sh path_to_folder_corresponding_to_day

echo "searcing for $1/*.txt"

count=0
for t in $(find $1 -name '*.txt')
do
  matches[$count]="$t"
  echo ${matches[$count]}
  let count++
done

for match in "${matches[@]}"
do
  echo $match
  regex='.+ (\w+) .+ (\w+) .+ (\w+)\.txt'
  if [[ $match =~ $regex ]]; then
  echo "it matches"
  n=${#BASH_REMATCH[*]}
  echo $n #should be 4
  name1=${BASH_REMATCH[$1]}
  name2=${BASH_REMATCH[$2]}
  name3=${BASH_REMATCH[$3]}
  else
    echo "no match"
  fi

  results=( $(find . -name "*$name1*.txt" -a -name "*$name2*.txt" -a -name "*$name3*.txt") ) #put these results in array
  echo ${results[@]}
  match1=${results[$1]}
  match2=${results[$2]}
  match3=${results[$3]}
  echo $match1
  echo $match2
  echo $match3
  #python AnalyzeMatchHistory.py $match1 $match2 $match3
done


