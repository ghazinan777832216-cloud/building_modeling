import nbformat
import json

notebook_path = r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

new_code = r"""from IPython.display import HTML, display
import json

try:
    gltf_list
    if not gltf_list or not gltf_list[0]:
         raise Exception("gltf_list موجودة ولكنها فارغة. تأكد من نجاح توليد النموذج.")
except NameError:
    raise Exception("لم يتم توليد gltf_list بعد. نفّذ الخلية السابقة أولاً.")

# تحويل بيانات glTF إلى JSON
try:
    if isinstance(gltf_list[0], str):
        model_data_raw = gltf_list[0]
    else:
        model_data_raw = json.dumps(gltf_list[0])
except Exception as e:
     raise Exception(f"خطأ في تحويل gltf_list[0] إلى JSON: {str(e)}")

html_code = f"""
<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #eee; border: 1px solid #ccc;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.8); color:white; font-size:12px; padding:5px; max-height:150px; overflow-y:auto; z-index:1000;'>
        Diagnostic Log: Initializing...
    </div>
</div>

<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
(function() {{
    var logDiv = document.getElementById('viewer-log');
    function log(msg) {{
        console.log('[Viewer]', msg);
        var p = document.createElement('div');
        p.textContent = '> ' + msg;
        logDiv.appendChild(p);
        logDiv.scrollTop = logDiv.scrollHeight;
    }}

    function initViewer() {{
        if (typeof Autodesk === 'undefined') {{
            log('Wait: Loading Autodesk library...');
            setTimeout(initViewer, 1000);
            return;
        }}

        var options = {{
            env: 'Local',
            useADP: false
        }};

        log('Initializing Initializer...');
        Autodesk.Viewing.Initializer(options, function() {{
            try {{
                var viewerDiv = document.getElementById('viewer');
                var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
                
                log('Starting Viewer instance...');
                var startedCode = viewer.start();
                
                if (startedCode > 0) {{
                    log('Error: Start failed with code ' + startedCode);
                    return;
                }}
                
                log('Viewer started. Processing glTF...');
                var gltfDataRaw = {model_data_raw};
                var gltfParsed = (typeof gltfDataRaw === 'string') ? JSON.parse(gltfDataRaw) : gltfDataRaw;
                
                log('JSON Parsed. Creating Blob...');
                var blob = new Blob([JSON.stringify(gltfParsed)], {{type: 'application/json'}});
                
                // FORCE THE URL TO END WITH .gltf
                var url = URL.createObjectURL(blob) + '#/model.gltf';
                
                log('Loading Model from: ' + url);
                
                // Triple-checking options
                var loadOptions = {{
                    loadAsExtension: 'gltf',
                    fileExt: 'gltf'
                }};

                viewer.loadModel(url, loadOptions, function(model) {{
                    log('SUCCESS: Model loaded!');
                    setTimeout(function() {{ logDiv.style.opacity = '0.3'; }}, 5000);
                }}, function(errorCode, errorMsg) {{
                    log('LOAD ERROR: ' + errorCode + ' - ' + errorMsg);
                    if (errorCode == 13) {{
                         log('Suggestion: Adding model.gltf suffix to Blob URL did not help. Trying loadExtension generic...');
                    }}
                }});
                
            }} catch (err) {{
                log('JS EXCEPTION: ' + err.message);
                console.error(err);
            }}
        }});
    }}

    setTimeout(initViewer, 500);
}})();
</script>
"""

display(HTML(html_code))"""

found = False
for cell in nb.cells:
    if cell.cell_type == 'code' and 'Diagnostic Log' in cell.source:
        cell.source = new_code
        found = True

if not found:
    nb.cells[9].source = new_code

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook update script finished.")
