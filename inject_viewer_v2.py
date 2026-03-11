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
    "<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #eee; border: 1px solid #ccc;'>\n",
    "    <div id='viewer' style='width:100%; height:100%'></div>\n",
    "    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:white; font-size:12px; padding:5px; max-height:150px; overflow-y:auto; z-index:1000;'>\n",
    "        Diagnostic Log: Initializing...\n",
    "    </div>\n",
    "</div>\n",
    "\n",
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
    "            log('Wait: Loading Autodesk library...');\n",
    "            setTimeout(initViewer, 1000);\n",
    "            return;\n",
    "        }}\n",
    "\n",
    "        var options = {{\n",
    "            env: 'Local',\n",
    "            useADP: false\n",
    "        }};\n",
    "\n",
    "        log('Initializing Initializer...');\n",
    "        Autodesk.Viewing.Initializer(options, function() {{\n",
    "            try {{\n",
    "                var viewerDiv = document.getElementById('viewer');\n",
    "                var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);\n",
    "                \n",
    "                log('Starting Viewer instance...');\n",
    "                var startedCode = viewer.start();\n",
    "                \n",
    "                if (startedCode > 0) {{\n",
    "                    log('Error: Start failed with code ' + startedCode);\n",
    "                    return;\n",
    "                }}\n",
    "                \n",
    "                log('Viewer started. Processing glTF...');\n",
    "                var gltfDataRaw = {model_data_raw};\n",
    "                var gltfParsed = (typeof gltfDataRaw === 'string') ? JSON.parse(gltfDataRaw) : gltfDataRaw;\n",
    "                \n",
    "                log('JSON Parsed. Creating Blob...');\n",
    "                var blob = new Blob([JSON.stringify(gltfParsed)], {{type: 'application/json'}});\n",
    "                var url = URL.createObjectURL(blob);\n",
    "                \n",
    "                log('Loading Model from: ' + url);\n",
    "                viewer.loadModel(url, {{}}, function(model) {{\n",
    "                    log('SUCCESS: Model loaded!');\n",
    "                    // logDiv.style.opacity = '0.3'; // Fade out log\n",
    "                }}, function(errorCode, errorMsg) {{\n",
    "                    log('LOAD ERROR: ' + errorCode + ' - ' + errorMsg);\n",
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

# Specifically target the cell that contains HTML(...) or pythreejs or the one at index 9
found = False
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and ('HTML(html_code)' in cell.source or 'pythreejs' in cell.source):
        cell.source = "".join(new_code)
        found = True
        print(f"Updated cell at index {i}")

if not found:
    # Fallback to index 9 if common patterns not found
    nb.cells[9].source = "".join(new_code)
    print("Fallback updated cell at index 9")

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook update script finished.")
