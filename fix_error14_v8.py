import nbformat
import json
import os

paths = [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']

# ─── New Cell 3 (Python Logic) ───
cell_3_code = r"""import pyprt
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
    
    # Recenter to avoid precision issues
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
    # Using glb (binary glTF) is often more robust in Autodesk Viewer
    gltf_data = mesh.export(file_type='gltf')
    if isinstance(gltf_data, bytes): gltf_data = gltf_data.decode('utf-8')
    gltf_list = [json.loads(gltf_data) if isinstance(gltf_data, str) else gltf_data]

    print(f"\n✅ Center Point: {center_point}")
    print(f"✅ Model centered and glTF ready.")
else:
    print("❌ Model generation failed.")"""

# ─── New Cell 4 (HTML/JS Logic) ───
cell_4_code = r"""from IPython.display import HTML, display
import json

try:
    gltf_list
    if not gltf_list or not gltf_list[0]:
         raise Exception("gltf_list is empty.")
except NameError:
    raise Exception("Run previous cells first.")

model_json = json.dumps(gltf_list[0])

html_code = f\"\"\"
<div id='viewer-container-v8' style='position:relative; width:800px; height:600px; background: #000; border-radius: 8px;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    <div id='log-v8' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#0f0; font-family:monospace; font-size:11px; padding:10px; z-index:1002;'>
        Diagnostic Viewer v8 (Fixing Error 14)...
    </div>
</div>

<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
function vLog(msg) {{
    var d = document.getElementById('log-v8');
    d.innerHTML += '<br>> ' + msg;
    d.scrollTop = d.scrollHeight;
}}

(function() {{
    function run() {{
        if (typeof Autodesk === 'undefined') {{
            setTimeout(run, 1000);
            return;
        }}

        var options = {{ env: 'Local', useADP: false }};
        
        Autodesk.Viewing.Initializer(options, async function() {{
            var viewerDiv = document.getElementById('viewer');
            var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
            viewer.start();
            
            vLog('Viewer started. Registering glTF extension manually...');
            
            try {{
                // Error 14 usually means the viewer can't resolve the glTF extension plugin.
                // We try to load it EXPLICITLY before loading the model.
                await viewer.loadExtension('Autodesk.glTF');
                vLog('Extension Autodesk.glTF loaded.');

                var modelData = {model_json};
                var blob = new Blob([JSON.stringify(modelData)], {{type: 'application/json'}});
                var url = URL.createObjectURL(blob);
                
                // Using a direct object with dummy name to satisfy internal extension checks
                var loadOptions = {{
                    fileExt: 'gltf',
                    modelName: 'model.gltf'
                }};

                vLog('Loading model...');
                viewer.loadModel(url, loadOptions, function(m) {{
                    vLog('SUCCESS: Model visible!');
                    viewer.fitToView();
                    setTimeout(function(){{ document.getElementById('log-v8').style.display='none'; }}, 5000);
                }}, function(errCode, errMsg) {{
                    vLog('LOAD ERROR ' + errCode + ': ' + errMsg);
                    if (errCode == 14) {{
                        vLog('CRITICAL: Viewer still cannot find glTF extension. This might be a VS Code webview sandbox restriction.');
                    }}
                }});

            }} catch (ex) {{
                vLog('EXCEPTION: ' + ex.message);
            }}
        }});
    }}
    setTimeout(run, 500);
}})();
</script>
\"\"\"
display(HTML(html_code))"""

for p in paths:
    if not os.path.exists(p): continue
    with open(p, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if 'pyprt.ModelGenerator' in cell.source:
                cell.source = cell_3_code
            if 'Diagnostic' in cell.source or 'viewer-container' in cell.source or 'Initializing Diagnostic' in cell.source:
                cell.source = cell_4_code
                
    with open(p, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Updated {p} to v8")
