# Python GIS Procedural Pipeline (Updated Notebook)

هذا الدفتر يشرح **خط الأنابيب الكامل لتوليد المباني الإجرائية** انطلاقاً من رسم مضلع على الخريطة وصولاً إلى توليد نموذج ثلاثي الأبعاد.

تحديث النسخة السابقة من الدفتر لتحسين:

- بنية الـ Pipeline
- فصل المراحل (GIS → Geometry → Procedural)
- جعل النظام أسهل للفهم والتوسعة

كل خلية أدناه تحتوي على:

- كيف الفكرة في النسخة القديمة
- ماذا يجب تغير في النسخة الجديدة
- لماذا التغيير مهم

---

# الخلية 1 — تثبيت المكتبات

## قبل التحديث

كانت الخلية تستخدم pip التقليدي:

```python
!pip install leafmap shapely pyproj pyprt pythreejs ipywidgets
```

المشكلة:

- pip بطيء في البيئات التفاعلية
- إدارة البيئات أصعب

---

## بعد التحديث

تم استخدام مدير الحزم **uv** لأنه أسرع وأكثر استقراراً.

```python
!uv pip install leafmap shapely pyproj pyprt
```

### سبب التغيير

- uv أسرع بكثير
- مناسب لبيئة Jupyter
- يقلل مشاكل الاعتمادات

---

# الخلية 2 — الخريطة ورسم المضلع

## قبل التحديث

كنا ننشئ الخريطة فقط دون تنظيم تدفق البيانات.

```python
import leafmap

m = leafmap.Map(center=[15, 45], zoom=16)
m.add_draw_control()
```

لكن لم يكن هناك نظام واضح لتخزين الرسومات.

---

## بعد التحديث

أضفنا نظام تخزين للمضلعات المرسومة.

```python
import leafmap

m = leafmap.Map(center=[15,45], zoom=16)

m.add_draw_control()


drawn_features = []


def on_draw(feature, **kwargs):

    drawn_features.append(feature)

    print("تم رسم مضلع جديد")


m.on_draw(on_draw)

m
```

### التحسين

الآن كل مضلع يتم رسمه يتم حفظه داخل:

```python
drawn_features
```

وهذا يسمح باستخدامه لاحقاً في الـ Pipeline.

---

# الخلية 3 — تحويل GeoJSON إلى Polygon

## قبل التحديث

كان التحويل يحدث مباشرة داخل خلية طويلة.

هذا جعل الكود:

- صعب القراءة
- صعب إعادة الاستخدام

---

## بعد التحديث

تم إنشاء دالة مستقلة.

```python
from shapely.geometry import shape


def get_polygon():

    if not drawn_features:
        return None

    geojson = drawn_features[-1]

    polygon = shape(geojson["geometry"])

    return polygon
```

### لماذا هذا أفضل

- الكود أصبح Modular
- يمكن إعادة استخدامه

---

# الخلية 4 — تحويل الإحداثيات إلى UTM

## قبل التحديث

كان التحويل يحدث داخل نفس الخلية التي تعالج المضلع.

المشكلة:

- صعوبة التعديل
- خلط بين GIS و Geometry

---

## بعد التحديث

تم فصل التحويل إلى دالة مستقلة.

```python
from pyproj import Transformer
from shapely.geometry import Polygon


transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32638",
    always_xy=True
)


def to_utm(polygon):

    coords = list(polygon.exterior.coords)

    utm = [
        transformer.transform(x,y)
        for x,y in coords
    ]

    return Polygon(utm)
```

### التحسين

الآن أصبح لدينا فصل واضح بين:

```
GIS coordinates
↓
UTM meters
```

وهذا مهم لمحركات ثلاثية الأبعاد.

---

# الخلية 5 — توليد المبنى Procedural

## قبل التحديث

كان الكود مدمجاً مع مراحل أخرى.

---

## بعد التحديث

تم إنشاء دالة واضحة لتوليد المبنى.

```python
import pyprt


def generate_building(utm_polygon):

    model = pyprt.Model()

    coords = list(utm_polygon.exterior.coords)

    model.set_geometry(coords)


    attributes = {

        "Usage": "Residential",

        "Mode": "Generate Facade",

        "Nbr_of_Floors": 8,

        "Standard_Floor_Height": 3.2,

        "Ground_Floor_Height": 5

    }


    model.set_attributes(attributes)


    rule = r"C:\\RPK\\RuleFootprint.rpk"


    model.run_rule(rule)


    gltf = model.export_to_memory("gltf")


    return gltf
```

### ما الذي تغير

الآن هذه الخلية مسؤولة فقط عن:

```
UTM polygon
↓
Procedural building
↓
glTF
```

---

# الخلية 6 — عارض Three.js

## قبل التحديث

كان العرض يتم باستخدام مكتبة Python ثلاثية الأبعاد.

لكن هذه المكتبات محدودة.

---

## بعد التحديث

تم استخدام Three.js مباشرة داخل Jupyter.

```python
from IPython.display import HTML


def create_viewer():

    return HTML("""

<script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>

<div id="viewer" style="width:900px;height:600px"></div>

<script>

const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(
60,
900/600,
0.1,
10000
)

camera.position.set(200,200,200)

const renderer = new THREE.WebGLRenderer()

renderer.setSize(900,600)


document.getElementById("viewer").appendChild(renderer.domElement)


const light = new THREE.DirectionalLight(0xffffff,1)

light.position.set(100,200,100)

scene.add(light)


const grid = new THREE.GridHelper(1000,50)

scene.add(grid)


function animate(){

requestAnimationFrame(animate)

renderer.render(scene,camera)

}

animate()

</script>

""")
```

### التحسين

الآن العارض:

- أسرع
- أكثر مرونة
- مناسب لعرض glTF

---

# الخلية 7 — تشغيل الـ Pipeline

## قبل التحديث

كان المستخدم يحتاج تشغيل عدة خلايا يدوياً.

---

## بعد التحديث

تم إنشاء دالة تشغل النظام بالكامل.

```python

def run_pipeline():

    polygon = get_polygon()


    if polygon is None:

        print("لا يوجد مضلع مرسوم")

        return


    utm_polygon = to_utm(polygon)


    gltf = generate_building(utm_polygon)


    print("تم توليد المبنى بنجاح")


    return gltf
```

تشغيل النظام:

```python
gltf_model = run_pipeline()
```

---

# النتيجة النهائية

الـ Pipeline أصبح واضحاً:

```
Sketch Polygon
      ↓
GeoJSON
      ↓
Shapely
      ↓
UTM
      ↓
PyPRT
      ↓
glTF
      ↓
Three.js
```

---

# التحسينات التي تحققت

- كود أوضح
- فصل المراحل
- Pipeline احترافي
- قابل للتوسعة

---

# Architecture العامة للنظام

لفهم المشروع بشكل أفضل، من المفيد تصور **تدفق البيانات الكامل** بين مكونات النظام.

```
User Sketch
     ↓
Leafmap / Leaflet
     ↓
GeoJSON
     ↓
Shapely Geometry
     ↓
Coordinate Transform
(pyproj)
     ↓
UTM Polygon (meters)
     ↓
PyPRT Procedural Engine
     ↓
Generated Building
     ↓
glTF Model
     ↓
Three.js Viewer
```

هذا التقسيم يوضح أن النظام يتكون من **ثلاث طبقات رئيسية**.

---

# طبقات النظام

## 1️⃣ طبقة GIS

المسؤولة عن:

- عرض الخريطة
- رسم المضلع
- إدارة GeoJSON

التقنيات المستخدمة:

- leafmap
- Leaflet

```
Map
↓
Sketch
↓
GeoJSON
```

---

## 2️⃣ طبقة المعالجة الهندسية

المسؤولة عن:

- تحويل GeoJSON إلى Polygon
- تحويل الإحداثيات إلى UTM

المكتبات:

- Shapely
- pyproj

```
GeoJSON
↓
Shapely
↓
UTM Polygon
```

السبب في استخدام UTM هو أن:

```
1 unit = 1 meter
```

وهذا مناسب لمحركات النمذجة ثلاثية الأبعاد.

---

## 3️⃣ طبقة التوليد الإجرائي

المسؤولة عن:

- توليد المبنى
- تطبيق القواعد المعمارية

المحرك المستخدم:

PyPRT

وهو نفس محرك القواعد المستخدم في:

Esri CityEngine

```
UTM Polygon
↓
CGA Rules
↓
Procedural Building
↓
glTF
```

---

# طبقة العرض ثلاثي الأبعاد

المسؤولة عن عرض النموذج النهائي.

المكتبة المستخدمة:

Three.js

```
glTF
↓
Three.js
↓
3D Scene
```

ميزة glTF أنه:

- خفيف
- مدعوم في معظم محركات 3D
- مناسب للويب

---

# تدفق البيانات في النظام

يمكن تلخيص الـ Pipeline النهائي بهذا الشكل:

```
Sketch Polygon
      ↓
GeoJSON
      ↓
Shapely Polygon
      ↓
UTM Conversion
      ↓
PyPRT
      ↓
glTF
      ↓
Three.js Viewer
```

---

# كيف يمكن تطوير المشروع أكثر

يمكن تحويل هذا الدفتر إلى **نواة محرك GIS ثلاثي الأبعاد** بإضافة:

### 1️⃣ دعم عدة مبانٍ

```
Multiple polygons
↓
Multiple procedural buildings
```

### 2️⃣ تحديث المبنى عند تعديل المضلع

```
Edit polygon
↓
Re-run PyPRT
↓
Update model
```

### 3️⃣ عرض المباني فوق الخريطة مباشرة

```
Map
+
3D buildings
```

### 4️⃣ تصدير بيانات المدينة

يمكن دعم:

- CityJSON
- glTF
- GeoJSON

---

# الهدف النهائي للمشروع

هذا الدفتر يمكن أن يتطور ليصبح:

```
Procedural GIS Editor
```

أي أداة تسمح بـ:

- رسم القطع الأرضية
- توليد المباني
- تعديل القواعد المعمارية
- تصدير نموذج مدينة ثلاثي الأبعاد

وهو مفهوم قريب من طريقة عمل:

CityEngine

لكن باستخدام Python و Jupyter.

---

# العمل بنظام UTM داخل المشهد ثلاثي الأبعاد

لكي تكون النماذج ثلاثية الأبعاد متوافقة مع بيانات GIS يجب أن يعمل المشهد ثلاثي الأبعاد بنفس وحدة القياس.

في هذا المشروع نستخدم نظام:

```
UTM meters
```

أي أن:

```
1 unit في Three.js = 1 meter
```

وهذا يجعل:

- أبعاد المباني صحيحة
- الارتفاعات دقيقة
- النماذج متوافقة مع بيانات GIS الأخرى

---

# تحويل إحداثيات UTM إلى إحداثيات Three.js

في العادة تكون إحداثيات UTM كبيرة جداً مثل:

```
Easting  = 414300
Northing = 1698500
```

لو استخدمنا هذه القيم مباشرة داخل Three.js قد يسبب ذلك مشاكل دقة.

لذلك نستخدم مفهوم:

```
Local Origin
```

نختار نقطة مرجعية:

```
origin_E = 414000
origin_N = 1698000
```

ثم نحسب الإحداثيات المحلية:

```
x = Easting - origin_E
z = Northing - origin_N
```

ويصبح النظام داخل المشهد:

```
Three.js

X → Easting
Z → Northing
Y → Height
```

---

# مثال تحويل الإحداثيات

إذا كان لدينا:

```
E = 414300
N = 1698500
```

بعد التحويل يصبح:

```
x = 300
z = 500
```

وهذا مناسب جداً لمحركات الرسوميات.

---

# دمج Three.js مع الخريطة

يمكن دمج المشهد ثلاثي الأبعاد مع الخريطة بطريقتين رئيسيتين.

## الطريقة الأولى — عرض منفصل

```
Map (Leafmap)
     ↓
Sketch Polygon
     ↓
Procedural Generation
     ↓
Three.js Viewer
```

ميزة هذه الطريقة:

- بسيطة
- مناسبة للتجارب داخل Jupyter

---

## الطريقة الثانية — دمج كامل مع GIS

يمكن لاحقاً دمج النظام مع:

ArcGIS JavaScript API

بحيث يصبح المشهد:

```
ArcGIS Map
      +
Three.js Scene
      +
Procedural Buildings
```

وهذا يسمح بـ:

- عرض المباني فوق الخريطة مباشرة
- التزامن مع الإحداثيات الجغرافية
- إدارة طبقات GIS

---

# الشكل النهائي للمعمارية

```
Sketch Polygon
      ↓
GeoJSON
      ↓
Shapely
      ↓
UTM Conversion
      ↓
PyPRT
      ↓
glTF
      ↓
Three.js (UTM Scene)
      ↓
GIS Integration
```

---

# لماذا هذا التصميم مهم

هذا التصميم يجعل المشروع:

- متوافقاً مع أنظمة GIS
- قابلاً للتوسع
- قريباً من طريقة عمل محركات المدن الرقمية

مثل:

- CityEngine
- Cesium
- Unreal GIS

---
