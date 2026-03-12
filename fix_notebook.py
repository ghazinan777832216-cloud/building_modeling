import json
import os

print("Updating the viewer cell in pipeline_new.ipynb...")
with open('pipeline_new.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

found = False
# Search from the end as it's usually the last cell
for i in range(len(nb['cells']) - 1, -1, -1):
    cell = nb['cells'][i]
    if cell['cell_type'] == 'code':
        source_str = ''.join(cell.get('source', []))
        if 'html_code =' in source_str and 'viewer-v15' in source_str:
            print(f"Found target cell at index {i}")
            
            new_source = [
                "import os\n",
                "import webbrowser\n",
                "from IPython.display import display, HTML\n",
                "\n",
                "# كود الـ HTML للفيوور المطور\n",
                "html_template = \"\"\"<!DOCTYPE html>\n",
                "<html>\n",
                "<head>\n",
                "    <title>CityEngine Viewer (External)</title>\n",
                "    <meta charset=\\\"utf-8\\\">\n",
                "    <style>\n",
                "        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; }\n",
                "        #viewer-v15 { width: 100%; height: 100vh; background: linear-gradient(#f0f0f0, #c0c0c0); }\n",
                "        #log-v15 { position: absolute; top: 10px; left: 10px; color: #000; background: rgba(224, 224, 224, 0.8); padding: 10px; font-family: monospace; font-size: 12px; font-weight: bold; border-radius: 5px; z-index: 100; }\n",
                "    </style>\n",
                "    <link rel=\"stylesheet\" href=\"https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css\" type=\"text/css\">\n",
                "    <script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>\n",
                "    <script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js'></script>\n",
                "</head>\n",
                "<body>\n",
                "    <div id='viewer-v15'></div>\n",
                "    <div id='log-v15'>Initializing Authentic CityEngine Viewer...</div>\n",
                "\n",
                "    <script>\n",
                "    (function() {\n",
                "        const log = (m) => document.getElementById('log-v15').innerText = '> ' + m;\n",
                "        \n",
                "        function b64ToBlob(b64) {\n",
                "            const bin = atob(b64);\n",
                "            const buf = new Uint8Array(bin.length);\n",
                "            for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);\n",
                "            return new Blob([buf], {type: 'model/gltf-binary'});\n",
                "        }\n",
                "\n",
                "        function start() {\n",
                "            if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {\n",
                "                setTimeout(start, 500); return;\n",
                "            }\n",
                "            \n",
                "            Autodesk.Viewing.Initializer({ env: 'Local' }, function() {\n",
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
                "                const url = URL.createObjectURL(b64ToBlob(\"{{MODEL_B64}}\"));\n",
                "                viewer.loadModel(url + '#.glb', { fileExt: 'glb' }, () => {\n",
                "                    log('CityEngine Procedural Building Loaded Successfully.');\n",
                "                    viewer.fitToView();\n",
                "                });\n",
                "            });\n",
                "        }\n",
                "        start();\n",
                "    })();\n",
                "    </script>\n",
                "</body>\n",
                "</html>\n",
                "\"\"\"\n",
                "\n",
                "final_html = html_template.replace(\"{{MODEL_B64}}\", model_b64)\n",
                "\n",
                "# حفظ الملف\n",
                "html_filename = \"viewer_v15.html\"\n",
                "with open(html_filename, \"w\", encoding=\"utf-8\") as f:\n",
                "    f.write(final_html)\n",
                "\n",
                "full_path = os.path.abspath(html_filename)\n",
                "webbrowser.open('file:///' + full_path.replace('\\\\', '/'))\n",
                "\n",
                "display(HTML(f\"\"\"\n",
                "<div style='background-color: #f8f9fa; border-left: 5px solid #28a745; padding: 20px; border-radius: 5px; font-family: sans-serif;'>\n",
                "    <h3 style='color: #28a745; margin-top: 0;'>✨ تم تحديث وعرض الموديل!</h3>\n",
                "    <p>تم فتح الفيوور في متصفح خارجي لضمان الأداء السلس وبدون لاق.</p>\n",
                "    <div style='margin-top: 15px;'>\n",
                "        <a href='viewer_v15.html' target='_blank' style='background-color: #007bff; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;'>\n",
                "            🚀 فتح الفيوور في صفحة مستقلة جديـدة\n",
                "        </a>\n",
                "    </div>\n",
                "    <p style='color: #6c757d; font-size: 13px; margin-top: 15px;'>ملاحظة: إذا لم يفتح المتصفح تلقائياً، يمكنك النقر على الزر أعلاه.</p>\n",
                "</div>\n",
                "\"\"\"))\n"
            ]
            cell['source'] = new_source
            found = True
            break

if found:
    with open('pipeline_new.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated successfully!")
else:
    print("Error: Could not find the cell with 'html_code =' and 'viewer-v15'")
