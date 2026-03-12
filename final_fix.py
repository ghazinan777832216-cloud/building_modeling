import json
import os

print("Applying final fixes to coordinate centering and viewer enhancements...")

with open('pipeline_new.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Update Cell 3 (Generation & Centering)
found_cell3 = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'pyprt.InitialShape' in ''.join(cell.get('source', [])):
        print("Updating Cell 3 (Centering logic)...")
        cell['source'] = [
            "import pyprt, os, base64\n",
            "import numpy as np\n",
            "\n",
            "pyprt.initialize_prt()\n",
            "\n",
            "# إخراج الإحداثيات للمبنى مع التوسيط (Centering) لتجنب مشاكل العرض\n",
            "coords_2d = list(utm_polygon.exterior.coords)[:-1]\n",
            "\n",
            "# حساب المركز (Centroid) لجعل الموديل حول نقطة الصفر (0,0,0)\n",
            "center_x = sum(c[0] for c in coords_2d) / len(coords_2d)\n",
            "center_y = sum(c[1] for c in coords_2d) / len(coords_2d)\n",
            "\n",
            "flat_coords = []\n",
            "for x, y in coords_2d:\n",
            "    # طرح المركز من كل إحداثي\n",
            "    flat_coords.extend([x - center_x, 0.0, y - center_y])\n",
            "\n",
            "initial_shape = pyprt.InitialShape(flat_coords)\n",
            "attributes = {\"Nbr_of_Floors\": 12, \"Usage\": \"Residential\"}\n",
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
            "    \"baseName\": \"procedural_building\"\n",
            "}\n",
            "\n",
            "# توليد المبنى\n",
            "model_generator.generate_model([attributes], RPK_PATH, encoder, encoder_options)\n",
            "\n",
            "# قراءة الملف وتحويله لـ Base64\n",
            "glb_path = os.path.join(out_dir, \"procedural_building_0.glb\")\n",
            "with open(glb_path, \"rb\") as f:\n",
            "    glb_data = f.read()\n",
            "\n",
            "model_b64 = base64.b64encode(glb_data).decode('utf-8')\n",
            "\n",
            "print(f\"✅ Model Centered at (0,0) and Ready!\")\n",
            "print(f\"Shifted by: X={center_x:.2f}, Y={center_y:.2f}\")\n"
        ]
        found_cell3 = True
        break

# 2. Update Cell 4 (Enhanced Viewer)
found_cell4 = False
for cell in nb['cells']:
    source_str = ''.join(cell.get('source', []))
    if cell['cell_type'] == 'code' and 'webbrowser.open' in source_str:
        print("Updating Cell 4 (Enhanced Viewer)...")
        cell['source'] = [
            "import os\n",
            "import webbrowser\n",
            "from IPython.display import display, HTML\n",
            "\n",
            "# كود الـ HTML المطور مع تحسينات الإضاءة والكاميرا\n",
            "html_template = \"\"\"<!DOCTYPE html>\n",
            "<html>\n",
            "<head>\n",
            "    <title>CityEngine Professional Viewer</title>\n",
            "    <meta charset=\\\"utf-8\\\">\n",
            "    <meta name=\\\"viewport\\\" content=\\\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\\\">\n",
            "    <style>\n",
            "        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }\n",
            "        #viewer-v15 { width: 100%; height: 100vh; background: #2b2b2b; }\n",
            "        #ui-overlay { position: absolute; top: 20px; left: 20px; z-index: 100; pointer-events: none; }\n",
            "        .status-badge { background: rgba(0, 0, 0, 0.7); color: white; padding: 12px 20px; border-radius: 8px; border-left: 4px solid #0076d1; backdrop-filter: blur(5px); }\n",
            "        #log-v15 { font-size: 14px; font-weight: 500; font-family: monospace; }\n",
            "    </style>\n",
            "    <link rel=\\\"stylesheet\\\" href=\\\"https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css\\\" type=\\\"text/css\\\">\n",
            "    <script src=\\\"https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js\\\"></script>\n",
            "    <script src=\\\"https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js\\\"></script>\n",
            "</head>\n",
            "<body>\n",
            "    <div id='viewer-v15'></div>\n",
            "    <div id='ui-overlay'>\n",
            "        <div class='status-badge'>\n",
            "            <div id='log-v15'>Loading 3D Scene...</div>\n",
            "        </div>\n",
            "    </div>\n",
            "\n",
            "    <script>\n",
            "    (function() {\n",
            "        const status = (m) => document.getElementById('log-v15').innerHTML = '📡 ' + m;\n",
            "        \n",
            "        function b64ToBlob(b64) {\n",
            "            const bin = atob(b64);\n",
            "            const buf = new Uint8Array(bin.length);\n",
            "            for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);\n",
            "            return new Blob([buf], {type: 'model/gltf-binary'});\n",
            "        }\n",
            "\n",
            "        function initViewer() {\n",
            "            if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {\n",
            "                setTimeout(initViewer, 300); return;\n",
            "            }\n",
            "            \n",
            "            const options = { env: 'Local', skipPropertyDb: true };\n",
            "            \n",
            "            Autodesk.Viewing.Initializer(options, function() {\n",
            "                const container = document.getElementById('viewer-v15');\n",
            "                const viewer = new Autodesk.Viewing.GuiViewer3D(container);\n",
            "                viewer.start();\n",
            "                \n",
            "                // Settings for High Visual Quality\n",
            "                viewer.setTheme('dark-theme');\n",
            "                viewer.setEnvMapBackground(true);\n",
            "                viewer.setLightPreset(1); // Plaza / Outdoor\n",
            "                viewer.setQualityLevel(true, true); // Ambient shadows + AA\n",
            "                viewer.setGroundShadow(true);\n",
            "                \n",
            "                const modelData = \"{{MODEL_B64}}\";\n",
            "                const blob = b64ToBlob(modelData);\n",
            "                const url = URL.createObjectURL(blob);\n",
            "                \n",
            "                viewer.loadModel(url + '#.glb', { fileExt: 'glb' }, \n",
            "                    (model) => {\n",
            "                        status('<span style=\"color:#4caf50\">Building Loaded Successfully!</span>');\n",
            "                        \n",
            "                        // Focus view on the model\n",
            "                        setTimeout(() => {\n",
            "                            viewer.fitToView();\n",
            "                            viewer.navigation.toDefaultView();\n",
            "                        }, 500);\n",
            "                    }, \n",
            "                    (err) => {\n",
            "                        status('<span style=\"color:#f44336\">Error: ' + err + '</span>');\n",
            "                        console.error(err);\n",
            "                    }\n",
            "                );\n",
            "            });\n",
            "        }\n",
            "        initViewer();\n",
            "    })();\n",
            "    </script>\n",
            "</body>\n",
            "</html>\n",
            "\"\"\"\n",
            "\n",
            "final_html = html_template.replace(\"{{MODEL_B64}}\", model_b64)\n",
            "\n",
            "html_filename = \"viewer_final.html\"\n",
            "with open(html_filename, \"w\", encoding=\"utf-8\") as f:\n",
            "    f.write(final_html)\n",
            "\n",
            "full_path = os.path.abspath(html_filename)\n",
            "webbrowser.open('file:///' + full_path.replace('\\\\', '/'))\n",
            "\n",
            "display(HTML(f\"\"\"\n",
            "<div style='border: 2px solid #0076d1; background: #f0f7ff; padding: 25px; border-radius: 12px; font-family: system-ui; text-align: center;'>\n",
            "    <h2 style='color: #0076d1; margin-bottom: 5px;'>🚀 تم تحسين الفيوور بنجاح!</h2>\n",
            "    <p style='color: #444; font-size: 16px;'>تمت معالجة إحداثيات الموديل (Centering) لضمان ظهوره بوضوح تام.</p>\n",
            "    <a href='viewer_final.html' target='_blank' \n",
            "       style='background: #0076d1; color: white; padding: 15px 30px; text-decoration: none; border-radius: 30px; font-weight: bold; display: inline-block; margin-top: 15px; box-shadow: 0 4px 15px rgba(0,118,209,0.3); transition: transform 0.2s;'>\n",
            "       👁️ فتح المشهد ثلاثي الأبعاد المطور\n",
            "    </a>\n",
            "    <p style='color: #777; font-size: 13px; margin-top: 20px;'>ملاحظة: تأكد من تشغيل الخلية 3 قبل تشغيل هذه الخلية.</p>\n",
            "</div>\n",
            "\"\"\"))\n"
        ]
        found_cell4 = True
        break

if found_cell3 and found_cell4:
    with open('pipeline_new.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated with final fixes!")
else:
    print(f"Error: Found Cell 3: {found_cell3}, Found Cell 4: {found_cell4}")
