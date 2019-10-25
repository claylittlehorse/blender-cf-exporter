import bpy, math, re, bpy_extras
from mathutils import Matrix

EXPORT_COLLECTION_NAME = "EXPORT"
ROOT_OBJ_NAME = "CF_ROOT"

# Rotation matrix to transform a Z-up matrix in blender to a Y-up roblox CF
# matrix
transformToYUpMatrix = bpy_extras.io_utils.axis_conversion(from_forward='-Y', from_up='Z', to_forward='Z', to_up='Y').to_4x4()

# Blender matrix to roblox cframe components
def matrixToCFrameComponents(matrix):
	# matrix @ matrix in python equivalent to cf * cf in roblox
	yUpMatrix = transformToYUpMatrix @ matrix
	cframe_components = [yUpMatrix[0][3], yUpMatrix[1][3], yUpMatrix[2][3],
		yUpMatrix[0][0], yUpMatrix[0][1], yUpMatrix[0][2],
		yUpMatrix[1][0], yUpMatrix[1][1], yUpMatrix[1][2],
		yUpMatrix[2][0], yUpMatrix[2][1], yUpMatrix[2][2]
	]
	return cframe_components

# Get the transforms from the current frame state
def getCurrentTransforms():
	# Get the collection holding the objects we want to bake CF data from
	# data. (https://docs.blender.org/api/current/bpy.data.html)
	exportCollection = bpy.data.collections[EXPORT_COLLECTION_NAME]

	rootMatrix = None
	# If the _ROOT object exists, we save its world transform.
	# (info on `in` operator in python: https://stackoverflow.com/a/19775766)
	if ROOT_OBJ_NAME in bpy.data.objects:
		rootMatrix = bpy.data.objects[ROOT_OBJ_NAME].matrix_world
	
	# Collect all of the object transforms in the export collection.
	objectTransforms = {}
	for obj in exportCollection.objects:
		objectMatrix = obj.matrix_world

		# If we rootMatrix exists, we get the transform of our object relative
		# to the root's transform. Otherwise, we just use the world transform.
		if rootMatrix:
			# With CFrames, this would be rootCF:ToObjectSpace(objectCF), or
			# rootCF:Inverse() * objectCF
			relativeToRootMatrix = rootMatrix.inverted() @ objectMatrix
			objectTransforms[obj.name] = matrixToCFrameComponents(relativeToRootMatrix)
		else:
			objectTransforms[obj.name] = matrixToCFrameComponents(objectMatrix)

	return objectTransforms

# Gets the transforms for every frame
def getAnimationCFrames():
	# Get the scene from context (https://docs.blender.org/api/current/bpy.context.html)
	scene = bpy.context.scene
	currentFrameNumber = scene.frame_current

	frames = []
	
	for i in range(scene.frame_start, scene.frame_end+1):
		# Set the frame
		scene.frame_set(i)
		# Ensures modifiers and everything are all updated
		bpy.context.evaluated_depsgraph_get().update()
		# Get transforms for this frame and add them to our list
		frame = getCurrentTransforms()
		frames.append(frame)
	
	# Set the scene back to the frame it was on before exporting
	scene.frame_set(currentFrameNumber)
	bpy.context.evaluated_depsgraph_get().update()
	
	return frames

# Strings we use to make the lua text file. These are confusing and weird!
# -- KEY --
# 	"{{" or "}}" = Literal bracket in the string
#	 \n = Newline
#	 \t = Tab
# 	{} = Argument pos for .format
luaTempltStr = "local c = CFrame.new\nreturn {{\n\tfps = {},\n\tframes = {{\n{}\n\t}}\n}}"
frameTempltStr = "{{ -- {}\n{}\n\t\t}}"
cfTempltString = "\t\t\t{} = c({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"

# Turns everything into a lua text file we can use in roblox
def serializeAsLua(frames):
	allFramesStr = ""
	firstFrame = True
	for i in range(0, len(frames)-1):
		frame = frames[i]
		thisFrameStr = ""
		firstTransform = True
		for partName, cfComponents in frame.items():
			# Unpack components in list with * operator
			cfStr = cfTempltString.format(partName, *cfComponents)
			# If this is the first CFrame, we don't wan't a comma and a newline
			# before it.
			proceedStr = not firstTransform and ",\n" or ""
			thisFrameStr += proceedStr + cfStr
			firstTransform = False

		# Proceed str helps us get the tabbing for the frame tables right
		proceedStr = firstFrame and "		" or ","
		allFramesStr += proceedStr + frameTempltStr.format(i+1, thisFrameStr)
		firstFrame = False

	playbackFps = bpy.context.scene.render.fps
	serializedAnimation = luaTempltStr.format(playbackFps, allFramesStr)
	
	return serializedAnimation

## ---- Addon Boilerplate ---- ##

# Addon metadata
bl_info = {
    "name" : "Rbx CFrame Exporter",
    "author" : "zoebasil",
    "description" : "Exports roblox animations",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "category" : "Import-Export"
}

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator

# Operator class; how we register functionality blender can interface with
class exportRbxCFrames(Operator, ExportHelper):
	bl_idname = "objects.rbx_cf_export"
	bl_label = "Export CFrames"
	bl_description = "Exports animation as Roblox CFrames"

	filename_ext = ".lua"

	filter_glob: StringProperty(
		default="*.lua",
		options={'HIDDEN'},
		maxlen=255,
	)

	# Export code
	def execute(self, context):
		if EXPORT_COLLECTION_NAME in bpy.data.collections:
			animationData = serializeAsLua(getAnimationCFrames())

			f = open(self.filepath, 'w', encoding='utf-8')
			f.write(animationData)
			f.close()
		else:
			self.report({'ERROR'}, "Cannot export CFrames, no '{}' collection.".format(EXPORT_COLLECTION_NAME))

		return {'FINISHED'}

def menu_func_export(self, context):
	self.layout.operator(exportRbxCFrames.bl_idname, text="Roblox CFrames (.lua)")

# Register to export topbar
def register():
	bpy.utils.register_class(exportRbxCFrames)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
	bpy.utils.unregister_class(exportRbxCFrames)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

# Registers our code when we run in blender python command window
if __name__ == "__main__":
	register()
