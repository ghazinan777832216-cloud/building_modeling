import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'

print(f"Opening {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_source = [
    "from IPython.display import HTML, display\n",
    "\n",
    "html_code = f\"\"\"\n",
    "<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>\n",
    "<div id='viewer-v19' style='position: relative; width:100%; height:600px; background: linear-gradient(#202020, #444); border-radius:10px; overflow: hidden;'></div>\n",
    "<div id='log-v19' style='color:#0f0; background:#000; padding:5px; font-family:monospace; font-size:11px;'>Initializing High-Quality Mode...</div>\n",
    "\n",
    "<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>\n",
    "<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/extensions/glTF/glTF.min.js'></script>\n",
    "\n",
    "<script>\n",
    "(function() {{\n",
    "    const log = (m) => document.getElementById('log-v19').innerText = '> ' + m;\n",
    "    \n",
    "    function b64ToBlob(b64) {{\n",
    "        const bin = atob(b64);\n",
    "        const buf = new Uint8Array(bin.length);\n",
    "        for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);\n",
    "        return new Blob([buf], {{type: 'model/gltf-binary'}});\n",
    "    }}\n",
    "\n",
    "    function start() {{\n",
    "        if (typeof Autodesk === 'undefined' || typeof Autodesk.Viewing === 'undefined' || typeof Autodesk.Viewing.Extensions === 'undefined' || typeof Autodesk.Viewing.Extensions.glTF === 'undefined') {{\n",
    "            setTimeout(start, 500); return;\n",
    "        }}\n",
    "        \n",
    "        Autodesk.Viewing.Initializer({{ env: 'Local' }}, function() {{\n",
    "            const viewerDiv = document.getElementById('viewer-v19');\n",
    "            // We can disable some post-processing that might clash with local unlit models\n",
    "            const viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv, {{ extensions: ['Autodesk.glTF'] }});\n",
    "            viewer.start();\n",
    "            \n",
    "            viewer.loadExtension('Autodesk.glTF').then(() => {{\n",
    "                log('Extension glTF Loaded.');\n",
    "                viewer.setTheme('dark-theme');\n",
    "                \n",
    "                const url = URL.createObjectURL(b64ToBlob(\"{model_b64}\"));\n",
    "                viewer.loadModel(url, {{ fileExt: 'glb', modelName: 'model.glb' }}, () => {{\n",
    "                    log('Model Loaded with Textures and Environmental Light.');\n",
    "                    \n",
    "                    // Inject Three.js Lights to fix black model issue safely \n",
    "                    try {\n",
    "                        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);\n",
    "                        const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);\n",
    "                        dirLight.position.set(100, 200, 100).normalize();\n",
    "                        viewer.impl.scene.add(ambientLight);\n",
    "                        viewer.impl.scene.add(dirLight);\n",
    "                        viewer.impl.sceneUpdated(true);\n",
    "                    } catch (e) { log('Light injection error: ' + e); }\n",
    "                    \n",
    "                    viewer.setLightPreset(0); \n",
    "                    viewer.fitToView();\n",
    "                    viewer.impl.invalidate(true, true, true);\n",
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
        if 'Autodesk' in concat_source and 'html_code' in concat_source:
             target_cell_index = i

if target_cell_index != -1:
    print(f"Found target cell at index {target_cell_index}")
    nb['cells'][target_cell_index]['source'] = new_source
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Write complete.")
else:
    print("Could not find the viewer cell.")
