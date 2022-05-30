#!/bin/bash


./start_workload.sh -w ./workload/workload_1.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_2.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_3.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_4.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_5.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_6.txt -d 180 -c 1 -l rr
sleep 1

./start_workload.sh -w ./workload/workload_7.txt -d 180 -c 1 -l rr