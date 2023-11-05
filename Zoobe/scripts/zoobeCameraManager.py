import maya.cmds as cmds
import maya.OpenMayaUI as mui
import maya.mel as mel
import PyQt4.QtCore as qtcore
import PyQt4.QtGui as qtgui
import sip
import zoobeTools as tools
import xml.dom.minidom as minidom
import math


#--------------------------------------------------------------------------------------
#	Stores information about a single light
class CamInfo():
	def __init__(self):
		self.color = ()
		self.position = ()
		self.direction = ()
		self.attenuation = ()


#--------------------------------------------------------------------------------------
# This class enables the export and import of the light situation in the Maya scene to/from a format readable by our engine.
class CameraManager():
	#--------------------------------------------------------------------------------------
	# Opens a window to select the file to save to. Then collects the information of the lighting in the scene and finally does the export.
	# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
	def exportCamera(self, p_someBool):
		#check if selected object is a camera
		selected = cmds.ls(sl=1)
		if selected != None:
			shapes = cmds.listRelatives(shapes = 1)
			if not shapes or cmds.nodeType(shapes[0]) != "camera":
					cmds.error("No camera selected.")

			# Open file selection dialog
			fileName = qtgui.QFileDialog.getSaveFileName(None, "Export Camera", "", "Camera TXT(*.txt)")

			# Abort if nothing was chosen
			if fileName == "":
				print("No file selected. Aborting Camera export.")
				return

			# Open file
			fileRef = open(fileName, "w")
			if not fileRef:
				cmds.error("Cant open file %s" %fileName)

			camPos = cmds.camera(shapes[0], q=1, p=1)
			camRot = cmds.camera(shapes[0], q=1, rot=1)
			fileRef.write( "%f\n" % camPos[0])
			fileRef.write( "%f\n" % camPos[1])
			fileRef.write( "%f\n" % camPos[2])

			fileRef.write( "%f\n" % camRot[0])
			fileRef.write( "%f\n" % camRot[1])
			fileRef.write( "%f\n" % camRot[2])

			fileRef.write( "%f\n" % cmds.camera(shapes[0], q=1, vfv=1))
			fileRef.close()

			return

		# If we reach this, no camera was selected
		cmds.error("You need to select a camera for the export.")