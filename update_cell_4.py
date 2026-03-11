from IPython.display import HTML, display
import json

try:
    gltf_list
    if not gltf_list or not gltf_list[0]:
         raise Exception("gltf_list موجودة ولكنها فارغة. تأكد من نجاح توليد النموذج.")
except NameError:
    raise Exception("لم يتم توليد gltf_list بعد. نفّذ الخلية السابقة أولاً.")

# تحويل بيانات glTF إلى JSON
model_data = json.dumps(gltf_list[0])

html_code = f"""
<div id='viewer-container' style='position:relative; width:800px; height:600px; background: #eee; border: 1px solid #ccc;'>
    <div id='viewer' style='width:100%; height:100%'></div>
    <div id='viewer-log' style='position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.5); color:white; font-size:12px; padding:5px; max-height:100px; overflow-y:auto; pointer-events:none;'>
        Initializing Viewer...
    </div>
</div>

<link rel='stylesheet' href='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/style.min.css' type='text/css'>
<script src='https://developer.api.autodesk.com/modelderivative/v2/viewers/7.98/viewer3D.min.js'></script>

<script>
(function() {{
    var logDiv = document.getElementById('viewer-log');
    function log(msg) {{
        console.log('[Viewer]', msg);
        logDiv.innerText += '\\n' + msg;
        logDiv.scrollTop = logDiv.scrollHeight;
    }}

    function initViewer() {{
        if (typeof Autodesk === 'undefined') {{
            log('Error: Autodesk library not loaded yet. Retrying...');
            setTimeout(initViewer, 500);
            return;
        }}

        var options = {{
            env: 'Local',
            useADP: false
        }};

        log('Initializing Autodesk.Viewing...');
        Autodesk.Viewing.Initializer(options, function() {{
            var viewerDiv = document.getElementById('viewer');
            var viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
            var startedCode = viewer.start();
            
            if (startedCode > 0) {{
                log('Error: Viewer failed to start with code ' + startedCode);
                return;
            {{
                log('Viewer started successfully.');
            }}

            try {{
                var gltf = {model_data};
                log('glTF data loaded (' + JSON.stringify(gltf).length + ' bytes).');

                var blob = new Blob([JSON.stringify(gltf)], {{type: 'application/json'}});
                var url = URL.createObjectURL(blob);
                log('Blob URL created: ' + url);

                viewer.loadModel(url, {{}}, function(model) {{
                    log('Model loaded successfully!');
                    logDiv.style.display = 'none'; // Hide log on success
                }}, function(errorCode, errorMsg, statusCode, statusText) {{
                    log('Error loading model: ' + errorCode + ' - ' + errorMsg);
                }});
            }} catch (e) {{
                log('Exception in data processing: ' + e.message);
            }}
        }});
    }}

    // Small delay to ensure script tags are processed
    setTimeout(initViewer, 100);
}})();
</script>
"""

display(HTML(html_code))
