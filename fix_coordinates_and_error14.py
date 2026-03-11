import nbformat
import json

paths = [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']

# 1. Update Cell 3 to center coordinates (fix for huge UTM values)
cell_3_update = r"""import pyprt
import os
import numpy as np
import trimesh
import json

# ── Verify Cell 2 output exists ──────────────────────────────────────────────
try:
    utm_polygon
except NameError:
    raise RuntimeError("لم يتم تعريف المضلع. تأكد من تنفيذ الخلية السابقة.")

# ── Initialize PRT engine ────────────────────────────────────────────────────
pyprt.initialize_prt()

# ── Build flat vertex list [x0,y0,z0, x1,y1,z1, ...] ────────────────────────
coords_2d = list(utm_polygon.exterior.coords)[:-1] 
flat_coords = []
for x, y in coords_2d:
    flat_coords.extend([x, 0.0, y]) 

# ── Create Initial Shape ─────────────────────────────────────────────────────
initial_shape = pyprt.InitialShape(flat_coords)

# ── Building attributes ──────────────────────────────────────────────────────
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
    "Layout_Orientation":                  \"Open To Back\",
    "Green_Space.Generate_Green_Space":     True,
    "Green_Space.Create_Trees":             False,
}

# ── Rule Package path ────────────────────────────────────────────────────────
RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
if not os.path.isfile(RPK_PATH):
    print(f"⚠️  RPK file not found at: {RPK_PATH}")
else:
    print(f"✅ RPK found: {RPK_PATH}")

# ── Generate the model ───────────────────────────────────────────────────────
model_generator = pyprt.ModelGenerator([initial_shape])
generated_models = model_generator.generate_model(
    [attributes], RPK_PATH, "com.esri.pyprt.PyEncoder",
    {"emitGeometry": True, "emitReport": True}
)

if generated_models and generated_models[0]:
    gm = generated_models[0]
    raw_verts = np.array(gm.get_vertices(), dtype=np.float32).reshape(-1, 3)
    
    # ── CRITICAL: CENTER THE MODEL (Recenter to 0,0,0) ────────────────────────
    # UTM coordinates are too large for 3D viewers (precision jitter)
    center_point = np.mean(raw_verts, axis=0)
    centered_verts = raw_verts - center_point
    print(f"Recenter: Model moved from {center_point} to origin.")
    
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

    print(f"\n✅ تم توليد المبنى وتوسيطه بنجاح (Centered Building Generated!)")
    print(f"   Vertices: {len(centered_verts)}")
else:
    print("❌ Model generation failed.")"""

# 2. Update Cell 4 to simplify loading and fix Error 14
cell_4_update = r"""from IPython.display import HTML, display
import json

try:
    gltf_list
    if not gltf_list or not gltf_list[0]:
         raise Exception("gltf_list موجودة ولكنها فارغة.")
except NameError:
    raise Exception("لم يتم توليد gltf_list بعد.")

model_data_raw = json.dumps(gltf_list[0])

html_code = f\"\"\"
<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #222; border-radius: 8px; overflow: hidden;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:#0f0; font-family:monospace; font-size:11px; padding:10px; z-index:1000;'>
        Diagnostic Viewer v7 (Centered Model Fix)...
    </div>
</div>

<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
function log(msg) {{
    var logDiv = document.getElementById('viewer-log');
    logDiv.innerHTML += '<br>> ' + msg;
    logDiv.scrollTop = logDiv.scrollHeight;
}}

(function() {{
    function initViewer() {{
        if (typeof Autodesk === 'undefined') {{
            setTimeout(initViewer, 1000);
            return;
        }}

        Autodesk.Viewing.Initializer({{ env: 'Local' }}, function() {{
            var viewerDiv = document.getElementById('viewer');
            var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
            viewer.start();
            
            log('Viewer Started. Loading data...');
            
            var gltf = {model_data_raw};
            var blob = new Blob([JSON.stringify(gltf)], {{type: 'application/json'}});
            
            // Using a simpler URL hint to avoid Error 14
            var url = URL.createObjectURL(blob);
            
            // We hint the extension using the options object
            var options = {{
                fileExt: 'gltf',
                loadAsExtension: 'gltf'
            }};

            // If Error 14 persists, we try to load without explicit extension string
            viewer.loadModel(url, options, function() {{
                log('SUCCESS: Building visible at center.');
                viewer.fitToView();
                setTimeout(function(){{ document.getElementById('viewer-log').style.display = 'none'; }}, 3000);
            }}, function(c, m) {{
                log('RETRY: Path based loader...');
                // Secondary attempt: dummy filename in URL
                viewer.loadModel(url + '?file=model.gltf', {{ fileExt: 'gltf' }});
            }});
        }});
    }}
    setTimeout(initViewer, 500);
}})();
</script>
\"\"\"
display(HTML(html_code))"""

for path in paths:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Cell 3 is index 8 based on previous views (markdown, code, markdown, code...)
        # Let's find them by content to be safe
        for cell in nb.cells:
            if cell.cell_type == 'code':
                if "pyprt.ModelGenerator" in cell.source:
                    cell.source = cell_3_update
                    print(f"Updated Cell 3 in {path}")
                if "Diagnostic" in cell.source or "viewer-container" in cell.source:
                    cell.source = cell_4_update
                    print(f"Updated Cell 4 in {path}")
        
        with open(path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
    except Exception as e:
        print(f"Error {path}: {e}")
