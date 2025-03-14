#!/bin/bash

while true; do
    DURATION=$(( (RANDOM % 180) + 30 ))

    stress-ng --cpu $(nproc) --iomix 4 --hdd 2 --vm-bytes 90% --vm-keep -t $DURATION &

    sleep $DURATION &
done