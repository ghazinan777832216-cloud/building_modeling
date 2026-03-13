import nbformat

def create_notebook():
    nb = nbformat.v4.new_notebook()
    
    # Cell 1: Intro
    nb.cells.append(nbformat.v4.new_markdown_cell(
        "# Python GIS Procedural Pipeline (Modular Architecture)\n\n"
        "This notebook implements an end-to-end pipeline using the new modular architecture:\n"
        "1. Draw a polygon on an interactive map\n"
        "2. Extract GeoJSON & transform coordinates to UTM with a standalone Geometry layer function\n"
        "3. Generate a procedural building with PyPRT kernel function with Local Offsetting\n"
        "4. Visualize the 3D model natively with Three.js via embedded HTML iframe"
    ))
    
    # Cell 2: Install
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 1: Project Infrastructure (uv) \nFast dependency installation using `uv`."))
    nb.cells.append(nbformat.v4.new_code_cell("!uv pip install leafmap shapely pyproj pyprt ipywidgets"))
    
    # Cell 3: Map View
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 2: GIS Layer - Map View & Polygon Drawing \nUses leafmap to render an interactive map where the user can sketch building footprints."))
    nb.cells.append(nbformat.v4.new_code_cell(
"""import leafmap
from IPython.display import display

m = leafmap.Map(center=[15.3694, 44.1910], zoom=16)

drawn_features = []

def on_draw(feature, **kwargs):
    drawn_features.append(feature)
    print("✅ تم رسم مضلع جديد (New polygon drawn!)")

m.on_draw(on_draw)
display(m)
"""
    ))
    
    # Cell 4: GIS to UTM Geometry conversion
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 3: Geometry Layer - Extract & Transform (UTM) \nModular function to safely parse the last drawn GeoJSON feature into a shapely polygon and convert to UTM zone 38N in meters."))
    nb.cells.append(nbformat.v4.new_code_cell(
"""from shapely.geometry import shape, Polygon
from pyproj import Transformer

def get_polygon():
    if not drawn_features:
        print("لا يوجد مضلع مرسوم (No polygon drawn yet)")
        return None
    geojson = drawn_features[-1]
    return shape(geojson["geometry"])

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32638", always_xy=True)

def to_utm(polygon):
    coords = list(polygon.exterior.coords)
    utm = [transformer.transform(x, y) for x, y in coords]
    p = Polygon(utm)
    if not p.exterior.is_ccw:
        p = Polygon(list(p.exterior.coords)[::-1])
    return p
"""
    ))
    
    # Cell 5: Procedural Kernel
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 4: Procedural Core (PyPRT) & Local Offsetting \nApplies Esri rules (`RuleFootprint.rpk`) after translating the model closer to the absolute center (0,0) to prevent precision issues across the pipeline."))
    nb.cells.append(nbformat.v4.new_code_cell(
"""import pyprt, os, base64

try:
    pyprt.initialize_prt()
except Exception as e:
    pass # PyPRT already initialized

def generate_building(utm_polygon):
    coords_2d = list(utm_polygon.exterior.coords)[:-1]
    
    # Mathematical Transformation: Local Offsetting to avoid Three.js precision issues
    center_x = sum(c[0] for c in coords_2d) / len(coords_2d)
    center_y = sum(c[1] for c in coords_2d) / len(coords_2d)
    
    flat_coords = []
    for x, y in coords_2d:
        flat_coords.extend([x - center_x, 0.0, y - center_y])  # X local = X UTM - X ref
        
    initial_shape = pyprt.InitialShape(flat_coords)
    attributes = {
        "Usage": "Residential",
        "Mode": "Generate Facade",
        "Nbr_of_Floors": 8,
        "Standard_Floor_Height": 3.2,
        "Ground_Floor_Height": 5
    }
    
    model = pyprt.ModelGenerator([initial_shape])
    
    RPK_PATH = r"C:\\RPK\\RuleFootprint.rpk"
    out_dir = os.path.join(os.getcwd(), "output_models")
    os.makedirs(out_dir, exist_ok=True)
    
    encoder = "com.esri.prt.codecs.GLTFEncoder"
    encoder_options = {
        "outputPath": out_dir,
        "baseName": "procedural_building"
    }
    
    model.generate_model([attributes], RPK_PATH, encoder, encoder_options)
    
    glb_path = os.path.join(out_dir, "procedural_building_0.glb")
    with open(glb_path, "rb") as f:
        glb_data = f.read()
        
    print(f"✅ Model Generated Locally for High Precision!")
    print(f"Reference offset: X={center_x:.2f}, Y={center_y:.2f}")
    
    return base64.b64encode(glb_data).decode('utf-8')
"""
    ))
    
    # Cell 6: Visualization ThreeJS
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 5: 3D Visualization (Three.js Native Component) \nWe take the base64-encoded GLB from the procedural core and inject it natively into an embedded Three.js viewer with interactive tools."))
    nb.cells.append(nbformat.v4.new_code_cell(
"""import os, webbrowser
from IPython.display import display, HTML

def create_viewer(model_b64):
    template_path = os.path.join(os.getcwd(), 'viewer_template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    final_html = html_content.replace('%%MODEL_B64%%', model_b64)
    
    html_filename = 'viewer_full.html'
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    full_path = os.path.abspath(html_filename)
    webbrowser.open('file:///' + full_path.replace(chr(92), '/'))
    
    display(HTML(f\"\"\"
    <div style='border: 2px solid #6366f1; background: linear-gradient(135deg, #eef2ff, #e0e7ff); padding: 25px; border-radius: 12px; font-family: system-ui; text-align: center;'>
        <h2 style='color: #4f46e5; margin-top: 0;'>🎉 Three.js Architectural Viewer</h2>
        <a href='viewer_full.html' target='_blank' 
           style='background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; box-shadow: 0 4px 16px rgba(99,102,241,0.35); margin-bottom: 20px;'>
           🏗 Open Full Screen Viewer
        </a>
        <br>
        <iframe src="{html_filename}" width="100%" height="600px" style="border:none; border-radius:8px;"></iframe>
    </div>
    \"\"\"))
"""
    ))

    # Cell 7: Full Pipeline Driver
    nb.cells.append(nbformat.v4.new_markdown_cell("## Cell 6: Execute Data Pipeline \nThe function that chains all Modular Functions step by step."))
    nb.cells.append(nbformat.v4.new_code_cell(
"""def run_pipeline():
    print("1. Reading GIS Sketch...")
    polygon = get_polygon()
    if polygon is None:
        return
        
    print("2. Mathematical Transformation to UTM...")
    utm_polygon = to_utm(polygon)
    
    print("3. Generating Procedural Model (PyPRT)...")
    gltf_b64 = generate_building(utm_polygon)
    
    print("4. Preparing Visualization Context...")
    create_viewer(gltf_b64)

# Execute the pipeline
run_pipeline()
"""
    ))

    with open('pipeline_new.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == '__main__':
    create_notebook()
    print("Notebook updated successfully.")
