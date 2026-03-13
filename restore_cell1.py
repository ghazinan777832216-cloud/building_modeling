import json

nb_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell1_code = {
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# === Cell 1: Interactive Map & Polygon Drawing ===\n',
        '\n',
        'import leafmap\n',
        'from IPython.display import display\n',
        '\n',
        '# Create interactive map centered on target area\n',
        'm = leafmap.Map(center=[15.3694, 44.1910], zoom=16)\n',
        '\n',
        '# Add drawing toolbar so the user can draw a polygon\n',
        'm.add_draw_control()\n',
        '\n',
        'print("\u2705 \u0627\u0644\u062e\u0631\u064a\u0637\u0629 \u062c\u0627\u0647\u0632\u0629 \u2014 \u0627\u0631\u0633\u0645 \u0645\u0636\u0644\u0639\u064b\u0627 \u062b\u0645 \u0634\u063a\u0651\u0644 \u0627\u0644\u062e\u0644\u064a\u0629 \u0627\u0644\u062a\u0627\u0644\u064a\u0629")\n',
        'print("\u2705 Map ready \u2014 draw a polygon then run Cell 2")\n',
        '\n',
        'm'
    ]
}

cells = nb['cells']
insert_idx = None
for i, cell in enumerate(cells):
    src = ''.join(cell.get('source', []))
    if 'Cell 1: Interactive Map' in src and cell['cell_type'] == 'markdown':
        insert_idx = i + 1
        break

if insert_idx is not None:
    next_cell = cells[insert_idx] if insert_idx < len(cells) else None
    if next_cell and next_cell['cell_type'] == 'code' and 'leafmap' in ''.join(next_cell.get('source', [])):
        print('Cell 1 code already present, skipping.')
    else:
        cells.insert(insert_idx, cell1_code)
        print(f'Inserted Cell 1 code at index {insert_idx}')
else:
    print('ERROR: Could not find Cell 1 markdown header')
    import sys; sys.exit(1)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done. Notebook saved.')
