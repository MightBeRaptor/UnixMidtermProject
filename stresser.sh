#!/bin/bash



stress-ng --cpu $(nproc) -t $(( (RANDOM % 180) + 30 )) &