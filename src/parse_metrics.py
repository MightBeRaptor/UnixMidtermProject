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
data['Disk'] = dict()
column_headers = disk_lines[0].replace('Mounted on', 'Mounted-on').strip().split() # 'Filesystem Size Used' -> ['Size', 'Used']
value_headers = disk_lines[1].strip().split() # '/dev/sda1  20G  10G' -> ['20G', '10G']
for i in range(len(column_headers)):
    header_str = column_headers[i]
    if header_str in ['Mounted-on', 'Filesystem']:
        continue #skip
    value = value_headers[i]
    data['Disk'][header_str] = value

    




# Save to json
json_path = os.path.join(data_dir, f'metrics_{date}.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(date)