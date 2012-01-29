#! /bin/bash
#   lulz I am mature 
#   script can be made faster if neede
#   usage: bash TripleAnal.sh path_to_folder_corresponding_to_day


echo "searching for $1/*.txt" 
(
  IFS=$'\n'
  count=0
  for t in $(find $1 -name '*.txt')
  do
    matches[$count]="$t"
    # echo ${matches[$count]}
    let count++
  done

  for match in "${matches[@]}"
  do
    # echo $match
    regex='.+ (\w+) vs\. (\w+) vs\. (\w+)\.txt'
    if [[ $match =~ $regex ]]
    then
      echo "it matches"
      n=${#BASH_REMATCH[*]}
      name1=${BASH_REMATCH[1]}
      name2=${BASH_REMATCH[2]}
      name3=${BASH_REMATCH[3]}
      echo "$name1"
      echo $name2
      echo $name3
    else
      echo "no match"
    fi

    results=( $(find $1 -name "*$name1*.txt" -a -name "*$name2*.txt" -a -name "*$name3*.txt") ) #put these results in array
    #echo ${results[@]}
    match1=${results[0]}
    match2=${results[1]}
    match3=${results[2]}
    echo $match1
    echo $match2
    echo $match3
    python AnalyzeMatchHistory.py $match1 $match2 $match3
  done
)
mkdir "$1/images"
mv *.png "$1/images"
