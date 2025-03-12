# UnixMidtermServer
This is a mid term project for a Unix System Administration course.

## Overview
Create 3 servers and 1 dashboard api/agent that monitors the servers, displays performance statistics, reboots the servers when they fail, and includes basic notification support.

## Disclaimer
This server is designed to be cloned into a GCP Google Cloud Ubuntu VM instance. The `get_metrics.sh` script may not function as expected in other environments and may require alterations for other operating systems during the dependency installation stage.

## Usage
1. Within the GCP instance, `git clone https://github.com/MightBeRaptor/UnixMidtermServer.git`
2. `cd UnixMidTermServer`
3. `bash src/get_metrics.sh` - Installs dependencies for checking metrics and writes them to `data/metrics_<timestamp>.txt`
4. `python3 src/parse_metrics.py` - Parses the metrics from the raw txt into a readable json format in `data/metrics/<timestamp>.json`
5. `python3 src/validate_metrics.py` - Raises warnings if the recorded metrics exceed any defined thresholds
6. `python3 src/archive_metrics.py` - Moves both the txt and the json from `data/*` to `data/archive/*`