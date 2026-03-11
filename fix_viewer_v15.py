import json
import base64

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The viewer cell is the last non-empty code cell
viewer_cell_index = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'html_code' in ''.join(cell['source']):
        viewer_cell_index = i
        break

if viewer_cell_index != -1:
    source = nb['cells'][viewer_cell_index]['source']
    # We want to replace the html_code string construction
    # Find the line where html_code starts
    start_line = -1
    for j, line in enumerate(source):
        if 'html_code = f"""' in line:
            start_line = j
            break
    
    if start_line != -1:
        new_source = source[:start_line+1]
        new_html_content = [
            "<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>\n",
            "<div id='viewer-v14' style='width:100%; height:600px; background: linear-gradient(#202020, #444); border-radius:10px;'></div>\n",
            "<div id='log-v14' style='color:#0f0; background:#000; padding:5px; font-family:monospace; font-size:11px;'>Initializing High-Quality Mode...</div>\n",
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
            "            const viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('viewer-v14'));\n",
            "            viewer.start();\n",
            "            \n",
            "            // Loading glTF extension explicitly\n",
            "            viewer.loadExtension('Autodesk.glTF').then(() => {{\n",
            "                log('glTF Extension Loaded.');\n",
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
            "</script>\n"
        ]
        # Find where the triple quotes end
        end_line = -1
        for k in range(start_line + 1, len(source)):
            if '"""' in source[k]:
                end_line = k
                break
        
        if end_line != -1:
            nb['cells'][viewer_cell_index]['source'] = source[:start_line+1] + new_html_content + source[end_line:]
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1)
            print("Successfully updated the notebook.")
        else:
            print("Could not find end of html_code string.")
    else:
        print("Could not find start of html_code string.")
else:
    print("Could not find viewer cell.")
