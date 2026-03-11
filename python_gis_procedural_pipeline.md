# Python GIS Procedural Pipeline

## تثبيت المكتبات

```python
!uv install leafmap shapely pyproj pyprt pythreejs ipywidgets
```

## الخلية 1: إعداد الخريطة ورسم المضلع

```python
import leafmap

m = leafmap.Map(center=[15, 45], zoom=16)
m.add_draw_control()
drawn_features = []

def on_draw(feature, **kwargs):
    drawn_features.append(feature)
    print("تم رسم مضلع جديد!")

m.on_draw(on_draw)
m
```

## الخلية 2: استخراج GeoJSON وتحويل الإحداثيات إلى UTM وترتيب CCW

```python
from shapely.geometry import shape, Polygon
from pyproj import Transformer

if len(drawn_features) == 0:
    print("لم يتم رسم أي مضلع بعد")
else:
    geojson_feature = drawn_features[-1]
    polygon = shape(geojson_feature['geometry'])
    coords = list(polygon.exterior.coords)
    print("إحداثيات Lat/Lon الأصلية:")
    print(coords)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32638", always_xy=True)
    utm_coords = [transformer.transform(x, y) for x, y in coords]
    utm_polygon = Polygon(utm_coords)
    if not utm_polygon.exterior.is_ccw:
        utm_coords = list(utm_polygon.exterior.coords)[::-1]
        utm_polygon = Polygon(utm_coords)
    print("تم تحويل الإحداثيات إلى UTM وترتيبها CCW بنجاح")
    utm_polygon
```

## الخلية 3: إرسال الشكل إلى PyPRT وتوليد المبنى Procedural

```python
import pyprt
import json

try:
    utm_polygon
except NameError:
    raise Exception("لم يتم تعريف المضلع. تأكد من تنفيذ الخلية السابقة.")

model = pyprt.Model()
coords_for_pyprt = list(utm_polygon.exterior.coords)
model.set_geometry(coords_for_pyprt)

attributes = {
    "Usage": "Residential",
    "Mode": "Generate Facade",
    "Nbr_of_Floors": 8,
    "Standard_Floor_Height": 3.200,
    "Ground_Floor_Height": 5.000,
    "Front_Setback_Mode": "Increasing",
    "Front_Setback_Distance": 4.500,
    "Layout_Shape": "Along Front",
    "Wing_Width": 15.000,
    "Layout_Orientation": "Open To Back",
    "Green_Space,enerate_Green_Space": True,
    "Green_Space,Create_Trees": False
}
model.set_attributes(attributes)

rule_path = r"C:\RPK\RuleFootprint.rpk"
model.run_rule(rule_path)

# حفظ glTF في متغير للعرض لاحقاً
gltf_output = model.export_to_memory(format="gltf")
gltf_list = [gltf_output]  # تخزين الناتج في قائمة
print("تم توليد المبنى Procedural وتخزينه في gltf_list")
```

## الخلية 4: عرض النموذج باستخدام pythreejs

```python
from pythreejs import *
from IPython.display import display

try:
    gltf_list
except NameError:
    raise Exception("لم يتم توليد gltf_list بعد. نفّذ الخلية السابقة أولاً.")

loader = GLTFLoader()
scene = loader.parse(gltf_list[0])

camera = PerspectiveCamera(position=[50, 50, 50], fov=45,
                           children=[DirectionalLight(color='white', position=[3,5,1], intensity=0.5)])
controller = OrbitControls(controlling=camera)

renderer = Renderer(camera=camera,
                    scene=scene.scene,
                    controls=[controller],
                    width=800,
                    height=600)

display(renderer)

```
