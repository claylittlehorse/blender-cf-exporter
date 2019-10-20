# Blender CFrame Exporter
A simple, lightweight addon to export CFrame data out from blender. This tool dumps only, CFrames, and nothing else. It is intended to be used as an initial step in a larger toolchain.

## Export Setup
In the outliner panel, right-click to create a new collection, and name it `EXPORTS`, as shown below.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/collection_2.png)

*When running the exporter, any object inside of this EXPORTS collection will have CFrame data written out on export.*

Optionally, you can also have the transforms objects be calculated relative to a root transform on export. (Useful if you want to move an entire rig in blender without baking that translation to animation data.)

This behavior can be achieved by having an object named `CF_ROOT` somwhere in the hierarchy. The root object does not have to be in the `EXPORTS` collection.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/root.png)

Finally, to export CFrames, go to *File > Export > Roblox CFrames*, and save the file wherever you'd like.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/export_dropdown.png)

The range of frames exported is determined by the start and end positions of the scene playback.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/start_end.png)