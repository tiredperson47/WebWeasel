#!/usr/bin/python3

import argparse
import json
import re
import os

parser = argparse.ArgumentParser(description="Convert Gobuster output to JSON")
# Add -f for the input file and -o for the output directory
parser.add_argument('-f', '--file', type=str, required=True, help="Path to the Gobuster output file")
parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output JSON file")
#parser.add_argument('-i', '--ip', type=str, required=True, help="IP address of server you scanned")
parser.add_argument('-d', '--directory', type=str, required=True, help="Dirctory/Subdirectory you scanned with Gobuster")

args = parser.parse_args()

file = args.file
output = args.output
#ip = args.ip
directory = args.directory

print("""\


▄█     █▄     ▄████████ ▀█████████▄        ▄█     █▄     ▄████████    ▄████████    ▄████████    ▄████████  ▄█       
███     ███   ███    ███   ███    ███      ███     ███   ███    ███   ███    ███   ███    ███   ███    ███ ███       
███     ███   ███    █▀    ███    ███      ███     ███   ███    █▀    ███    ███   ███    █▀    ███    █▀  ███       
███     ███  ▄███▄▄▄      ▄███▄▄▄██▀       ███     ███  ▄███▄▄▄       ███    ███   ███         ▄███▄▄▄     ███       
███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄       ███     ███ ▀▀███▀▀▀     ▀███████████ ▀███████████ ▀▀███▀▀▀     ███       
███     ███   ███    █▄    ███    ██▄      ███     ███   ███    █▄    ███    ███          ███   ███    █▄  ███       
███ ▄█▄ ███   ███    ███   ███    ███      ███ ▄█▄ ███   ███    ███   ███    ███    ▄█    ███   ███    ███ ███▌    ▄ 
 ▀███▀███▀    ██████████ ▄█████████▀        ▀███▀███▀    ██████████   ███    █▀   ▄████████▀    ██████████ █████▄▄██


""")

# Ensure file exists
if not os.path.isfile(file):
    print(f"Error: The file '{file}' does not exist.")
    exit(1)

# Ensure the output directory exists
output_dir = os.path.dirname(output)
if not os.path.exists(output_dir):
    print(f"Error: The output directory '{output_dir}' does not exist.")
    exit(1)

# initialize dictionary and shit for output and neo4j
dict1 = {}
node = []
relationship = []

parent_node = {
    "id": "parent_node",
    "labels": ["Directory"],
    "properties": {"directory": directory}
}
node.append(parent_node)


# create fields that will contain data that each discovered endpoint will show
fields = ['directory', 'status', 'size']

with open(file) as fh:
     
 
     
    # Used to uniquly identify endpoints and subdirectories. 
    e = 1
    s = 1
     
    for line in fh:
         
        # reading line by line from the text file
        match_ep = re.search(r'(?<=^\/)\S+', line)
        match_code = re.search(r'(?<=Status:\s)\d{3}', line)
        match_size = re.search(r'(?<=Size:\s)\d+', line)

        if match_ep and match_code and match_size:
            info = [match_ep.group(0), int(match_code.group(0)), int(match_size.group(0))]

            if 300 <= info[1] < 400:
                subdirect_node = {
                    "id": f"subdir{s}",
                    "labels": ["Subdirectory"],
                    "properties": {
                        "directory": info[0],
                        "status": info[1],
                        "size": info[2]
                    }
                }
                node.append(subdirect_node)
                
                sub_relation = {
                    "startNode": f"subdir{s}",
                    "endNode": directory,
                    "type": "Subdirectory_of"
                }
                relationship.append(sub_relation)
                s = s + 1

            else:
                endpoint_node = {
                    "id": f"endpoint{e}",
                    "labels": ["Endpoint"],
                    "properties": {
                        "directory": info[0],
                        "status": info[1],
                        "size": info[2]
                    }
                }
                node.append(endpoint_node)

                relation = {
                    "startNode": f"endpoint{e}",
                    "endNode": directory,
                    "type": "Endpoint_of"
                }
                relationship.append(relation)
                e = e + 1

# creating json file        
output_data = {
    "nodes": node,
    "relationships": relationship
}

output_file = output

with open(output_file, "w") as out_file:
    json.dump(output_data, out_file, indent = 4)

print(f"======================================== Output written to {output} ========================================")

