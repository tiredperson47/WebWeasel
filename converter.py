#!/usr/bin/python3

import argparse
import json
import re
import os

parser = argparse.ArgumentParser(description="Convert Gobuster output to JSON")
parser.add_argument('-f', '--file', type=str, required=True, help="Path to the Gobuster output file")
parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output JSON file")

args = parser.parse_args()

file = args.file
output = args.output

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

# dictionary used to output json
dict1 = {}

# create fields that will contain data that each discovered endpoint will show
fields = ['directory', 'staus', 'size']

with open(file) as fh:
     
 
     
    # count variable so that each discovered endpoint is its own section
    l = 1
     
    for line in fh:
         
        # reading line by line from the text file
        match_ep = re.search(r'(?<=^\/)\S+', line)
        match_code = re.search(r'(?<=Status:\s)\d{3}', line)
        match_size = re.search(r'(?<=Size:\s)\d+', line)

        if match_ep and match_code and match_size:
            info = [match_ep.group(0), match_code.group(0), match_size.group(0)]
     
        i = 0
        # intermediate dictionary
        dict2 = {}
        while i<len(fields):
             
                # creating dictionary for each endpoint
                dict2[fields[i]] = info[i]
                i = i + 1
                 
        # appending the record of each endpoint to the main dictionary
        bruh ='endpoint'+str(l)
        dict1[bruh]= dict2
        l = l + 1
 
 
# creating json file        
out_file = open(output, "w")
json.dump(dict1, out_file, indent = 4)
out_file.close()

print(f"'==================== Output written to' {output} '===================='")
