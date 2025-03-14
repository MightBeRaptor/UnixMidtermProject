# Script to check if the socket is connected or not
mkdir -p tmp
rm -f tmp/socket_status.txt
touch tmp/socket_status.txt

if [ $(netstat -an | grep 127.0.0.1:3300 | grep TCP | grep ESTABLISHED | wc -l) -eq 0 ]; then
    if [ $(netstat -an | grep 127.0.0.1:3300 | grep TCP | grep LISTEN | wc -l) -eq 0 ]; then
        echo "not listening" >> /tmp/socket_status.txt
    else
        echo "listening for connection" >> /tmp/socket_status.txt
    fi
else
    echo "connected" >> /tmp/socket_status.txt
fi
