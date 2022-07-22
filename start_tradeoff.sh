#!/bin/bash

# START swg
cd ./swg || exit 1
./bin/swg -w ./workload/stress_1.txt -d 86400 -t http://localhost:8004 &
