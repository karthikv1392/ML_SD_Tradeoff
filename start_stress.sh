#!/bin/bash

# START monitoring
cd ./monitoring || exit 1
python main.py --m=live_monitoring &

cd ..
# START swg
cd ./swg || exit 1
./bin/swg -w ./workload/workload_8.txt -d 86400 -t http://localhost:8000 &
