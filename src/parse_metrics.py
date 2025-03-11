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
    cpu_code_map = {
        'us': 'user',
        'sy': 'system',
        'ni': 'lower_priority_processes',
        'id': 'idle',
        'wa': 'waiting_for_IO',
        'hi': 'hardware_interrupts',
        'si': 'software_interrupts',
        'st': 'steal_time'
    }
    cpu_lines = ""
    mem_lines = ""

    previous_line = None
    for line in lines:
        if line.startswith('%Cpu(s):'):
            cpu_lines += line

    # CPU
    data['cpu'] = dict()
    cpu_lines = cpu_lines.split('%Cpu(s):')[1].strip()
    cpu_data = cpu_lines.split(',') # ['0.0 us', '50.0 sy', ..]
    for element in cpu_data:
        element = element.strip() # '0.0 us'
        value = element.split(' ')[0] # '0.0'
        code = element.split(' ')[1] # 'us'
        code_string = cpu_code_map[code] # 'user'
        data['cpu'][code_string] = float(value)




# Save to json
json_path = os.path.join(data_dir, f'metrics_{date}.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(date)