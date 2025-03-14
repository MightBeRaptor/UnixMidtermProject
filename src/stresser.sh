#!/bin/bash

while true; do
    stress-ng --cpu $(nproc) --iomix 4 --hdd 2 --vm-bytes 90% --vm-keep -t $(( (RANDOM % 180) + 30 ))s &
    sleep $(( (RANDOM % 180) + 30 ))
done