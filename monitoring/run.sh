#!/bin/bash

python main.py --m=cpu_utilization > cpu_utilization.log 2>&1 &
python main.py --m=response_time > response_time.log 2>&1 &
