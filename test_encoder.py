import pyprt
import os

pyprt.initialize_prt()

# Dummy shape for testing
initial_shape = pyprt.InitialShape([0, 0, 0, 0, 0, 10, 10, 0, 10, 10, 0, 0])
attributes = {"Nbr_of_Floors": 12, "Usage": "Residential"}

RPK_PATH = r"C:\RPK\RuleFootprint.rpk"
model_generator = pyprt.ModelGenerator([initial_shape])

# Export using GLTF Encoder
encoder = "com.esri.prt.codecs.GLTFEncoder"
encoder_options = {
    "outputPath": os.path.dirname(os.path.abspath(__file__)),
    "baseName": "pyprt_gltf_output"
}

generated_models = model_generator.generate_model(
    [attributes], 
    RPK_PATH, 
    encoder, 
    encoder_options
)
print("Finished generation using GLTFEncoder")
