import pyprt
import os

pyprt.initialize_prt()

# Create a 10x10 square
dummy_coords = [0.0, 0.0, 0.0, 10.0, 0.0, 0.0, 10.0, 0.0, 10.0, 0.0, 0.0, 10.0]
initial_shape = pyprt.InitialShape(dummy_coords)

RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])

# Print basic info
print(f"RPK Path: {RPK_PATH}")
print(f"File exists: {os.path.exists(RPK_PATH)}")

# Generate and check reports
models = model_generator.generate_model([{}], RPK_PATH, "com.esri.prt.codecs.AttributeReporterEncoder", {})
if models:
    print("Reports from RPK:")
    for key, val in models[0].get_report().items():
        print(f"  {key}: {val}")
else:
    print("Failed to generate model.")

# Check GLTF Encoder options
# We want to make sure we are not missing anything
print("\nTesting GLTF Generation...")
out_dir = os.path.join(os.getcwd(), "test_output")
os.makedirs(out_dir, exist_ok=True)
encoder_options = {
    "outputPath": out_dir,
    "baseName": "test_building",
    "embedTextures": True
}
model_generator.generate_model([{"Nbr_of_Floors": 12}], RPK_PATH, "com.esri.prt.codecs.GLTFEncoder", encoder_options)

glb_file = os.path.join(out_dir, "test_building_0.glb")
if os.path.exists(glb_file):
    print(f"Generated GLB Size: {os.path.getsize(glb_file)} bytes")
else:
    print("GLB not generated.")

pyprt.shutdown_prt()
