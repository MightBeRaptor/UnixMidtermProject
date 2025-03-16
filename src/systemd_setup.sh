#!/bin/bash

SERVICE_PATH="/etc/systemd/system/stresser.service"

echo "[Unit]
Description=Cause stress on the system
After=network.target

[Service]
ExecStart=/home/etg1717/UnixMidtermServer/src/stresser.sh
Restart=always
User=etg1717
WorkingDirectory=/home/etg1717/UnixMidtermServer
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target" | sudo tee  > /dev/null

sudo chmod +x src/stresser.sh

sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME