import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell.get('source', []))
        if 'trimesh.Trimesh' in source:
            print("--- CELL 3 ---")
            print(source)
