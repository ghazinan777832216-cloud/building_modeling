import trimesh
import base64
import os

box = trimesh.creation.box(extents=[10, 20, 10])
box.visual.face_colors = [200, 50, 50, 255] # Red

floor = trimesh.creation.box(extents=[100, 0.1, 100])
floor.visual.face_colors = [50, 50, 50, 255] # Dark Gray

scene = trimesh.Scene([box, floor])
with open("test.glb", "wb") as f:
    f.write(scene.export(file_type='glb'))

print("Exported test.glb")
