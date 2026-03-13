import json

nb_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'm.add_draw_control()' in source:
            source = source.replace('m.add_draw_control()', '# leafmap.Map comes with a drawing toolbar by default\n# (No need to call add_draw_control() anymore)')
            # Let's rebuild the source list properly:
            cell['source'] = [line + '\n' for line in source.split('\n')]
            # Remove trailing \n on last line
            if cell['source'] and cell['source'][-1].endswith('\n') and not source.endswith('\n'):
                cell['source'][-1] = cell['source'][-1][:-1]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done. Notebook saved.')
