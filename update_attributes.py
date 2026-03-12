import json
import os

print("Updating notebook with more robust RPK attributes...")

with open('pipeline_new.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update Cell 3 (Generation)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'pyprt.InitialShape' in ''.join(cell.get('source', [])):
        print("Found Cell 3. Updating attributes...")
        cell['source'] = [
            "import pyprt, os, base64\n",
            "import numpy as np\n",
            "\n",
            "pyprt.initialize_prt()\n",
            "\n",
            "# إخراج الإحداثيات للمبنى مع التوسيط (Centering)\n",
            "coords_2d = list(utm_polygon.exterior.coords)[:-1]\n",
            "center_x = sum(c[0] for c in coords_2d) / len(coords_2d)\n",
            "center_y = sum(c[1] for c in coords_2d) / len(coords_2d)\n",
            "\n",
            "flat_coords = []\n",
            "for x, y in coords_2d:\n",
            "    flat_coords.extend([x - center_x, 0.0, y - center_y])\n",
            "\n",
            "initial_shape = pyprt.InitialShape(flat_coords)\n",
            "\n",
            "# تحديث السمات بناءً على تحليل الـ RPK لضمان توليد الواجهات والتفاصيل\n",
            "attributes = {\n",
            "    \"Nbr_of_Floors\": 12,\n",
            "    \"Usage\": \"Residential\",\n",
            "    \"Generic_Modern_Facades.Generate_Facade\": True, # تفعيل توليد الواجهات\n",
            "    \"Generic_Modern_Facades.Level_of_Detail\": \"High\",\n",
            "    \"Generic_Modern_Facades.Transparent\": True\n",
            "}\n",
            "\n",
            "RPK_PATH = r\"C:\\RPK\\RuleFootprint.rpk\"\n",
            "model_generator = pyprt.ModelGenerator([initial_shape])\n",
            "\n",
            "encoder = \"com.esri.prt.codecs.GLTFEncoder\"\n",
            "out_dir = os.path.join(os.getcwd(), \"output_models\")\n",
            "os.makedirs(out_dir, exist_ok=True)\n",
            "\n",
            "encoder_options = {\n",
            "    \"outputPath\": out_dir,\n",
            "    \"baseName\": \"procedural_building\",\n",
            "    \"embedTextures\": True, # تأكد من تضمين القوام ليعمل الفيوور بشكل صحيح\n",
            "    \"doubleSided\": True\n",
            "}\n",
            "\n",
            "# توليد المبنى\n",
            "print(\"Generating model with enhanced attributes...\")\n",
            "model_generator.generate_model([attributes], RPK_PATH, encoder, encoder_options)\n",
            "\n",
            "# قراءة الملف وتحويله لـ Base64\n",
            "glb_path = os.path.join(out_dir, \"procedural_building_0.glb\")\n",
            "with open(glb_path, \"rb\") as f:\n",
            "    glb_data = f.read()\n",
            "\n",
            "model_b64 = base64.b64encode(glb_data).decode('utf-8')\n",
            "\n",
            "print(f\"✅ Model Generation Complete! GLB Size: {len(glb_data)/1024:.2f} KB\")\n",
            "print(f\"Centered at: ({center_x:.2f}, {center_y:.2f})\")\n"
        ]
        break

with open('pipeline_new.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated.")
