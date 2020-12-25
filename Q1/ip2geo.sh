#!/bin/sh
# Sort the frequency of the IP
cat access.log | sort | uniq -c | awk '{print $2}' > ips.txt
uniq -c ips.txt | awk '{print $2","$1}' | sort -k2g > ips.csv

# Find the country name of the IP
cat /dev/null > countries.csv
while IFS=, read -r f1 f2
do
    echo "`curl -s https://freegeoip.app/csv/$f1 | cut -d "," -f3`,$f2" >> countries.csv
done < ips.csv

# Find the most hit country
awk -F "," '{arr[$1]+=$2;} END {for (i in arr) print i"," arr[i]}' countries.csv > sum.csv
sort -r -k2 -n -t, sum.csv > output.csv && head -1 output.csv

