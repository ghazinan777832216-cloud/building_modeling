import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell_idx_3 = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        concat_source = "".join(cell.get('source', []))
        if 'trimesh.Scene' in concat_source and 'pyprt' in concat_source:
             cell_idx_3 = i
             break

if cell_idx_3 != -1:
    old_source = "".join(nb['cells'][cell_idx_3]['source'])
    
    # Let's completely replace the mesh creation part cleanly
    # We will compute normals and update the unlit properties if possible
    new_source = [
        "import pyprt, os, numpy as np, trimesh, json, base64\n",
        "\n",
        "pyprt.initialize_prt()\n",
        "coords_2d = list(utm_polygon.exterior.coords)[:-1] \n",
        "flat_coords = []\n",
        "for x, y in coords_2d: flat_coords.extend([x, 0.0, y]) \n",
        "\n",
        "initial_shape = pyprt.InitialShape(flat_coords)\n",
        "attributes = {\"Nbr_of_Floors\": 12, \"Usage\": \"Residential\"} \n",
        "\n",
        "RPK_PATH = r\"C:\\RPK\\RuleFootprint.rpk\"\n",
        "model_generator = pyprt.ModelGenerator([initial_shape])\n",
        "generated_models = model_generator.generate_model([attributes], RPK_PATH, \"com.esri.pyprt.PyEncoder\", {\"emitGeometry\": True})\n",
        "\n",
        "if generated_models and generated_models[0]:\n",
        "    gm = generated_models[0]\n",
        "    raw_verts = np.array(gm.get_vertices(), dtype=np.float32).reshape(-1, 3)\n",
        "    \n",
        "    center_point = np.mean(raw_verts, axis=0)\n",
        "    centered_verts = raw_verts - center_point\n",
        "    \n",
        "    raw_indices, raw_faces = gm.get_indices(), gm.get_faces()\n",
        "    triangles, face_colors, offset = [], [], 0\n",
        "    \n",
        "    for n in raw_faces:\n",
        "        idx = raw_indices[offset:offset + n]\n",
        "        v1, v2, v3 = raw_verts[idx[0]], raw_verts[idx[1]], raw_verts[idx[2]]\n",
        "        normal = np.cross(v2-v1, v3-v1)\n",
        "        is_roof = normal[1] > 0.8 \n",
        "        \n",
        "        color = [200, 200, 200, 255] if is_roof else [240, 230, 210, 255] \n",
        "        \n",
        "        for i in range(1, n - 1):\n",
        "            triangles.append([idx[0], idx[i], idx[i + 1]])\n",
        "            face_colors.append(color)\n",
        "        offset += n\n",
        "\n",
        "    # Create mesh and compute normals to prevent black models\n",
        "    mesh = trimesh.Trimesh(vertices=centered_verts, faces=triangles, face_colors=face_colors)\n",
        "    mesh.fix_normals()\n",
        "    \n",
        "    # Let's adjust material to diffuse so it doesn't need environment lights for reflection\n",
        "    if hasattr(mesh.visual, 'material'):\n",
        "        mesh.visual.material.metallicFactor = 0.0\n",
        "        mesh.visual.material.roughnessFactor = 0.8\n",
        "    \n",
        "    floor = trimesh.creation.box(extents=[100, 0.1, 100]) \n",
        "    floor.visual.face_colors = [50, 50, 50, 255] \n",
        "    floor.fix_normals()\n",
        "    if hasattr(floor.visual, 'material'):\n",
        "        floor.visual.material.metallicFactor = 0.0\n",
        "        floor.visual.material.roughnessFactor = 0.8\n",
        "    \n",
        "    scene = trimesh.Scene([mesh, floor])\n",
        "    \n",
        "    glb_data = scene.export(file_type='glb')\n",
        "    model_b64 = base64.b64encode(glb_data).decode('utf-8')\n",
        "    \n",
        "    print(\"✅ Procedural Model Generated, Normals Computed, and Exported successfully.\")\n"
    ]
    
    nb['cells'][cell_idx_3]['source'] = new_source
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Write Cell 3 complete.")
