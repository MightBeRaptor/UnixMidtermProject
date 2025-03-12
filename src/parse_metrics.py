# Import parent path
import sys
sys.path.append('..')
import os
import json

# Print the name of the only txt file in data dir
data_dir = 'data'
metrics_path = None
for file in os.listdir(data_dir):
    if file.endswith('.txt'):
        metrics_path = os.path.join(data_dir, file)
        break

if metrics_path is None:
    raise FileNotFoundError('No .txt file found in data dir')

# Parse the date from the metrics file name
date = metrics_path.split('/')[-1].split('.')[0].split('metrics_')[-1] # data/metrics_2025-03-11_23-14-42.txt -> 2025-03-11_23-14-42

# Parse the metrics from the file
data = dict()

# Open the file
with open(metrics_path, 'r') as f:
    lines = f.readlines()

if len(lines) == 0:
    raise ValueError('No data found in the metrics file')

cpu_code_map = {
    'us': 'User',
    'sy': 'System',
    'ni': 'Lower Priority Processes',
    'id': 'Idle',
    'wa': 'Waiting for Input/Output',
    'hi': 'Hardware Interrupts',
    'si': 'Software Interrupts',
    'st': 'Steal Time'
}
cpu_line = None
mem_lines = []
disk_lines = []
disk_io_lines = []

previous_line = None
for line in lines:
    if line.startswith('%Cpu(s):'):
        cpu_lines = line
    if line.startswith('Mem:'):
        # Add previous line
        if previous_line is None:
            raise ValueError('Memory data was found, but with no column data in a preceding line')
        mem_lines.append(previous_line)
        mem_lines.append(line)
    if line.startswith('Filesystem') or line.startswith('/dev/sda1') and not line.startswith('/dev/sda15'):
        disk_lines.append(line)
    if line.startswith('Device') or line.startswith('sda'):
        disk_io_lines.append(line)



    previous_line = line

# CPU
# Expected data
# %Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

# parse into
# {
#     'cpu': {
#               'user': 0.0,
#               'system': 0.0, ...
#            }
# }
data['CPU'] = dict()
cpu_lines = cpu_lines.split('%Cpu(s):')[1].strip()
cpu_data = cpu_lines.split(',') # ['0.0 us', '50.0 sy', ..]
for element in cpu_data:
    element = element.strip() # '0.0 us'
    value = element.split(' ')[0] # '0.0'
    code = element.split(' ')[1] # 'us'
    code_string = cpu_code_map[code] # 'user'
    data['CPU'][code_string] = float(value)

# Memory
# Expected data
#                total        used        free      shared  buff/cache   available
# Mem:             969         469         208           0         442         500

# parse into
# {
#    'memory': {
#                 'total': 969,
#              }
# }
data['Memory'] = dict()
column_headers = mem_lines[0].strip().split() #' total used free ' -> ['total', 'used', 'free']
values = mem_lines[1].strip().split('Mem:')[1].strip().split() #'Mem: 969 469' -> ['969', '469']
if len(column_headers) != len(values):
    raise ValueError('Number of columns does not match number of values for memory data')
mem_code_map = {
    'total': 'Total',
    'used': 'Used',
    'free': 'Free',
    'shared': 'Shared',
    'buff/cache': 'Buffer/Cache',
    'available': 'Available'
}
for i in range(len(column_headers)):
    header_code = column_headers[i]
    header_str = mem_code_map[header_code]
    value = int(values[i])
    data['Memory'][header_str] = value

# Disk
# Expected data:
# /dev/sda1        9.7G 2.7G   6.5G   30% /
# /dev/sda15       124M  7.8M  116M    7% /boot/efi

# parse into
# {
#     'Disk': {
#                'Size': '9.7G',
#                'Used': '2.7G',
#             }
# }
data['Disk'] = dict()
column_headers = disk_lines[0].replace('Mounted on', 'Mounted-on').strip().split() # 'Filesystem Size Used' -> ['Filesystem', 'Size', 'Used']
value_headers = disk_lines[1].strip().split() # '/dev/sda1  20G  10G' -> ['/dev/sda1', '20G', '10G']
for i in range(len(column_headers)):
    header_str = column_headers[i]
    if header_str in ['Mounted-on', 'Filesystem']:
        continue #skip
    value = value_headers[i]
    data['Disk'][header_str] = value

    
# Disk I/O
# Expected data:
# Device            r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz     w/s     wkB/s   wrqm/s  %wrqm w_await wareq-sz     d/s     dkB/s   drqm/s  %drqm d_await dareq-sz     f/s f_await  aqu-sz  %util
# sda              2.32     57.09     0.15   5.99    0.96    24.61    2.25    160.07     0.62  21.74   26.21    71.25    0.03    239.88     0.00   0.00    0.39  7834.06    0.19    0.05    0.06   0.30

# parse into
# {
#    'Disk I/O': {
#                'r/s': '2.32',
#                }
# }
data['Disk I/O'] = dict()
disk_io_code_map = {
    'r/s': 'Read Requests per Second',
    'rkB/s': 'Read Kilobytes per Second',
    'rrqm/s': 'Read Requests Merged per Second',
    '%rrqm': 'Percentage of Read Requests Merged',
    'r_await': 'Read Request Average Wait Time',
    'rareq-sz': 'Read Request Average Size',
    'w/s': 'Write Requests per Second',
    'wkB/s': 'Write Kilobytes per Second',
    'wrqm/s': 'Write Requests Merged per Second',
    '%wrqm': 'Percentage of Write Requests Merged',
    'w_await': 'Write Request Average Wait Time',
    'wareq-sz': 'Write Request Average Size',
    'd/s': 'Discard Requests per Second',
    'dkB/s': 'Discard Kilobytes per Second',
    'drqm/s': 'Discard Requests Merged per Second',
    '%drqm': 'Percentage of Discard Requests Merged',
    'd_await': 'Discard Request Average Wait Time',
    'dareq-sz': 'Discard Request Average Size',
    'f/s': 'Flush Requests per Second',
    'f_await': 'Flush Request Average Wait Time',
    'aqu-sz': 'Average Queue Size',
    '%util': 'Percentage of CPU Utilization'
}
column_headers = disk_io_lines[0].strip().split() # 'Device r/s' -> ['Device', 'r/s']
values = disk_io_lines[1].strip().split() # 'sda 2.32' -> ['sda', '2.32']
for i in range(len(column_headers)):
    header_code = column_headers[i]
    if header_code in ['Device']:
        continue #skip
    header_str = disk_io_code_map[header_code]
    value = values[i]
    data['Disk I/O'][header_str] = value



# Save to json
json_path = os.path.join(data_dir, f'metrics_{date}.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(date)