import nbformat
import json

paths = [r'c:\Users\hisham\Desktop\building_modeling\pipeline.ipynb', r'c:\Users\hisham\Desktop\building_modeling\pipeline_new.ipynb']

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

html_code = f\"\"\"
<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #333; border: 1px solid #555; border-radius: 8px; overflow: hidden;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    
    <!-- UI Controls -->
    <div style='position:absolute; top:10px; left:10px; z-index:1001; display:flex; gap:5px;'>
        <button onclick='focusModel()' style='background:#06f; color:white; border:none; padding:8px 15px; border-radius:4px; cursor:pointer; font-weight:bold; box-shadow:0 2px 5px rgba(0,0,0,0.3);'>
            🎯 Focus on Model (Fly To)
        </button>
        <button onclick='resetCamera()' style='background:#555; color:white; border:none; padding:8px 15px; border-radius:4px; cursor:pointer;'>
            🏠 Home View
        </button>
    </div>

    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.85); color:#0f0; font-family:monospace; font-size:11px; padding:8px; max-height:150px; overflow-y:auto; z-index:1000; border-top: 1px solid #444;'>
        [System] Initializing Diagnostic Viewer v6 (Fly-To Support)...
    </div>
</div>

<!-- Load Autodesk Viewer Scripts -->
<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
var globalViewer = null;

function focusModel() {{
    if (globalViewer) {{
        log('Executing Fit to View...');
        globalViewer.viewSelected();
        globalViewer.fitToView();
    }}
}}

function resetCamera() {{
    if (globalViewer) {{
        globalViewer.autocam.goHome();
    }}
}}

function log(msg) {{
    console.log('[Viewer]', msg);
    var logDiv = document.getElementById('viewer-log');
    var p = document.createElement('div');
    p.textContent = '> ' + msg;
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
}}

(function() {{
    function initViewer() {{
        if (typeof Autodesk === 'undefined') {{
            setTimeout(initViewer, 1000);
            return;
        }}

        var options = {{
            env: 'Local',
            useADP: false
        }};

        log('Initializing Autodesk.Viewing...');
        Autodesk.Viewing.Initializer(options, function() {{
            try {{
                var viewerDiv = document.getElementById('viewer');
                globalViewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
                
                log('Starting viewer instance...');
                var startedCode = globalViewer.start();
                
                if (startedCode > 0) {{
                    log('FAIL: Viewer start failed code ' + startedCode);
                    return;
                }}
                
                log('Processing Model Data...');
                var gltfDataRaw = {model_data_raw};
                var gltfParsed = (typeof gltfDataRaw === 'string') ? JSON.parse(gltfDataRaw) : gltfDataRaw;
                
                var blob = new Blob([JSON.stringify(gltfParsed)], {{type: 'application/json'}});
                var url = URL.createObjectURL(blob) + '#.gltf';
                
                log('Loading Model URL: ' + url);
                
                var loadOptions = {{
                    fileExt: 'gltf',
                    loadAsExtension: 'gltf',
                    applyScaling: 'm' // UTM is in meters
                }};

                globalViewer.loadModel(url, loadOptions, function(model) {{
                    log('SUCCESS: Model loaded!');
                    
                    // Automatically focus after a short delay
                    setTimeout(function() {{
                        log('Auto-focusing camera...');
                        globalViewer.setLightPreset(4); // Blue Sky
                        globalViewer.fitToView();
                    }}, 1000);

                    setTimeout(function() {{ 
                        logDiv.style.background = 'rgba(0,40,0,0.5)'; 
                        logDiv.innerText = 'OK: Model Visible. Use buttons to zoom.';
                    }}, 4000);
                }}, function(errorCode, errorMsg) {{
                    log('ERROR ' + errorCode + ': ' + errorMsg);
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
\"\"\"

display(HTML(html_code))
"""

for path in paths:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        updated = False
        for cell in nb.cells:
            if cell.cell_type == 'code' and ('Diagnostic Viewer' in cell.source or 'viewer-container' in cell.source or 'HTML(html_code)' in cell.source):
                cell.source = new_code
                updated = True
        
        if updated:
            with open(path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print(f"Updated {path}")
    except Exception as e:
        print(f"Failed {path}: {str(e)}")
