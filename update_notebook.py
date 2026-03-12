 import json
import os

print("Loading notebook...")
with open('pipeline_new.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

found = False
for i, cell in enumerate(nb['cells']):
    source_str = ''.join(cell.get('source', []))
    if cell['cell_type'] == 'code' and 'html_code =' in source_str and 'Autodesk.Viewing' in source_str:
        print(f"Found cell at index {i}")
        found = True
        code_cell = cell
        
        new_source = [
            "import os\n",
            "import webbrowser\n",
            "from IPython.display import display, HTML\n",
            "\n",
            "html_code = f\"\"\"<!DOCTYPE html>\n",
            "<html>\n",
            "<head>\n",
            "    <title>CityEngine Viewer</title>\n",
            "    <meta charset=\\\"utf-8\\\">\n",
            "    <style>\n",
            "        body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }}\n",
            "        #viewer-v15 {{ width: 100%; height: 100vh; background: linear-gradient(#f0f0f0, #c0c0c0); }}\n",
            "        #log-v15 {{ position: absolute; top: 10px; left: 10px; color: #000; background: rgba(224, 224, 224, 0.8); padding: 10px; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 5px; z-index: 100; pointer-events: none; }}\n",
            "    </style>\n",
            "    <!-- Load Autodesk Viewer library -->\n",
            "    <link rel=\"stylesheet\" href=\"https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css\" type=\"text/css\">\n",
            "    <script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>\n",
            "    <script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js'></script>\n",
            "</head>\n",
            "<body>\n",
            "    <div id='viewer-v15'></div>\n",
            "    <div id='log-v15'>Initializing Authentic CityEngine Viewer...</div>\n",
            "\n",
            "    <script>\n",
            "    (function() {{\n",
            "        const log = (m) => document.getElementById('log-v15').innerText = '> ' + m;\n",
            "        \n",
            "        function b64ToBlob(b64) {{\n",
            "            const bin = atob(b64);\n",
            "            const buf = new Uint8Array(bin.length);\n",
            "            for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);\n",
            "            return new Blob([buf], {{type: 'model/gltf-binary'}});\n",
            "        }}\n",
            "\n",
            "        function start() {{\n",
            "            if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {{\n",
            "                setTimeout(start, 500); return;\n",
            "            }}\n",
            "            \n",
            "            Autodesk.Viewing.Initializer({{ env: 'Local' }}, function() {{\n",
            "                const viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('viewer-v15'));\n",
            "                viewer.start();\n",
            "                \n",
            "                viewer.setTheme('light-theme');\n",
            "                viewer.setEnvMapBackground(true);\n",
            "                viewer.setLightPreset(2);\n",
            "                viewer.setQualityLevel(false, true);\n",
            "                viewer.prefs.set('groundShadow', true);\n",
            "                viewer.prefs.set('groundReflection', false);\n",
            "                \n",
            "                const url = URL.createObjectURL(b64ToBlob(\"{model_b64}\"));\n",
            "                viewer.loadModel(url + '#.glb', {{ fileExt: 'glb' }}, () => {{\n",
            "                    log('CityEngine Procedural Building Loaded Successfully.');\n",
            "                    viewer.fitToView();\n",
            "                }});\n",
            "            }});\n",
            "        }}\n",
            "        start();\n",
            "    }})();\n",
            "    </script>\n",
            "</body>\n",
            "</html>\n",
            "\"\"\"\n",
            "\n",
            "# حفظ الكود كملف HTML مستقل لفتحه في المتصفح وتجنب لاق النوت بوك\n",
            "html_path = os.path.join(os.getcwd(), \"viewer.html\")\n",
            "with open(html_path, \"w\", encoding=\"utf-8\") as f:\n",
            "    f.write(html_code)\n",
            "\n",
            "# فتح المتصفح التلقائي\n",
            "webbrowser.open('file:///' + html_path.replace('\\\\', '/'))\n",
            "\n",
            "# عرض رسالة ورابط في النوت بوك\n",
            "display(HTML(f\"\"\"\n",
            "<h3>✅ تم إنشاء الفيوور!</h3>\n",
            "<p style='font-size: 16px; color: #333;'>تم استخراج الفيوور ليعمل في المتصفح لتجنب البطء واللاق في جوبيتر.</p>\n",
            "<div style='margin-top: 15px;'>\n",
            "    <a href='viewer.html' target='_blank' style='background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;'>\n",
            "        🌐 انقر هنا لفتح الفيوور في صفحة مستقلة\n",
            "    </a>\n",
            "</div>\n",
            "\"\"\"))\n"
        ]
        code_cell['source'] = new_source
        break

if found:
    print("Writing notebook...")
    with open('pipeline_new.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated!")
else:
    print("Cell not found!")
