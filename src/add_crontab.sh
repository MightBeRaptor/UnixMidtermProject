# Add src/get_socket_status.sh to crontab to run every 5 mins
crontab -l | { cat; echo "*/5 * * * * /usr/bin/python /home/etg1717/UnixMidtermServer/src/server.py >> /home/etg1717/server.log 2>&1"; } | crontab - 