#!/bin/bash

DAY_DURATION=180
DAYS_COUNT=7  # accepts from 1 to 7

# START monitoring
cd ./monitoring || exit 1
chmod +x ./run.sh
chmod +x ./terminate.sh

TS_INIT=$(date  +"%Y-%m-%d %T.%6N")

./run.sh

cd .. || exit 1

# START swg
cd ./swg || exit 1
./bin/swg -w $1 -d $DAY_DURATION

# STOP monitoring
cd ../monitoring || exit 1
./terminate.sh

TS_END=$(date  +"%Y-%m-%d %T.%6N")

# CLEAN cache
redis-cli flushdb

# SAVING workload metadata
python main.py --m=save_workload --ts_init="$TS_INIT" --ts_end="$TS_END" --days_count=1 --day_duration=$DAY_DURATION
