# Add src/get_socket_status.sh to crontab to run every 5 mins
crontab -l | { cat; echo "*/5 * * * * /bin/bash /home/your-username/Downloads/agent/src/get_socket_status.sh"; } | crontab - 