import json
import shapely.geometry
from pyproj import Transformer
import pyprt
import os

print("--- Step 1: Mocking Map Drawing ---")
# Mock a 10x10 meter residential plot in Zurich (Lat: 47.37, Lon: 8.54)
mock_geojson = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [[8.540, 47.370], [8.540, 47.371], [8.541, 47.371], [8.541, 47.370], [8.540, 47.370]]
        ]
    }
}
drawn_features = [mock_geojson]
print("Mock polygon created.")

print("\n--- Step 2: Extract & Transform to UTM ---")
geojson_feature = drawn_features[-1]
polygon = shapely.geometry.shape(geojson_feature['geometry'])
coords = list(polygon.exterior.coords)

# Zurich is around EPSG:32632
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
utm_coords = [transformer.transform(x, y) for x, y in coords]
utm_polygon = shapely.geometry.Polygon(utm_coords)

if not utm_polygon.exterior.is_ccw:
    utm_coords = list(utm_polygon.exterior.coords)[::-1]
    utm_polygon = shapely.geometry.Polygon(utm_coords)

print(f"UTM Coords: {utm_coords}")

print("\n--- Step 3: Run PyPRT ---")
pyprt.initialize_prt()

coords_2d = list(utm_polygon.exterior.coords)[:-1]
flat_coords = []
for x, y in coords_2d:
    flat_coords.extend([x, 0.0, y])

print(f"Flat coords for PRT: {flat_coords}")
initial_shape = pyprt.InitialShape(flat_coords)

rpk_path = r"C:\RPK\RuleFootprint.rpk"
if not os.path.exists(rpk_path):
    print(f"SKIP: RPK file {rpk_path} not found. Cannot test generation.")
else:
    attributes = {"Usage": "Residential", "Nbr_of_Floors": 8}
    generator = pyprt.ModelGenerator([initial_shape])
    models = generator.generate_model(
        [attributes],
        rpk_path,
        "com.esri.pyprt.PyEncoder",
        {"emitGeometry": True, "emitReport": True}
    )
    
    if models and models[0]:
        gm = models[0]
        print(f"SUCCESS! Building generated with {len(gm.get_vertices())//3} vertices and {len(gm.get_faces())} faces.")
    else:
        print("FAILED to generate building.")
