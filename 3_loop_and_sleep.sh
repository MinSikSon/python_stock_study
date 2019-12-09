#!/bin/sh
#sec_per_day=86400
sec_per_day=3600
count=0
while [ 1 ]; do
count=`expr $count + 1`
echo "execute count : ${count}"
./1_run.sh
echo "done.."
sleep $sec_per_day
done

