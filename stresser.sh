#!/bin/bash

stress-ng --cpu $(nproc) --io 4 --hdd 2 --vm-bytes 90% --vm-keep -t $(( (RANDOM % 180) + 30 ))s &