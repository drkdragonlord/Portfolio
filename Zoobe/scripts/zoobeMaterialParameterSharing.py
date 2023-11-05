import maya.cmds as cmds
import maya.OpenMayaUI as mui
import maya.mel as mel
import PyQt4.QtCore as qtcore
import PyQt4.QtGui as qtgui
import sip
import zoobeTools as tools


#--------------------------------------------------------------------------------------
# This class will make sure that specific materials can share specific parameters
class MaterialParameterSharing():
	watchedMaterials = dict()
	objectWatchJobIdentifier = dict()
	currentlyApplyingMat = ""


	#--------------------------------------------------------------------------------------
	# Constructor
	def __init__(self):
		# Assign function to check if a material was selected
		cmds.scriptJob(cc = ["SomethingSelected", self.checkSelection], permanent = True)
		cmds.scriptJob(ct = ["SomethingSelected", self.checkSelection], permanent = True)
		cmds.scriptJob(cf = ["SomethingSelected", self.checkSelection], permanent = True)
		cmds.scriptJob(e = ["SceneOpened", self.getMaterialsFromScene], permanent = True)


	#--------------------------------------------------------------------------------------
	# Checks if the current selection is a cgfx shader.
	# If it is, it is added to the parameter watch (if it is not already there)
	def checkSelection(self):
		# Make sure that current selection is a cgfx shader of the correct type
		# and not already being watched
		selected = cmds.ls(sl = True)
		if len(selected) == 0:
			return

		self.addMaterialWatch(selected[0])


	#--------------------------------------------------------------------------------------
	# Adds the passed material name to the watch (if not already there)
	def addMaterialWatch(self, p_matName):
		print("Check material for parameter sharing: " + p_matName)
		if cmds.nodeType(p_matName) == "cgfxShader" and cmds.objExists("%s.ZoobeShader" %p_matName) and not p_matName in self.watchedMaterials:
			# Add material name to watched materials
			matName = p_matName
			self.watchedMaterials[matName] = matName

			# Add listeners to parameter changes
			self.addWatchScriptJob("%s.NumLights" %matName, lambda: self.updateParameterOnWatchedMaterials(("NumLights", "float"), matName))
			self.addWatchScriptJob("%s.DirLight0" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight0", "light"), matName))
			self.addWatchScriptJob("%s.DirLight0Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight0Color", "float3"), matName))
			self.addWatchScriptJob("%s.DirLight1" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight1", "light"), matName))
			self.addWatchScriptJob("%s.DirLight1Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight1Color", "float3"), matName))
			self.addWatchScriptJob("%s.DirLight2" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight2", "light"), matName))
			self.addWatchScriptJob("%s.DirLight2Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("DirLight2Color", "float3"), matName))
			self.addWatchScriptJob("%s.PointLight0" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight0", "light"), matName))
			self.addWatchScriptJob("%s.PointLight0Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight0Color", "float3"), matName))
			self.addWatchScriptJob("%s.PointLight0AttC" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight0AttC", "float"), matName))
			self.addWatchScriptJob("%s.PointLight0AttL" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight0AttL", "float"), matName))
			self.addWatchScriptJob("%s.PointLight0AttQ" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight0AttQ", "float"), matName))
			self.addWatchScriptJob("%s.PointLight1" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight1", "light"), matName))
			self.addWatchScriptJob("%s.PointLight1Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight1Color", "float3"), matName))
			self.addWatchScriptJob("%s.PointLight1AttC" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight1AttC", "float"), matName))
			self.addWatchScriptJob("%s.PointLight1AttL" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight1AttL", "float"), matName))
			self.addWatchScriptJob("%s.PointLight1AttQ" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight1AttQ", "float"), matName))
			self.addWatchScriptJob("%s.PointLight2" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight2", "light"), matName))
			self.addWatchScriptJob("%s.PointLight2Color" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight2Color", "float3"), matName))
			self.addWatchScriptJob("%s.PointLight2AttC" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight2AttC", "float"), matName))
			self.addWatchScriptJob("%s.PointLight2AttL" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight2AttL", "float"), matName))
			self.addWatchScriptJob("%s.PointLight2AttQ" %matName, lambda: self.updateParameterOnWatchedMaterials(("PointLight2AttQ", "float"), matName))

			print("Added %s to the materials being watched." %matName)


	#--------------------------------------------------------------------------------------
	# Adds a script job to the watch.
	#	Will output an error if the object doesn't exist.
	def addWatchScriptJob(self, p_object, p_function):
		if cmds.objExists(p_object):
			print("Putting into watch: " + p_object)
			self.objectWatchJobIdentifier[p_object] = cmds.scriptJob(attributeChange = [str(p_object), p_function], allChildren = True, killWithScene = True, runOnce = True)
		else:
			cmds.warning("Could not add listener. " + str(p_object) + " doesn't exist.")


	#--------------------------------------------------------------------------------------
	# Updates the passed attribute on all materials that are being watched
	# @param p_attribute				The attribute that caused the callback.
	#														It must be a tuple of size 2.
	#														The first tuple variable is the attribute name.
	#														The second tuple variable is the attribute type (light, float, float2, float3, etc.)
	# @param p_listenerFunction	The listener function to clear & re-add
	#	@param p_originMat				The original material this function was assigned to.
	def updateParameterOnWatchedMaterials(self, p_attribute, p_originMat):
		matName = cmds.ls(sl = True)[0] if len(cmds.ls(sl = True)) > 0 else "INVALID!"

		if matName == "INVALID!":
			return

		# If this is not the material DOING the update, re-add the scriptJob and skip (lest we end up in an endless loop)
		if matName != p_originMat:
			self.addWatchScriptJob("%s.%s" % (p_originMat, p_attribute[0]), lambda: self.updateParameterOnWatchedMaterials(p_attribute, p_originMat))
			return

		print("Updating Attributes, caused by attribute: " + matName + "." + p_attribute[0])
		if self.currentlyApplyingMat == "":
			self.currentlyApplyingMat = matName

			# Get the changed values
			value = ""
			object = "%s.%s" % (matName, p_attribute[0])
			# If this is a connection destination, get the source, not the value
			if p_attribute[1] == "light":
				connectionName = cmds.connectionInfo(object, sourceFromDestination = True)
				if connectionName != "":
					connectionName = connectionName.replace(".worldVector", "")
					print("Light connection name: " + connectionName)
					connections = cmds.listConnections(connectionName, s = True, d = False)
					if connections != None and len(connections) > 0:
						print("Light original light name: " + connections[0])
						value = connections[0]
					else:
						print("No light connection - removing light from all materials.")
						value = ""
				else:
					print("No light connection - removing light from all materials.")
					value = ""
			# Otherwise, just get the value
			else:
				value = cmds.getAttr(object)
				if type(value) is list:
					value = value[0]

			# Update all the OTHER watched materials
			namesToRemove = []
			for watchedMatName in self.watchedMaterials:
				if matName != watchedMatName:
					# Mark material name for removal if it doesn't exist any more
					if not cmds.objExists(watchedMatName):
						namesToRemove.append(watchedMatName)
					# Apply the changed values
					else:
						if p_attribute[1] == "light":
							evalString = "cgfxShader_connectVector %s.%s \"%s\";" % (watchedMatName, p_attribute[0], value)
							print("Changing light with: " + evalString)
							mel.eval(evalString)
						elif p_attribute[1] == "float3":
							print("Changing float3 for: " + watchedMatName + "." + p_attribute[0])
							cmds.setAttr("%s.%s" % (watchedMatName, p_attribute[0]), value[0], value[1], value[2])
						elif p_attribute[1] == "float2":
							print("Changing float2 for: " + watchedMatName + "." + p_attribute[0])
							cmds.setAttr("%s.%s" % (watchedMatName, p_attribute[0]), value[0], value[1])
						else:
							print("Setting float to: " + str(value) + " : " + "%s.%s" % (watchedMatName, p_attribute[0]))
							cmds.setAttr("%s.%s" % (watchedMatName, p_attribute[0]), value)

			# Remove marked materials
			for name in namesToRemove:
				del self.watchedMaterials[name]

			# Re-add script job
			object = "%s.%s" % (matName, p_attribute[0])
			self.addWatchScriptJob(object, lambda: self.updateParameterOnWatchedMaterials(p_attribute, matName))

			# Clear the currentlyApplyingMat
			self.currentlyApplyingMat = ""
			print("Updating Attribute finished.")


	#--------------------------------------------------------------------------------------
	# Restores the watched material list from the loaded scene.
	# Useful so materials don't have to be clicked first.
	def getMaterialsFromScene(self):
		materialNames = cmds.ls(mat = True)

		if len(materialNames) == 0:
			return

		# Iterate over each material in the scene and add it to the watch
		for matName in materialNames:
			self.addMaterialWatch(matName)