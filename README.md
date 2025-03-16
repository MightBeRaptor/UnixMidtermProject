# UnixMidtermServer
Server for a mid term project for a Unix System Administration course

## Overview
Create 3 servers and 1 dashboard api/agent that monitors the servers, displays performance statistics, reboots the servers when they fail, and includes basic notification support.

## Disclaimer
This server is designed to be cloned into a GCP Google Cloud Ubuntu VM instance, and connected to from a dashboard that has [Surxe/UnixMidtermDashboard](https://github.com/Surxe/UnixMidtermDashboard.git) cloned. The `get_metrics.sh` script may not function as expected in other environments and may require alterations for other operating systems during the dependency installation stage.

## Setup
1. Within the GCP instance, `git clone https://github.com/MightBeRaptor/UnixMidtermServer.git`
2. `cd UnixMidtermServer`
3. Create `.env` using `.env.example` as a guide
4. `bash src/update_dependencies.sh` - Installs dependencies for checking metrics and stressing the server
5. `bash src/add_user_groups.sh` - Creates user and groups for the server to be added to
6. `bash src/systemd_setup.sh` - Creates systemd file for the stresser. This will cause it to always run stresser for a random amount of seconds.
7. WIP `bash src/add_crontab.sh` - Adds a crontab entry that WIP runs `bash src/get_socket_status.sh` every 5 minutes which saves the socket's current status to `tmp/socket_status.txt` and restarts `python src/server.py`

## Starting the server socket
1. The crontab will start the server (if its not already up) with `python src/server.py`    
2. Every 5 minutes of the dashboard's runtime, it will request the server to run:
    1. `bash src/stresser.sh` - Stresses the server
    2. `bash src/get_metrics.sh` - Retrieve's metrics and writes them to `data/metrics_<timestamp>.txt`
    3. `python src/parse_metrics.py` - Parses the metrics from the raw txt into a readable json format in `data/metrics_<timestamp>.json`
    4. WIP: sends `data/metrics_<timestamp.json` back to the dashboard at `data/serverN/metrics_<timestamp>.json`, where serverN is the server_name from `.env`
3. When the server is no longer connected to the dashboard, it will run
    1. WIP `rm tmp/socket_status.txt` - To ensure the next time its started its not using the previous session's status


## Disable Stresser
If the stresser.service becomes problematic, it can be disabled using the following commands:
1. `sudo systemctl disable stresser.service` - Prevents launch on boot
2. `sudo systemctl stop stresser.service` - Stops the stresser.service from working
3. `systemctl status stresser.service` - Displays the status of stresser.service to make sure it is disabled
4. `pkill -9 stress-ng` - Ends the currently running stress process
To renable this service, run the command `bash src/systemd_setup.sh`