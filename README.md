# Blender CFrame Exporter
A simple, lightweight addon to export CFrame data out from blender. This tool dumps _only CFrames_ and nothing else. It is intended to be used as an initial step in a larger toolchain.

### Installation
Download the latest [addon.py](https://github.com/zoebasil/blender-cf-exporter/releases/download/1.0/addon.py) and save it somewhere. To install the addon, in Blender, go to *Edit > Preferences > Addons* and click the *Install* button near the top right corner. Navigate to wherever you saved the `addon.py` file, select it, and confirm the installation. Lastly, make sure you enable the addon.

## Export Setup
_For quick setup reference, you can download and open the [example file](https://github.com/zoebasil/blender-cf-exporter/releases/download/1.0/Example.blend) from the releases page._

In the outliner panel, right-click to create a new collection, and name it `EXPORT`, as shown below.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/collection_2.png)

When running the exporter, any object inside of this EXPORT collection will have CFrame data written out on export.

Optionally, you can also have the transforms objects be calculated relative to a root transform on export. (Useful if you want to move an entire rig in blender without baking that translation to animation data.)

This behavior can be achieved by having an object named `CF_ROOT` somwhere in the hierarchy. The root object does not have to be in the `EXPORT` collection.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/root.png)

Finally, to export CFrames, go to *File > Export > Roblox CFrames*, and save the file wherever you'd like.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/export_dropdown.png)

The range of frames exported is determined by the start and end positions of the scene playback.

![alt text](https://github.com/zoebasil/blender-cf-exporter/raw/master/readme_imgs/start_end.png)

