#!/bin/bash

# START swg
cd ./swg || exit 1
./bin/swg -w ./workload/workload_soft_2.txt -d 3600 -t http://localhost:8004 &
