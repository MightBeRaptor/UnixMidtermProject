#!/bin/bash

while true; do
    # Cause stress for a random amount of time
    stress-ng --cpu $(nproc) --iomix 4 --hdd 2 --vm-bytes 90% --vm-keep -t $(( (RANDOM % 180) + 30 ))

    # Sleep for a random amount of time
    sleep($(( (RANDOM % 180) + 30 )))
done