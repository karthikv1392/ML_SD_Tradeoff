#!/bin/bash

while getopts m: flag
do
    case "${flag}" in
        m) mode=${OPTARG};;
        *) ;;
    esac
done

if [ "$mode" -eq 1 ]; then
  python main.py --m=cpu_utilization --live=True > cpu_utilization.log 2>&1 &
fi

if [ "$mode" -eq 2 ]; then
  python main.py --m=response_time --live=True > response_time.log 2>&1 &
fi

if [ "$mode" -eq 3 ]; then
  python main.py --m=cpu_utilization --live=True > cpu_utilization.log 2>&1 &
  python main.py --m=response_time --live=True > response_time.log 2>&1 &
fi


