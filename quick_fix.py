import os

paths = [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']

target = '"                var url = URL.createObjectURL(blob);\\n",'
replacement = '"                var url = URL.createObjectURL(blob) + \'#.gltf\';\\n",'

target2 = '"                log(\'Loading Model from: \' + url);\\n",'
replacement2 = '"                log(\'Loading Model URL: \' + url);\\n",'

target3 = '"                viewer.loadModel(url, {{}}, function(model) {{\\n",'
replacement3 = '"                var loadOptions = { fileExt: \'gltf\', loadAsExtension: \'gltf\' };\\n",\n    "                viewer.loadModel(url, loadOptions, function(model) {{\\n",'

for path in paths:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace(target, replacement)
        content = content.replace(target2, replacement2)
        content = content.replace(target3, replacement3)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
