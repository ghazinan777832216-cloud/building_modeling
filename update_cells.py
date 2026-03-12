import json

with open("pipeline_new.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Find Cell 3
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and "pyprt" in "".join(cell["source"]) and "trimesh" in "".join(cell["source"]):
        cell3_idx = i
        break

# The new source for Cell 3
cell3_source = """import pyprt, os, base64

pyprt.initialize_prt()

# إعداد الإحداثيات للمبنى
coords_2d = list(utm_polygon.exterior.coords)[:-1] 
flat_coords = []
for x, y in coords_2d: flat_coords.extend([x, 0.0, y]) 

initial_shape = pyprt.InitialShape(flat_coords)
attributes = {"Nbr_of_Floors": 12, "Usage": "Residential"} # مثال

RPK_PATH = r"C:\\RPK\\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])

# استخدام GLTF Encoder للحصول على الألوان والخامات الحقيقية من CityEngine (RPK)
encoder = "com.esri.prt.codecs.GLTFEncoder"
out_dir = os.path.join(os.getcwd(), "output_models")
os.makedirs(out_dir, exist_ok=True)

encoder_options = {
    "outputPath": out_dir,
    "baseName": "procedural_building"
}

# توليد المبنى بصيغة GLB
model_generator.generate_model(
    [attributes], 
    RPK_PATH, 
    encoder, 
    encoder_options
)

# قراءة الملف الناتج وتحويله إلى Base64
glb_path = os.path.join(out_dir, "procedural_building_0.glb")
with open(glb_path, "rb") as f:
    glb_data = f.read()

model_b64 = base64.b64encode(glb_data).decode('utf-8')

print(f"✅ Model Ready with CityEngine Textures and Materials!")
"""

nb["cells"][cell3_idx]["source"] = [line + "\n" if not line.endswith('\n') else line for line in cell3_source.split("\n")[:-1]]
nb["cells"][cell3_idx]["outputs"] = []

# Find Cell 4
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and "Autodesk.Viewing.GuiViewer3D" in "".join(cell["source"]):
        cell4_idx = i
        break

cell4_source = """from IPython.display import HTML, display

html_code = f\"\"\"
<div id='viewer-v15' style='width:100%; height:800px; background: linear-gradient(#f0f0f0, #c0c0c0); border-radius:10px;'></div>
<div id='log-v15' style='color:#000; background:#e0e0e0; padding:10px; font-family:monospace; font-size:12px; font-weight:bold;'>Initializing Authentic CityEngine Viewer...</div>

<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js'></script>

<script>
(function() {{
    const log = (m) => document.getElementById('log-v15').innerText = '> ' + m;
    
    function b64ToBlob(b64) {{
        const bin = atob(b64);
        const buf = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
        return new Blob([buf], {{type: 'model/gltf-binary'}});
    }}

    function start() {{
        if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {{
            setTimeout(start, 500); return;
        }}
        
        Autodesk.Viewing.Initializer({{ env: 'Local' }}, function() {{
            const viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('viewer-v15'));
            viewer.start();
            
            // Themes and Environmental Setup for Best Texture Visibility
            viewer.setTheme('light-theme');
            viewer.setEnvMapBackground(true);
            viewer.setLightPreset(2); // Simple Grey / Daylight Preset for accurate colors
            viewer.setQualityLevel(/* ambient shadows */ false, /* antialiasing */ true);
            viewer.prefs.set('groundShadow', true);
            viewer.prefs.set('groundReflection', false);
            
            const url = URL.createObjectURL(b64ToBlob("{model_b64}"));
            viewer.loadModel(url + '#.glb', {{ fileExt: 'glb' }}, () => {{
                log('CityEngine Procedural Building Loaded Successfully.');
                
                // Set Up the Camera and Views appropriately
                viewer.fitToView();
            }});
        }});
    }}
    start();
}})();
</script>
\"\"\"
display(HTML(html_code))
"""
nb["cells"][cell4_idx]["source"] = [line + "\n" if not line.endswith('\n') else line for line in cell4_source.split("\n")[:-1]]
nb["cells"][cell4_idx]["outputs"] = []

with open("pipeline_new.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Updated pipeline_new.ipynb")
