#!/bin/bash

d=480
label="rr"
rest=60

./start_workload.sh -w ./workload/workload_1.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_2.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_3.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_4.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_5.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_6.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_7.txt -d $d -c 1 -l $label
sleep $rest

./start_workload.sh -w ./workload/workload_8.txt -d $d -c 1 -l $label
sleep $rest