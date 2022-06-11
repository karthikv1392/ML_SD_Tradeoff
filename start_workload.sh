#!/bin/bash

#################################################################
#
# call example
#
# ./start_workload.sh -w ./workload/workload_1.txt -d 180 -c 1 -l rr
#
#################################################################


while getopts w:d:c:l flag
do
    case "${flag}" in
        w) workload_path=${OPTARG};;
        d) day_duration=${OPTARG};;
        c) days_count=${OPTARG};;
        l) label=${OPTARG};;
        *) ;;
    esac
done


# START monitoring
cd ./monitoring || exit 1
chmod +x ./run.sh
chmod +x ./terminate.sh

TS_INIT=$(date  +"%Y-%m-%d %T.%6N")

./run.sh -m 2

cd .. || exit 1

# START swg
cd ./swg || exit 1
./bin/swg -w $workload_path -d $day_duration

# STOP monitoring
cd ../monitoring || exit 1
./terminate.sh

TS_END=$(date  +"%Y-%m-%d %T.%6N")

# CLEAN cache
redis-cli flushdb

# SAVING workload metadata
python main.py --m=save_workload --ts_init="$TS_INIT" --ts_end="$TS_END" --days_count=$days_count --day_duration=$day_duration --label=$label

