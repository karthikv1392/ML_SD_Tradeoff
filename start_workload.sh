#!/bin/bash

DAY_DURATION=600
DAYS_COUNT=2
WORKLOAD_FILE_PATH="./workload/workload_2_days.txt"

# START monitoring
cd ./monitoring || exit 1
chmod +x ./run.sh
chmod +x ./terminate.sh

TS_INIT=$(date  +"%Y-%m-%d %T.%6N")

./run.sh

cd .. || exit 1

# START swg

cd ./swg || exit 1
./bin/swg -w $WORKLOAD_FILE_PATH -d $DAY_DURATION

# STOP monitoring
cd ../monitoring || exit 1
./terminate.sh

TS_END=$(date  +"%Y-%m-%d %T.%6N")

# SAVING workload metadata
python main.py --m=save_workload --ts_init="$TS_INIT" --ts_end="$TS_END" --days_count=$DAYS_COUNT --day_duration=$DAY_DURATION
