#!/bin/bash

# START monitoring
cd ./monitoring || exit 1
python main.py --m=live_monitoring &

cd ..
# START swg
cd ./swg || exit 1
./bin/swg -w ./workload/live_1.txt -d 86400 &
