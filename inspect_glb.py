import json
import struct

with open("test.glb", "rb") as f:
    magic = f.read(4)
    version = struct.unpack('<I', f.read(4))[0]
    length = struct.unpack('<I', f.read(4))[0]
    
    chunk0_length = struct.unpack('<I', f.read(4))[0]
    chunk0_type = f.read(4)
    
    json_data = f.read(chunk0_length)
    gltf = json.loads(json_data.decode('utf-8'))
    print(json.dumps(gltf, indent=2))
