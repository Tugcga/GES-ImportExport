# Blender *.ges exporter

This addon export blender scene to ges-file - general description format for 3d-scenes. Features:

* Export Cycles materials to *.gem files. This format is based on [General Node Tree Description](https://github.com/Tugcga/GeneralNodeTreeDescription)
* Export all geometry to *.geo files. This format is based on [Mesh Data Serialized Format](https://github.com/Tugcga/MeshDataSerializedFormat)
* Export lights and cameras. If the light has Cycles shader, then this shader export as *.gem file
* Export render settings
* All objects exports with preserved hierarchy

Limitations:

* No animations, skinning data and other rigs
* Does not support import *.ges files, only export it
* Works only with Blender 2.80

## How to use

1. Select File - Export - General Export Scene

![Export command](tut_01.png?raw=true)

2. Set destination directory and file name. Also you can set the export mode:

* Selected material: export only one material as *.gem file
* All scene: export all data
* All materials: export only materials from the scene as one *.gem file with library
* Selected objects: export selected objects and corresponding materials

If you turn on "Copy textures" checkbox, then all textures from materials will be copied to folder with the name [scene name]_textures. Relative path mode means that all paths to textures in materials and geo-objects in the scene will be saved as relative path relatively to saved path.

![Export command](tut_02.png?raw=true)

For example, if we have the basic scene with one cube, one point light and one camera, then after export (with the mode All scene) as scene.ges we will obtain three files:

* scene.ges with scene description
* scene.gem with material of the cube object
* scene_lights.gem with shader of the light

and two directories: scene_meshes with one object Cube.geo and scene_lights_textures with under_bridge_1k.hdr (this texture used by background shader).