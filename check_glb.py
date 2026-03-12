import trimesh
import os

glb_path = os.path.join("output_models", "procedural_building_0.glb")
if os.path.exists(glb_path):
    try:
        scene = trimesh.load(glb_path)
        print(f"GLB File: {glb_path}")
        print(f"Is Scene: {isinstance(scene, trimesh.Scene)}")
        if isinstance(scene, trimesh.Scene):
            print(f"Number of geometries: {len(scene.geometry)}")
            for name, mesh in scene.geometry.items():
                print(f"  Mesh '{name}': {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
            print(f"Bounding Box: {scene.bounds}")
        else:
            print(f"Vertices: {len(scene.vertices)}")
            print(f"Faces: {len(scene.faces)}")
            print(f"Bounding Box: {scene.bounds}")
    except Exception as e:
        print(f"Error loading GLB: {e}")
else:
    print(f"GLB file not found at {glb_path}")
