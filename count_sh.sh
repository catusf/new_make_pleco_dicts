#!/bin/bash

# Directory to scan (default to current directory)
DIR=${1:-.}

# Find all files, get their last modification time in "date hour" format, and count occurrences
find "$DIR" -type f -printf "%TY-%Tm-%Td %TH\n" | awk '
{
    # Extract date and hour
    date_hour[$1 " " $2]++
}
END {
    # Print the results in sorted order
    for (key in date_hour) {
        print key, date_hour[key]
    }
}' | sort | awk '
{
    # Reformat the sorted results for better readability
    printf "%s %s:00 - %s:59 => %d modifications\n", $1, $2, $2, $3
}'
