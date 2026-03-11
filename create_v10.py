import json
import os

p = r'c:\Users\hisham\Desktop\building_modeling\pipeline_v10.ipynb'

v10_c3 = r"""import pyprt
import os
import numpy as np
import trimesh
import json

try:
    utm_polygon
except NameError:
    raise RuntimeError("لم يتم تعريف المضلع. تأكد من تنفيذ الخلية السابقة.")

pyprt.initialize_prt()

coords_2d = list(utm_polygon.exterior.coords)[:-1] 
flat_coords = []
for x, y in coords_2d:
    flat_coords.extend([x, 0.0, y]) 

initial_shape = pyprt.InitialShape(flat_coords)

attributes = {
    "Usage":                              "Residential",
    "Mode":                               "Generate Facade",
    "Nbr_of_Floors":                      8,
    "Standard_Floor_Height":               3.200,
    "Ground_Floor_Height":                 5.000,
    "Front_Setback_Mode":                 "Increasing",
    "Front_Setback_Distance":              4.500,
    "Layout_Shape":                       "Along Front",
    "Wing_Width":                          15.000,
    "Layout_Orientation":                  "Open To Back",
    "Green_Space.Generate_Green_Space":     True,
    "Green_Space.Create_Trees":             False,
}

RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])
generated_models = model_generator.generate_model(
    [attributes], RPK_PATH, "com.esri.pyprt.PyEncoder",
    {"emitGeometry": True, "emitReport": True}
)

if generated_models and generated_models[0]:
    gm = generated_models[0]
    raw_verts = np.array(gm.get_vertices(), dtype=np.float32).reshape(-1, 3)
    
    center_point = np.mean(raw_verts, axis=0)
    centered_verts = raw_verts - center_point
    
    raw_indices = gm.get_indices()
    raw_faces = gm.get_faces()
    triangles = []
    offset = 0
    for n in raw_faces:
        face_indices = raw_indices[offset:offset + n]
        for i in range(1, n - 1):
            triangles.append([face_indices[0], face_indices[i], face_indices[i + 1]])
        offset += n

    mesh = trimesh.Trimesh(vertices=centered_verts, faces=triangles)
    gltf_data = mesh.export(file_type='gltf')
    if isinstance(gltf_data, bytes): gltf_data = gltf_data.decode('utf-8')
    gltf_list = [json.loads(gltf_data) if isinstance(gltf_data, str) else gltf_data]

    print(f"\n✅ Center Point: {center_point}")
    print(f"✅ Model centered successfully.")
else:
    print("❌ Model generation failed.")"""

v10_c4 = r"""from IPython.display import HTML, display
import json

try:
    gltf_list
except NameError:
    raise Exception("Run Cell 3 first.")

model_json = json.dumps(gltf_list[0])

html_code = f\"\"\"
<div id='viewer-container-v10' style='position:relative; width:800px; height:600px; background: #000; border-radius: 8px;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    <div id='log-v10' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#0f0; font-family:monospace; font-size:11px; padding:10px; z-index:1002;'>
        Diagnostic Viewer v10 (FORCED FIX)...
    </div>
</div>

<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
function vLog(msg) {{
    var d = document.getElementById('log-v10');
    d.innerHTML += '<br>> ' + msg;
    d.scrollTop = d.scrollHeight;
}}

(function() {{
    async function run() {{
        if (typeof Autodesk === 'undefined') {{
            setTimeout(run, 1000);
            return;
        }}

        Autodesk.Viewing.Initializer({{ env: 'Local', useADP: false }}, async function() {{
            var viewerDiv = document.getElementById('viewer');
            var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
            viewer.start();
            vLog('Viewer started. MANUALLY loading glTF extension...');
            
            try {{
                await new Promise(r => setTimeout(r, 1000));
                await viewer.loadExtension('Autodesk.glTF');
                vLog('Extension Autodesk.glTF loaded.');

                var blob = new Blob([JSON.stringify({model_json})], {{type: 'application/json'}});
                var url = URL.createObjectURL(blob);
                
                viewer.loadModel(url, {{ fileExt: 'gltf', modelName: 'model.gltf' }}, function() {{
                    vLog('SUCCESS: Visible!');
                    viewer.fitToView();
                }}, function(c, m) {{ vLog('LOAD ERROR ' + c + ': ' + m); }});
            }} catch (ex) {{ vLog('ERROR: ' + ex.message); }}
        }});
    }}
    setTimeout(run, 100);
}})();
</script>
\"\"\"
display(HTML(html_code))"""

with open(p, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = "".join(cell['source'])
        if 'pyprt.ModelGenerator' in src:
            cell['source'] = [v10_c3]
            cell['outputs'] = []
        if 'Diagnostic' in src or 'viewer-container' in src or 'HTML(html_code)' in src:
            cell['source'] = [v10_c4]
            cell['outputs'] = []

with open(p, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("v10 Created")
