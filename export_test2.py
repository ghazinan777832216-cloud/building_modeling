import trimesh
import base64

box = trimesh.creation.box(extents=[10, 20, 10])
box.visual.face_colors = [200, 50, 50, 255]

# Force vertex colors instead of face colors
box.visual.vertex_colors = box.visual.vertex_colors 

# Force material creation
box.visual.material = trimesh.visual.material.PBRMaterial(
    name="default",
    baseColorFactor=[1.0, 1.0, 1.0, 1.0],
    metallicFactor=0.0,
    roughnessFactor=0.8
)

# Force vertex normals
normals = box.vertex_normals

floor = trimesh.creation.box(extents=[100, 0.1, 100])
floor.visual.face_colors = [50, 50, 50, 255]
floor.visual.material = trimesh.visual.material.PBRMaterial(
    name="default",
    baseColorFactor=[1.0, 1.0, 1.0, 1.0],
    metallicFactor=0.0,
    roughnessFactor=0.8
)
fnormals = floor.vertex_normals

scene = trimesh.Scene([box, floor])
with open("test2.glb", "wb") as f:
    f.write(scene.export(file_type='glb'))

print("Exported test2.glb")
