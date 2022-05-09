#!/bin/bash

DAY_LENGTH=180
WORKLOAD_FILE_PATH="./workload/workload_test.txt"

# START monitoring
cd ./monitoring || exit 1
chmod +x ./run.sh
chmod +x ./terminate.sh
./run.sh

cd .. || exit 1

# START swg
cd ./swg || exit 1
./bin/swg -w $WORKLOAD_FILE_PATH -d $DAY_LENGTH

# STOP monitoring
cd ../monitoring || exit 1
./terminate.sh
