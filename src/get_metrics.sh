# Store the time in a variable
filename="data/metrics_$(date +'%Y-%m-%d_%H-%M-%S').txt"

# Ensure the directory exists
mkdir -p data

# Get metrics
touch "$filename"

# CPU
top -bn1 | grep "Cpu(s)" >> "$filename"
# Expected data
# %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

# MEMORY
free -m | grep -E "total|Mem:" >> "$filename"
# Expected data:
#                total        used        free      shared  buff/cache   available
#Mem:             969         492         283           0         344         477

# DISK
df -h | grep -E "Filesystem|sda" >> "$filename"
# Expected data:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       9.7G  2.7G  6.5G  30% /
# /dev/sda15      124M   12M  113M  10% /boot/efi

# DISK I/O
iostat -dx 1 1 | grep -E "Device|sda" >> "$filename"
# Expected data:
# Device            r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz     f/s f_await  aqu-sz  %util
# sda              2.32     57.09     0.15   5.99    0.96    24.61    2.25    160.07     0.62  21.74   26.21    71.25    0.03    239.88     0.00   0.00    0.39  7834.06    0.19    0.05    0.06   0.30

# NETWORK
ifstat 1 1 >> "$filename"
# Expected data:
#      ens5                ens4       
#KB/s in  KB/s out   KB/s in  KB/s out
#   0.00      0.00      0.06      0.19