#!/bin/bash

DAY_DURATION=180
DAYS_COUNT=7

cd ./monitoring || exit 1
TS_INIT=$(date  +"%Y-%m-%d %T.%6N")

sleep 2

TS_END=$(date  +"%Y-%m-%d %T.%6N")

# SAVING workload metadata
python main.py --m=save_workload --ts_init="$TS_INIT" --ts_end="$TS_END" --days_count=$DAYS_COUNT --day_duration=$DAY_DURATION
