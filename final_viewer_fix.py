import nbformat
import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

new_code = [
    "from IPython.display import HTML, display\n",
    "import json\n",
    "\n",
    "try:\n",
    "    gltf_list\n",
    "    if not gltf_list or not gltf_list[0]:\n",
    "         raise Exception(\"gltf_list موجودة ولكنها فارغة. تأكد من نجاح توليد النموذج.\")\n",
    "except NameError:\n",
    "    raise Exception(\"لم يتم توليد gltf_list بعد. نفّذ الخلية السابقة أولاً.\")\n",
    "\n",
    "# تحويل بيانات glTF إلى JSON\n",
    "try:\n",
    "    if isinstance(gltf_list[0], str):\n",
    "        model_data_raw = gltf_list[0]\n",
    "    else:\n",
    "        model_data_raw = json.dumps(gltf_list[0])\n",
    "except Exception as e:\n",
     "     raise Exception(f\"خطأ في تحويل gltf_list[0] إلى JSON: {str(e)}\")\n",
    "\n",
    "html_code = f\"\"\"\n",
    "<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #333; border: 1px solid #555; border-radius: 8px; overflow: hidden;'>\n",
    "    <div id='viewer' style='width:100%; height:100%'></div>\n",
    "    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.85); color:#0f0; font-family:monospace; font-size:11px; padding:8px; max-height:150px; overflow-y:auto; z-index:1000; border-top: 1px solid #444;'>\n",
    "        [System] Initializing Diagnostic Viewer v5...\n",
    "    </div>\n",
    "</div>\n",
    "\n",
    "<!-- Load Autodesk Viewer Scripts -->\n",
    "<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>\n",
    "<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>\n",
    "\n",
    "<script>\n",
    "(function() {{\n",
    "    var logDiv = document.getElementById('viewer-log');\n",
    "    function log(msg) {{\n",
    "        console.log('[Viewer]', msg);\n",
    "        var p = document.createElement('div');\n",
    "        p.textContent = '> ' + msg;\n",
    "        logDiv.appendChild(p);\n",
    "        logDiv.scrollTop = logDiv.scrollHeight;\n",
    "    }}\n",
    "\n",
    "    function initViewer() {{\n",
    "        if (typeof Autodesk === 'undefined') {{\n",
    "            log('Waiting for Autodesk library...');\n",
    "            setTimeout(initViewer, 1000);\n",
    "            return;\n",
    "        }}\n",
    "\n",
    "        var options = {{\n",
    "            env: 'Local',\n",
    "            useADP: false\n",
    "        }};\n",
    "\n",
    "        log('Initializing Autodesk.Viewing...');\n",
    "        Autodesk.Viewing.Initializer(options, function() {{\n",
    "            try {{\n",
    "                var viewerDiv = document.getElementById('viewer');\n",
    "                var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);\n",
    "                \n",
    "                log('Starting viewer instance...');\n",
    "                var startedCode = viewer.start();\n",
    "                \n",
    "                if (startedCode > 0) {{\n",
    "                    log('FAIL: Viewer start failed code ' + startedCode);\n",
    "                    return;\n",
    "                }}\n",
    "                \n",
    "                log('Processing Model Data...');\n",
    "                var gltfDataRaw = {model_data_raw};\n",
    "                var gltfParsed = (typeof gltfDataRaw === 'string') ? JSON.parse(gltfDataRaw) : gltfDataRaw;\n",
    "                \n",
    "                log('Creating Blob from JSON...');\n",
    "                var blob = new Blob([JSON.stringify(gltfParsed)], {{type: 'application/json'}});\n",
    "                \n",
    "                // FORCE VIRTUAL EXTENSION VIA HASH\n",
    "                var url = URL.createObjectURL(blob) + '#.gltf';\n",
    "                \n",
    "                log('Loading Model URL: ' + url);\n",
    "                \n",
    "                // CRITICAL FIX: Explicitly tell the viewer this IS a gltf file\n",
    "                var loadOptions = {{\n",
    "                    fileExt: 'gltf',\n",
    "                    loadAsExtension: 'gltf'\n",
    "                }};\n",
    "\n",
    "                viewer.loadModel(url, loadOptions, function(model) {{\n",
    "                    log('SUCCESS: Model loaded into scene!');\n",
    "                    setTimeout(function() {{ \n",
    "                        logDiv.style.background = 'rgba(0,40,0,0.5)'; \n",
    "                        logDiv.innerText = 'OK: Model Visible';\n",
    "                    }}, 2000);\n",
    "                }}, function(errorCode, errorMsg) {{\n",
    "                    log('ERROR ' + errorCode + ': ' + errorMsg);\n",
    "                    if (errorCode == 13) {{\n",
    "                         log('RETRY: Using alternative loading method...');\n",
    "                         viewer.loadModel(url, {{ fileExt: \"gltf\" }}, null, null);\n",
    "                    }}\n",
    "                }});\n",
    "                \n",
    "            }} catch (err) {{\n",
    "                log('JS EXCEPTION: ' + err.message);\n",
    "                console.error(err);\n",
    "            }}\n",
    "        }});\n",
    "    }}\n",
    "\n",
    "    setTimeout(initViewer, 500);\n",
    "}})();\n",
    "</script>\n",
    "\"\"\"\n",
    "\n",
    "display(HTML(html_code))"
]

# Update BOTH notebooks to be ultra-sure
for path in [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb_temp = nbformat.read(f, as_version=4)
        
        updated = False
        for cell in nb_temp.cells:
            if cell.cell_type == 'code' and ('Diagnostic Log' in cell.source or 'viewer-log' in cell.source):
                cell.source = "".join(new_code)
                updated = True
        
        if not updated:
             # If diagnostic viewer not found, it must be the pythreejs one or similar
             for cell in nb_temp.cells:
                 if cell.cell_type == 'code' and ('HTML(html_code)' in cell.source or 'pythreejs' in cell.source):
                     cell.source = "".join(new_code)
                     updated = True
        
        if updated:
            with open(path, 'w', encoding='utf-8') as f:
                nbformat.write(nb_temp, f)
            print(f"Successfully updated {path}")
    except Exception as e:
        print(f"Error updating {path}: {e}")

print("Update completed.")
