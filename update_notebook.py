import nbformat
import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

print(f"Total cells: {len(nb.cells)}")

# Update Notebook Description (Index 0)
nb.cells[0].source = nb.cells[0].source.replace(
    '4. Visualize the 3D model with pythreejs',
    '4. Visualize the 3D model with Autodesk Viewer'
)

# Update Cell 3 (PyPRT) - Index 7
# We want to replace the part after rule generation
if 'generated_models = model_generator.generate_model' in nb.cells[7].source:
    print("Found Cell 7 correctly.")
    
    # We want to insert the gltf_list logic before the final 'else:'
    source = nb.cells[7].source
    
    gltf_logic = """
    # ── Convert to glTF for Autodesk Viewer ──────────────────────────────────
    import numpy as np
    import trimesh
    import json

    vertices = np.array(gm.get_vertices(), dtype=np.float32).reshape(-1, 3)
    raw_indices = gm.get_indices()
    raw_faces = gm.get_faces()

    triangles = []
    offset = 0
    for n in raw_faces:
        face_indices = raw_indices[offset:offset + n]
        for i in range(1, n - 1):
            triangles.append([face_indices[0], face_indices[i], face_indices[i + 1]])
        offset += n

    mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
    # Export to a self-contained glTF dictionary
    gltf_data = mesh.export(file_type='gltf')
    if isinstance(gltf_data, bytes):
        gltf_data = gltf_data.decode('utf-8')
    
    if isinstance(gltf_data, str):
        gltf_list = [json.loads(gltf_data)]
    else:
        if isinstance(gltf_data, dict) and 'model.gltf' in gltf_data:
            gltf_list = [json.loads(gltf_data['model.gltf'])]
        else:
            gltf_list = [gltf_data]

    print(f"\\n✅ تم تجهيز نموذج glTF للعرض في Autodesk Viewer (glTF prepared for Viewer)")
"""
    
    if 'if report:' in source:
        parts = source.split('if report:')
        # parts[1] contains "print(...)\nelse:\n..."
        if 'else:' in parts[1]:
            report_part, else_part = parts[1].split('else:', 1)
            nb.cells[7].source = parts[0] + 'if report:' + report_part + gltf_logic + 'else:' + else_part

# Update Cell 4 Header - Index 8
nb.cells[8].source = nb.cells[8].source.replace(
    '## الخلية 4: عرض النموذج باستخدام pythreejs',
    '## الخلية 4: عرض النموذج باستخدام Autodesk Viewer'
).replace(
    '## Cell 4: Visualize the Model with pythreejs',
    '## Cell 4: Visualize the Model with Autodesk Viewer'
)

# Update Cell 4 Code - Index 9
autodesk_code = """from IPython.display import HTML
import json

try:
    gltf_list
except NameError:
    raise Exception(\"لم يتم توليد gltf_list بعد. نفّذ الخلية السابقة أولاً.\")

# تحويل بيانات glTF إلى JSON
model_data = json.dumps(gltf_list[0])

html_code = f\"\"\"
<div id='viewer' style='width:800px;height:600px;'></div>

<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/viewer3D.min.js'></script>
<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/style.min.css'/>

<script>
var options = {{
    env: 'Local'
}};

Autodesk.Viewing.Initializer(options, function() {{
    var viewerDiv = document.getElementById('viewer');
    var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
    viewer.start();

    var gltf = {model_data};

    var blob = new Blob([JSON.stringify(gltf)], {{type: 'application/json'}});
    var url = URL.createObjectURL(blob);

    viewer.loadModel(url);
}});
</script>
\"\"\"

HTML(html_code)"""

nb.cells[9].source = autodesk_code

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook updated successfully.")
