import json
import os

notebook_path = r'c:\\Users\\hisham\\Desktop\\building_modeling\\pipeline_new.ipynb'

print(f"Opening {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")

new_source = [
    "from IPython.display import HTML, display\n",
    "\n",
    "html_code = f\"\"\"\n",
    "<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>\n",
    "<div id='viewer-v14' style='width:100%; height:600px; background: linear-gradient(#202020, #444); border-radius:10px;'></div>\n",
    "<div id='log-v14' style='color:#0f0; background:#000; padding:5px; font-family:monospace; font-size:11px;'>Initializing Viewer...</div>\n",
    "\n",
    "<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>\n",
    "<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js'></script>\n",
    "\n",
    "<script>\n",
    "(function() {{\n",
    "    const log = (m) => document.getElementById('log-v14').innerText = '> ' + m;\n",
    "    \n",
    "    function b64ToBlob(b64) {{\n",
    "        const bin = atob(b64);\n",
    "        const buf = new Uint8Array(bin.length);\n",
    "        for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);\n",
    "        return new Blob([buf], {{type: 'model/gltf-binary'}});\n",
    "    }}\n",
    "\n",
    "    function start() {{\n",
    "        if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing.Extensions === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {{\n",
    "            setTimeout(start, 500); return;\n",
    "        }}\n",
    "        \n",
    "        Autodesk.Viewing.Initializer({{ env: 'Local' }}, function() {{\n",
    "            const viewerDiv = document.getElementById('viewer-v14');\n",
    "            const viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);\n",
    "            viewer.start();\n",
    "            \n",
    "            viewer.loadExtension('Autodesk.glTF').then(() => {{\n",
    "                log('Extension glTF Loaded.');\n",
    "                viewer.setTheme('dark-theme');\n",
    "                \n",
    "                const url = URL.createObjectURL(b64ToBlob(\"{model_b64}\"));\n",
    "                viewer.loadModel(url, {{ fileExt: 'glb', modelName: 'model.glb' }}, () => {{\n",
    "                    log('Model Loaded Successfully.');\n",
    "                    viewer.setLightPreset(4); \n",
    "                    viewer.setEnvMapBackground(false);\n",
    "                    viewer.fitToView();\n",
    "                }}, (errCode, errMsg) => {{\n",
    "                    log('Load Error ' + errCode + ': ' + errMsg);\n",
    "                }});\n",
    "            }}).catch(err => {{\n",
    "                log('Extension Load Error: ' + err);\n",
    "            }});\n",
    "        }});\n",
    "    }}\n",
    "    start();\n",
    "}})();\n",
    "</script>\n",
    "\"\"\"\n",
    "display(HTML(html_code))\n"
]

target_cell_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        concat_source = "".join(cell.get('source', []))
        if 'html_code' in concat_source and 'Autodesk' in concat_source:
            target_cell_index = i
            break

if target_cell_index != -1:
    print(f"Found target cell at index {target_cell_index}")
    nb['cells'][target_cell_index]['source'] = new_source
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f)
    print("Write complete.")
else:
    print("Could not find the viewer cell.")
