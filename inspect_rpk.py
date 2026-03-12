import pyprt
import os

pyprt.initialize_prt()

# Create a dummy initial shape to inspect the RPK
# We use a 10x10 square
dummy_coords = [0.0, 0.0, 0.0, 10.0, 0.0, 0.0, 10.0, 0.0, 10.0, 0.0, 0.0, 10.0]
initial_shape = pyprt.InitialShape(dummy_coords)

RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])

# Usually we can get the default attributes by generating once without overrides
models = model_generator.generate_model([{}], RPK_PATH, "com.esri.prt.codecs.AttributeReporterEncoder", {})

if models:
    reports = models[0].get_report()
    print("Detected attributes and reports:")
    for key, value in reports.items():
        print(f"  {key}: {value}")
else:
    print("Failed to generate model for inspection.")

pyprt.shutdown_prt()
