import json

def fix_notebook():
    file_path = 'pipeline_new.ipynb'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update Cell 4 (index 4)
    data['cells'][4]['source'] = [
        "# === Cell 2: GIS Layer — Map & Polygon Storage ===\n",
        "\n",
        "import leafmap\n",
        "from IPython.display import display\n",
        "\n",
        "# إنشاء الخريطة التفاعلية\n",
        "m = leafmap.Map(center=[15.3694, 44.1910], zoom=16)\n",
        "\n",
        "# نظام تخزين المضلعات - سيتم الاعتماد على m.draw_features الافتراضية\n",
        "drawn_features = []\n",
        "\n",
        "print(\"✅ الخريطة جاهزة — ارسم مضلعًا ثم شغّل الخلية التالية\")\n",
        "print(\"✅ Map ready — draw a polygon then run the next cells\")\n",
        "m"
    ]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    fix_notebook()
    print("Notebook cell 4 successfully updated!")
