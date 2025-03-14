#!/bin/bash

while true; do
    STRESS_DURATION=$(( (RANDOM % 180) + 30 ))

    stress-ng --cpu $(nproc) --iomix 4 --hdd 2 --vm-bytes 90% --vm-keep -t $STRESS_DURATION &
    sleep $STRESS_DURATION &

    sleep $(( (RANDOM % 180) + 30 )) &
done