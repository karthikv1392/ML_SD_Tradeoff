#!/bin/bash

# START monitoring
cd ./monitoring || exit 1
./terminate.sh

pkill -f [s]wg