#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def replace_in_file(file_path, replacements):
    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace each target string with 'memory_order_seq_cst'
    for target in replacements:
        content = content.replace(target, 'memory_order_seq_cst')

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory, replacements):
    # Walk through all files and directories within the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a .cpp or .h file (or any other file type you need)
            if file.endswith('.cpp') or file.endswith('.h') or file.endswith("cc"):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, replacements)
                print(f"Processed {file_path}")

# List of memory order types to be replaced
memory_order_types = [
    'memory_order_relaxed',
    'memory_order_consume',
    'memory_order_acquire',
    'memory_order_release',
    'memory_order_acq_rel'
]

# Replace '/path/to/your/folder' with the path to your folder
process_directory(sys.argv[1], memory_order_types)
