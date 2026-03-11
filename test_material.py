import trimesh
import base64
floor = trimesh.creation.box(extents=[100, 0.1, 100])
floor.visual.face_colors = [50, 50, 50, 255]

print("Material type:", type(floor.visual.material))
print("Material dict:", floor.visual.material.to_dict() if hasattr(floor.visual.material, 'to_dict') else dir(floor.visual.material))
