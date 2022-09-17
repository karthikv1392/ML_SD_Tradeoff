#!/bin/bash

# START monitoring
cd ./monitoring || exit 1
python main.py --m=live_monitoring &

cd ..
# START swg
cd ./swg || exit 1
./bin/swg -w ./workload/workload_soft.txt -d 1800 -t http://localhost:8000 &
