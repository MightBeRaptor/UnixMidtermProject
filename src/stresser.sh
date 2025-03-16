#!/bin/bash

can_run=true

while true; do
    if $can_run; then
        can_run=false
        DURATION=$(( (RANDOM % 180) + 30 ))
        stress-ng --cpu $(nproc) --iomix 4 --hdd 2 --vm-bytes 90% --vm-keep -t $DURATION &

        (
            sleep $DURATION
            can_run=true
        ) &
    fi
    sleep 1
done