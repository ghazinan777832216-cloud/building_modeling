import json
import os

paths = [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']

# ─── V11: GLB + BASE64 Logic (Cell 3) ───
v11_c3 = r"""import pyprt, os, numpy as np, trimesh, json, base64

# ... (PRT common logic) ...
try:
    utm_polygon
except NameError:
    raise RuntimeError("لم يتم تعريف المضلع. تأكد من تنفيذ الخلية السابقة.")

pyprt.initialize_prt()
coords_2d = list(utm_polygon.exterior.coords)[:-1] 
flat_coords = []
for x, y in coords_2d: flat_coords.extend([x, 0.0, y]) 

initial_shape = pyprt.InitialShape(flat_coords)
attributes = {
    "Usage": "Residential", "Mode": "Generate Facade", "Nbr_of_Floors": 8,
    "Standard_Floor_Height": 3.2, "Ground_Floor_Height": 5.0,
    "Front_Setback_Mode": "Increasing", "Front_Setback_Distance": 4.5,
    "Layout_Shape": "Along Front", "Wing_Width": 15.0,
    "Layout_Orientation": "Open To Back", "Green_Space.Generate_Green_Space": True,
    "Green_Space.Create_Trees": False,
}

RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])
generated_models = model_generator.generate_model([attributes], RPK_PATH, "com.esri.pyprt.PyEncoder", {"emitGeometry": True})

if generated_models and generated_models[0]:
    gm = generated_models[0]
    raw_verts = np.array(gm.get_vertices(), dtype=np.float32).reshape(-1, 3)
    
    # Recenter model to origin
    center_point = np.mean(raw_verts, axis=0)
    centered_verts = raw_verts - center_point
    
    raw_indices, raw_faces = gm.get_indices(), gm.get_faces()
    triangles, offset = [], 0
    for n in raw_faces:
        face_indices = raw_indices[offset:offset + n]
        for i in range(1, n - 1): triangles.append([face_indices[0], face_indices[i], face_indices[i + 1]])
        offset += n

    mesh = trimesh.Trimesh(vertices=centered_verts, faces=triangles)
    
    # EXPORT AS GLB (Binary) - More robust than glTF JSON
    glb_data = mesh.export(file_type='glb')
    
    # Convert binary to Base64 string for safe transport to JS
    glb_base64 = base64.b64encode(glb_data).decode('utf-8')
    
    # Store it in a way Cell 4 can find
    model_b64 = glb_base64
    print(f"\n✅ Model generated, centered at {center_point}, and encoded as GLB.")
else:
    print("❌ Generation failed.")"""

# ─── V11: BASE64 -> BLOB -> VIEWER (Cell 4) ───
v11_c4 = r"""from IPython.display import HTML, display

try:
    model_b64
except NameError:
    raise Exception("Run Cell 3 first.")

html_code = f\"\"\"
<div id='viewer-v11' style='width:800px; height:600px; background: #000; border-radius:8px;'></div>
<div id='log-v11' style='font-size:11px; color:#0f0; background:#111; padding:5px; font-family:monospace;'>Initializing...</div>

<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>
<script>
(function() {{
    var log = (m) => document.getElementById('log-v11').innerText = m;
    
    function base64ToBlob(base64) {{
        var binary = atob(base64);
        var array = new Uint8Array(binary.length);
        for (var i = 0; i < binary.length; i++) array[i] = binary.charCodeAt(i);
        return new Blob([array], {{type: 'model/gltf-binary'}});
    }}

    async function start() {{
        if (typeof Autodesk === 'undefined') {{ setTimeout(start, 500); return; }}
        
        Autodesk.Viewing.Initializer({{ env: 'Local' }}, async function() {{
            var viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('viewer-v11'));
            viewer.start();
            
            log('Loading Extension...');
            await viewer.loadExtension('Autodesk.glTF');
            
            log('Decoding Model...');
            var blob = base64ToBlob("{model_b64}");
            var url = URL.createObjectURL(blob);
            
            log('Opening model...');
            viewer.loadModel(url, {{ fileExt: 'glb' }}, () => {{
                log('Model Visible!');
                viewer.fitToView();
            }}, (c, m) => log('Error ' + c + ': ' + m));
        }});
    }}
    start();
}})();
</script>
\"\"\"
display(HTML(html_code))"""

for p in paths:
    if not os.path.exists(p): continue
    with open(p, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            src = "".join(cell['source'])
            if 'pyprt.ModelGenerator' in src or 'Recenter model' in src:
                cell['source'] = [v11_c3]
                cell['outputs'] = []
            if 'viewer-v10' in src or 'viewer-v11' in src or 'vLog' in src or 'Diagnostic' in src:
                cell['source'] = [v11_c4]
                cell['outputs'] = []
    
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print(f"Patched {p} to v11 (Base64/GLB)")
