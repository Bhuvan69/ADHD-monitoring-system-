#!/bin/bash

timestamp=$(date +%s)

test1="arecord /home/pi/videos/"$timestamp".wav -D sysdefault:CARD=1 -d 0"
test2="raspivid -o /home/pi/videos/"$timestamp".h264 -t 0"

echo "Process \"$test1\" started";
$test1 & pid=$!
PID_LIST+=" $pid";

echo "Process \"$test2\" started";
$test2 & pid=$!
PID_LIST+=" $pid";

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";
