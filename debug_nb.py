import json
import os

print("Searching for cells with 'html_code'...")
with open('pipeline_new.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    source_str = ''.join(cell.get('source', []))
    if 'html_code =' in source_str:
        print(f"Cell {i} (Type: {cell['cell_type']}):")
        print("-" * 20)
        print(source_str[:200] + "...")
        print("-" * 20)
