# === Cell 4: عرض النموذج ثلاثي الأبعاد بعارض Three.js Editor ===

import os, webbrowser
from IPython.display import display, HTML

# قراءة قالب العارض
template_path = os.path.join(os.getcwd(), 'viewer_template.html')
with open(template_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# تضمين بيانات النموذج
final_html = html_content.replace('%%MODEL_B64%%', model_b64)

# حفظ الملف
html_filename = 'viewer_full.html'
with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(final_html)

full_path = os.path.abspath(html_filename)

# فتح العارض في المتصفح تلقائياً
webbrowser.open('file:///' + full_path.replace(chr(92), '/'))

# عرض زر في الـ Notebook
display(HTML(f"""
<div style="border:1px solid #333; background:#1a1a1a; padding:20px; border-radius:8px;
            font-family:Arial,sans-serif; text-align:center; color:#ccc;">
  <h2 style="color:#fff; margin:0 0 10px">Three.js Viewer — جاهز</h2>
  <p style="color:#888; font-size:13px; margin:0 0 16px">
    تم فتح العارض في المتصفح تلقائياً · أو اضغط الزر أدناه
  </p>
  <a href="{html_filename}" target="_blank"
     style="background:#333; color:#ccc; padding:10px 24px; text-decoration:none;
            border-radius:4px; border:1px solid #444; font-size:13px; display:inline-block;">
    🌐 فتح العارض في المتصفح
  </a>
</div>
"""))
