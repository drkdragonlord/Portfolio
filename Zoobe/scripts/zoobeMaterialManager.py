
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import PyQt4.QtCore as qtcore
import PyQt4.QtGui as qtgui
import sip
import zoobeTools as tools


#--------------------------------------------------------------------------------------
# Data class for material assignments
class MaterialAssignmentData():
	def __init__(self):
		self.shaderName = "Zoobe Character"
		self.diffuseTexture = ""
		self.normalTexture = ""
		self.specularTexture = ""
		self.specularPower = 0.0
		self.specularFactor = 0.0
		self.fresnelBias = 0.0
		self.fresnelFallOffAmount = 0.0
		self.fresnelExponent = 0.0
		self.Bump = 0.0
		self.hemiCompressTransition = 0.0
		self.hemiSkyColor = (0.0, 0.0, 0.0)
		self.hemiGroundColor = (0.0, 0.0, 0.0)
		self.hemiLightAmount = 0.0
		self.rimIntensity = 0.0
		self.rimColor = (0.0, 0.0, 0.0)
		self.rimWidth = 0.0
		self.vRimLightDir = (0.0, 0.0, 0.0)
		self.useGlass = False
		self.useEyeHighlight = False
		self.eyeHighlightColor = (0.0, 0.0, 0.0)
		self.eyeHighlightIntensity = 0.0
		self.eyeHighlightShininess = 1.0
		self.vEyeHighlightDir = (0.0, 0.0, 0.0)


#--------------------------------------------------------------------------------------
# This class will manage the material assignments from the original maya materials to our zoobe Ogre materials
class MaterialManager():
	activeMaterialName = ""
	activeShaderName = ""
	activeControls = []
	materialAssignments = dict()
	shaderIndexMap = dict()
	shaderFormFunctionMap = dict()
	materialList = None
	mainLayout = None
	comboBoxShader = None
	refreshButton = None


	#--------------------------------------------------------------------------------------
	# Constructor
	def __init__(self):
		# Initialize material assignment area
		contents = tools.toQtControl("scrlMaterialAssignmentContents")
		self.mainLayout = qtgui.QVBoxLayout(contents)
		contents.setLayout(self.mainLayout)
		tools.toQtControl("scrlMaterialAssignment").setWidget(contents)

		# Add widget for zoobe material selection
		topWidget = qtgui.QWidget()
		topWidget.setGeometry(0, 0, 710, 40)
		topWidget.setFixedHeight(45)
		self.mainLayout.addWidget(topWidget)
		label = qtgui.QLabel("Assigned Zoobe Shader: ", topWidget)
		label.move(0, 2)
		self.comboBoxShader = qtgui.QComboBox(topWidget)
		self.comboBoxShader.move(label.fontMetrics().boundingRect(label.text()).width() + 10, 0)
		self.comboBoxShader.setEnabled(False)

		# Button to refresh values from original scene material
		self.refreshButton = qtgui.QPushButton("Refresh Values From Material", topWidget)
		self.refreshButton.move(label.fontMetrics().boundingRect(label.text()).width() + 230, -2)
		self.refreshButton.clicked.connect(self.refreshButtonClicked)
		self.refreshButton.setEnabled(False)

		# Add shaders
		self.comboBoxShader.addItem("Zoobe Character")
		self.shaderIndexMap["Zoobe Character"] = 0
		self.shaderFormFunctionMap["Zoobe Character"] = self.createFormStandardCharacterShader

		# Restore values saved in the scene
		materialNames = cmds.ls(mat = True)
		for name in materialNames:
			# Create shader assignment data if there is none for the material
			if not name in self.materialAssignments:
				self.materialAssignments[name] = MaterialAssignmentData()
				self.updateAssignmentsFromMaterial(name)

		# Reset shared class variables
		del self.activeControls[:]


	#--------------------------------------------------------------------------------------
	# Will update the material list with all materials from the scene
	# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
	def updateMaterialList(self, p_someBool):
		# Get list widget
		if self.materialList == None:
			self.materialList = tools.toQtControl("lstOriginalMaterials")

		# Clear list first
		self.materialList.clear()

		materialNames = cmds.ls(mat = True)
		for name in materialNames:
			self.materialList.addItem(name)

			# Create shader assignment data if there is none for the material
			if not name in self.materialAssignments:
				self.materialAssignments[name] = MaterialAssignmentData()
				self.updateAssignmentsFromMaterial(name)



	#--------------------------------------------------------------------------------------
	# Updates the display to show the material assignment settings for the selected material
	# @param p_force						If this is True, the material form will be re-created even if the selected material hasn't changed
	# @param p_saveCurrent			If this is True, the currently active values will be stored before the new ones are created.
	# @param p_updateFromScene	If this is True, the assignment values will be updated from the scene, though only if they are still at default values
	def showSelectedMaterial(self, p_force = False, p_saveCurrent = True, p_updateFromScene = True):
		matName = cmds.textScrollList('lstOriginalMaterials', query = True, si = True)[0]

		# Do nothing if the active material was selected
		if self.activeMaterialName == matName and not p_force:
			return

		# Save current values
		#if p_saveCurrent:
		# self.saveActiveValues()
		# self.storeAssignmentsInScene()

		self.activeMaterialName = matName

		# Activate zoobe material selector and refresh button
		self.comboBoxShader.setEnabled(True)
		self.refreshButton.setEnabled(True)

		# Remove active controls
		self.removeActiveControls()

		# Create shader assignment data if there is none for the material
		if not matName in self.materialAssignments:
			self.materialAssignments[matName] = MaterialAssignmentData()

		# Update shader
		self.activeShaderName = self.materialAssignments[matName].shaderName
		self.comboBoxShader.setCurrentIndex(self.shaderIndexMap[self.activeShaderName])

		# Update values from scene
		if p_updateFromScene:
			self.updateAssignmentsFromMaterial(self.activeMaterialName)

		# Display form (this will also fill with values)
		self.shaderFormFunctionMap[self.activeShaderName](self.activeMaterialName)


	#--------------------------------------------------------------------------------------
	# Will remove all active controls
	def removeActiveControls(self):
		# Hide and remove widgets
		for control in self.activeControls:
			control.hide()
			self.mainLayout.removeWidget(control)
			control.setParent(None)
			control = None

		# Clear the array
		del self.activeControls[:]


	#--------------------------------------------------------------------------------------
	# Will refresh the assignments values with the ones from the scene material, but only if a material is selected
	def refreshButtonClicked(self):
		if self.activeMaterialName != "":
			if self.activeShaderName == "Zoobe Character":
				# self.saveActiveValues()
				self.updateAssignmentsFromMaterial(self.activeMaterialName, True)
				self.showSelectedMaterial(True, False, False)


	#--------------------------------------------------------------------------------------
	# Will update the shader assignment values for the current material with the original scene material values.
	# @param p_matName	The name of the (original) material, used for looking up textures, etc.
	# @param p_force		If this is set to True, the values will be updated even if the user has changed them, losing the user changes.
	def updateAssignmentsFromMaterial(self, p_matName, p_force = False):
		# Skip default materials
		if p_matName == "lambert1" or p_matName == "particleCloud1" or p_matName == "shaderGlow1":
			cmds.warning("WARNING: " + p_matName + " is a standard material. We don't use it. Please use zoobe cgfs shaders.")
			return

		# Diffuse texture name
		if self.materialAssignments[p_matName].diffuseTexture == "" or p_force:
			# Diffuse maps are a direct file connection in the material
			if cmds.objExists("%s.diffuseMapSampler" %p_matName):
				fileConnections = cmds.listConnections("%s.diffuseMapSampler" %p_matName, source = True, destination = False, type = "file")
				if fileConnections != None and len(fileConnections) > 0:
					self.materialAssignments[p_matName].diffuseTexture = cmds.getAttr("%s.fileTextureName" %fileConnections[0])
					if self.materialAssignments[p_matName].diffuseTexture.endswith(".psd"):
						cmds.error("ERROR: " + p_matName + ": Ogre cannot use .psd files.")
				else:
					self.materialAssignments[p_matName].diffuseTexture = "None"
			else:
				self.materialAssignments[p_matName].diffuseTexture = "None"
				cmds.warning("WARNING: Could not find diffuseMapSampler in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Specular texture name
		if self.materialAssignments[p_matName].specularTexture == "" or p_force:
			# Specular maps are a direct file connection in the material
			if cmds.objExists("%s.specularMapSampler" %p_matName):
				fileConnections = cmds.listConnections("%s.specularMapSampler" %p_matName, source = True, destination = False, type = "file")
				if fileConnections != None and len(fileConnections) > 0:
					self.materialAssignments[p_matName].specularTexture = cmds.getAttr("%s.fileTextureName" %fileConnections[0])
					if self.materialAssignments[p_matName].specularTexture.endswith(".psd"):
						cmds.error("ERROR: " + p_matName + ": Ogre cannot use .psd files.")
				else:
					self.materialAssignments[p_matName].specularTexture = "None"
			else:
				self.materialAssignments[p_matName].specularTexture = "None"
				cmds.warning("WARNING: Could not find specularMapSampler in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Specularity parameters
		# Power
		if self.materialAssignments[p_matName].specularPower == 0.0 or p_force:
			if cmds.objExists("%s.SpecExpon" %p_matName):
				self.materialAssignments[p_matName].specularPower = cmds.getAttr("%s.SpecExpon" %p_matName)
			else:
				cmds.warning("WARNING: Could not find SpecExpon in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Factor
		if self.materialAssignments[p_matName].specularFactor == 0.0 or p_force:
			if cmds.objExists("%s.Ks" %p_matName):
				self.materialAssignments[p_matName].specularFactor = cmds.getAttr("%s.Ks" %p_matName)
			else:
				cmds.warning("WARNING: Could not find Ks in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Fresnel Parameters
		# Bias
		if self.materialAssignments[p_matName].fresnelBias == 0.0 or p_force:
			if cmds.objExists("%s.fresnelBias" %p_matName):
				self.materialAssignments[p_matName].fresnelBias = cmds.getAttr("%s.fresnelBias" %p_matName)
			else:
				cmds.warning("WARNING: Could not find fresnelBias in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# FallOff Amount
		if self.materialAssignments[p_matName].fresnelFallOffAmount == 0.0 or p_force:
			if cmds.objExists("%s.fresnelFallOffAmount" %p_matName):
				self.materialAssignments[p_matName].fresnelFallOffAmount = cmds.getAttr("%s.fresnelFallOffAmount" %p_matName)
			else:
				cmds.warning("WARNING: Could not find fresnelFallOffAmount in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Exponent
		if self.materialAssignments[p_matName].fresnelExponent == 0.0 or p_force:
			if cmds.objExists("%s.fresnelExponent" %p_matName):
				self.materialAssignments[p_matName].fresnelExponent = cmds.getAttr("%s.fresnelExponent" %p_matName)
			else:
				cmds.warning("WARNING: Could not find fresnelExponent in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Bumpiness
		if self.materialAssignments[p_matName].Bump == 0.0 or p_force:
			if cmds.objExists("%s.Bump" %p_matName):
				self.materialAssignments[p_matName].Bump = cmds.getAttr("%s.Bump" %p_matName)
			else:
				cmds.warning("WARNING: Could not find Bump in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Normal texture name
		if self.materialAssignments[p_matName].normalTexture == "" or p_force:
			# Normal maps are a direct file connection in the material
			if cmds.objExists("%s.normalMapSampler" %p_matName):
				fileConnections = cmds.listConnections("%s.normalMapSampler" %p_matName, source = True, destination = False, type = "file")
				if fileConnections != None and len(fileConnections) > 0:
					self.materialAssignments[p_matName].normalTexture = cmds.getAttr("%s.fileTextureName" %fileConnections[0])
					if self.materialAssignments[p_matName].normalTexture.endswith(".psd"):
						cmds.error("ERROR: " + p_matName + ": Ogre cannot use .psd files.")
				else:
					self.materialAssignments[p_matName].normalTexture = "None"
			else:
				self.materialAssignments[p_matName].normalTexture = "None"
				cmds.warning("WARNING: Could not find normalMapSampler in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Hemi lighting parameters
		# Transition
		if self.materialAssignments[p_matName].hemiCompressTransition == 0.0 or p_force:
			if cmds.objExists("%s.hemiCompressTransition" %p_matName):
				self.materialAssignments[p_matName].hemiCompressTransition = cmds.getAttr("%s.hemiCompressTransition" %p_matName)
			else:
				cmds.warning("WARNING: Could not find hemiCompressTransition in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Sky color
		if len(self.materialAssignments[p_matName].hemiSkyColor) == 0 or self.materialAssignments[p_matName].hemiSkyColor == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.hemiSkyColor" %p_matName):
				self.materialAssignments[p_matName].hemiSkyColor = cmds.getAttr("%s.hemiSkyColor" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find hemiSkyColor in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Ground color
		if len(self.materialAssignments[p_matName].hemiGroundColor) == 0 or self.materialAssignments[p_matName].hemiGroundColor == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.hemiGroundColor" %p_matName):
				self.materialAssignments[p_matName].hemiGroundColor = cmds.getAttr("%s.hemiGroundColor" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find hemiGroundColor in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Amount
		if self.materialAssignments[p_matName].hemiLightAmount == 0.0 or p_force:
			if cmds.objExists("%s.hemiLightAmount" %p_matName):
				self.materialAssignments[p_matName].hemiLightAmount = cmds.getAttr("%s.hemiLightAmount" %p_matName)
			else:
				cmds.warning("WARNING: Could not find hemiLightAmount in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Rim parameters
		# Intensity
		if self.materialAssignments[p_matName].rimIntensity == 0.0 or p_force:
			if cmds.objExists("%s.rimIntensity" %p_matName):
				self.materialAssignments[p_matName].rimIntensity = cmds.getAttr("%s.rimIntensity" %p_matName)
			else:
				cmds.warning("WARNING: Could not find rimIntensity in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Color
		if len(self.materialAssignments[p_matName].rimColor) == 0 or self.materialAssignments[p_matName].rimColor == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.rimColor" %p_matName):
				self.materialAssignments[p_matName].rimColor = cmds.getAttr("%s.rimColor" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find rimColor in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Width
		if self.materialAssignments[p_matName].rimWidth == 0.0 or p_force:
			if cmds.objExists("%s.rimWidth" %p_matName):
				self.materialAssignments[p_matName].rimWidth = cmds.getAttr("%s.rimWidth" %p_matName)
			else:
				cmds.warning("WARNING: Could not find rimWidth in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Direction
		if len(self.materialAssignments[p_matName].vRimLightDir) == 0 or self.materialAssignments[p_matName].vRimLightDir == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.vRimLightDir" %p_matName):
				self.materialAssignments[p_matName].vRimLightDir = cmds.getAttr("%s.vRimLightDir" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find vRimLightDir in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Use glass shader?
		if self.materialAssignments[p_matName].useGlass == False or p_force:
			if cmds.objExists("%s.bUseGlass" %p_matName):
				self.materialAssignments[p_matName].useGlass = cmds.getAttr("%s.bUseGlass" %p_matName)
			else:
				cmds.warning("WARNING: Could not find bUseGlass in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

		# Use eye shader?
		if self.materialAssignments[p_matName].useEyeHighlight == False or p_force:
			if cmds.objExists("%s.bUseEyeHighlight" %p_matName):
				self.materialAssignments[p_matName].useEyeHighlight = cmds.getAttr("%s.bUseEyeHighlight" %p_matName)
			else:
				cmds.warning("WARNING: Could not find bUseEyeHighlight in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Color
		if len(self.materialAssignments[p_matName].eyeHighlightColor) == 0 or self.materialAssignments[p_matName].eyeHighlightColor == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.eyeHighlightColor" %p_matName):
				self.materialAssignments[p_matName].eyeHighlightColor = cmds.getAttr("%s.eyeHighlightColor" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find eyeHighlightColor in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Eye Highlight Intensity
		if self.materialAssignments[p_matName].eyeHighlightIntensity == 0.0 or p_force:
			if cmds.objExists("%s.eyeHighlightIntensity" %p_matName):
				self.materialAssignments[p_matName].eyeHighlightIntensity = cmds.getAttr("%s.eyeHighlightIntensity" %p_matName)
			else:
				cmds.warning("WARNING: Could not find eyeHighlightIntensity in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Eye Highlight Shininess
		if self.materialAssignments[p_matName].eyeHighlightShininess == 0.0 or p_force:
			if cmds.objExists("%s.eyeHighlightShininess" %p_matName):
				self.materialAssignments[p_matName].eyeHighlightShininess = cmds.getAttr("%s.eyeHighlightShininess" %p_matName)
			else:
				cmds.warning("WARNING: Could not find eyeHighlightShininess in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")
		# Eye Highlight Direction
		if len(self.materialAssignments[p_matName].vEyeHighlightDir) == 0 or self.materialAssignments[p_matName].vEyeHighlightDir == (0.0, 0.0, 0.0) or p_force:
			if cmds.objExists("%s.vEyeHighlightDir" %p_matName):
				self.materialAssignments[p_matName].vEyeHighlightDir = cmds.getAttr("%s.vEyeHighlightDir" %p_matName)[0]
			else:
				cmds.warning("WARNING: Could not find vEyeHighlightDir in " + p_matName + ".")
				cmds.warning("WARNING: Is the proper cgfx shader assigned?")

	#--------------------------------------------------------------------------------------
	# Will add the controls for the form of the standard character shader
	# @param p_matName	The name of the (original) material, used for looking up textures, etc.
	def createFormStandardCharacterShader(self, p_matName):
		# Base widget
		topWidget = qtgui.QWidget()
		topWidget.setGeometry(0, 0, 710, 10)
		self.mainLayout.addWidget(topWidget)
		self.activeControls.append(topWidget)

		# Diffuse texture
		currentY = 0
		stepY = 25
		separatorY = 35
		secondColumnX = 145
		label = qtgui.QLabel("Diffuse Texture: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(400)
		lineEdit.setObjectName("txtDiffuseTex")
		lineEdit.setReadOnly(True)
		#lineEdit.editingFinished.connect(self.diffuseTextEdited)
		lineEdit.setText(self.materialAssignments[p_matName].diffuseTexture)

		# Normal texture
		currentY += separatorY
		label = qtgui.QLabel("Normal Texture: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(400)
		lineEdit.setObjectName("txtNormalTex")
		lineEdit.setReadOnly(True)
		lineEdit.setText(self.materialAssignments[p_matName].normalTexture)

		# Specular texture
		currentY += separatorY
		label = qtgui.QLabel("Specular Texture: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(400)
		lineEdit.setObjectName("txtSpecTex")
		lineEdit.setReadOnly(True)
		lineEdit.setText(self.materialAssignments[p_matName].specularTexture)

		# Specular parameters
		# Power
		currentY += stepY
		label = qtgui.QLabel("Specular Power: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtSpecPow")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].specularPower))
		# Factor
		currentY += stepY
		label = qtgui.QLabel("Specular Factor: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtSpecFac")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].specularFactor))

		# Fresnel parameters
		# Bias
		currentY += stepY
		label = qtgui.QLabel("Fresnel Bias: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtFresBias")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].fresnelBias))
		# FallOff
		currentY += stepY
		label = qtgui.QLabel("Fresnel FallOff: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtFresFall")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].fresnelFallOffAmount))
		# Exponent
		currentY += stepY
		label = qtgui.QLabel("Fresnel Exponent: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtFresExpo")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].fresnelExponent))

		# Bumpiness
		currentY += stepY
		label = qtgui.QLabel("Bumpiness: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtBump")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].Bump))

		# Hemi parameters
		# Transition
		currentY += separatorY
		label = qtgui.QLabel("Hemi Transition: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtHemiTrans")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].hemiCompressTransition))
		# Sky color
		currentY += stepY
		label = qtgui.QLabel("Hemi Sky Color: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtHemiSkyCol")
		lineEdit.setReadOnly(True)
		lineEdit.setText("")
		lineEdit.setStyleSheet("QLineEdit { background-color: rgb(%s,%s,%s); }" % (int(self.materialAssignments[p_matName].hemiSkyColor[0] * 255), \
																																								int(self.materialAssignments[p_matName].hemiSkyColor[1] * 255), \
																																								int(self.materialAssignments[p_matName].hemiSkyColor[2] * 255)))
		# Ground color
		currentY += stepY
		label = qtgui.QLabel("Hemi Ground Color: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtHemiGroundCol")
		lineEdit.setReadOnly(True)
		lineEdit.setText("")
		lineEdit.setStyleSheet("QLineEdit { background-color: rgb(%s,%s,%s); }" % (int(self.materialAssignments[p_matName].hemiGroundColor[0] * 255), \
																																								int(self.materialAssignments[p_matName].hemiGroundColor[1] * 255), \
																																								int(self.materialAssignments[p_matName].hemiGroundColor[2] * 255)))
		# Amount
		currentY += stepY
		label = qtgui.QLabel("Hemi Amount: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtHemiAmount")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].hemiLightAmount))

		# Rim Parameters
		# Intensity
		currentY += separatorY
		label = qtgui.QLabel("Rim Intensity: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtRimInt")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].rimIntensity))
		# Color
		currentY += stepY
		label = qtgui.QLabel("Rim Color: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtRimCol")
		lineEdit.setReadOnly(True)
		lineEdit.setText("")
		lineEdit.setStyleSheet("QLineEdit { background-color: rgb(%s,%s,%s); }" % (int(self.materialAssignments[p_matName].rimColor[0] * 255), \
																																								int(self.materialAssignments[p_matName].rimColor[1] * 255), \
																																								int(self.materialAssignments[p_matName].rimColor[2] * 255)))
		# Width
		currentY += stepY
		label = qtgui.QLabel("Rim Width: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtRimWidth")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].rimWidth))
		# Direction
		currentY += stepY
		label = qtgui.QLabel("Rim Direction: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(200)
		lineEdit.setObjectName("txtRimCol")
		lineEdit.setReadOnly(True)
		lineEdit.setText("X: %f Y: %f Z: %f" % (self.materialAssignments[p_matName].vRimLightDir[0],\
																						self.materialAssignments[p_matName].vRimLightDir[1],\
																						self.materialAssignments[p_matName].vRimLightDir[2]))

		# Use glass shader?
		currentY += separatorY
		cb = qtgui.QCheckBox('Use Glass Shader', topWidget)
		cb.move(0, currentY + 2)
		cb.setEnabled(False)
		cb.setChecked(self.materialAssignments[p_matName].useGlass)

		# Use eye shader?
		currentY += separatorY
		cb = qtgui.QCheckBox('Use Eye Highlight', topWidget)
		cb.move(0, currentY + 2)
		cb.setEnabled(False)
		cb.setChecked(self.materialAssignments[p_matName].useEyeHighlight)

		# Eye Highlight Color
		currentY += stepY
		label = qtgui.QLabel("Eye Highlight Color: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtEyeCol")
		lineEdit.setReadOnly(True)
		lineEdit.setText("")
		lineEdit.setStyleSheet("QLineEdit { background-color: rgb(%s,%s,%s); }" % (int(self.materialAssignments[p_matName].eyeHighlightColor[0] * 255), \
																										int(self.materialAssignments[p_matName].eyeHighlightColor[1] * 255), \
																										int(self.materialAssignments[p_matName].eyeHighlightColor[2] * 255)))

		# Eye Highlight Intensity
		currentY += stepY
		label = qtgui.QLabel("Eye Highlight Intensity: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtEyeIntensity")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].eyeHighlightIntensity))

		# Eye Highlight Shininess
		currentY += stepY
		label = qtgui.QLabel("Eye Highlight Shininess: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(100)
		lineEdit.setObjectName("txtEyeShininess")
		lineEdit.setReadOnly(True)
		lineEdit.setText(str(self.materialAssignments[p_matName].eyeHighlightShininess))

		# Eye Highlight Direction
		currentY += stepY
		label = qtgui.QLabel("Eye Highlight Direction: ", topWidget)
		label.move(0, currentY + 2)
		lineEdit = qtgui.QLineEdit(topWidget)
		lineEdit.move(secondColumnX, currentY)
		lineEdit.setFixedWidth(200)
		lineEdit.setObjectName("txtEyeDir")
		lineEdit.setReadOnly(True)
		lineEdit.setText("X: %f Y: %f Z: %f" % (self.materialAssignments[p_matName].vEyeHighlightDir[0],\
																						self.materialAssignments[p_matName].vEyeHighlightDir[1],\
																						self.materialAssignments[p_matName].vEyeHighlightDir[2]))

		# Make sure to force height for containing widget, or else the scrollArea won't react
		topWidget.setGeometry(0, 0, 700, currentY + 25)
		topWidget.setFixedHeight(currentY + 25)

	#--------------------------------------------------------------------------------------
	# Will store the value of the diffuse texture text field
	def diffuseTextEdited(self):
		self.materialAssignments[self.activeMaterialName].diffuseTexture = tools.toQtControl("txtDiffuseTex").text()
		self.storeAssignmentsInScene()


	#--------------------------------------------------------------------------------------
	# Will show a color picker dialog and save the result inside the "txtColor" widget
	def pickColor(self):
		currentCol = qtgui.QColor()
		currentCol.setRed(int(self.materialAssignments[self.activeMaterialName].shadowColor.split(" ")[0].replace(",","")))
		currentCol.setGreen(int(self.materialAssignments[self.activeMaterialName].shadowColor.split(" ")[1].replace(",","")))
		currentCol.setBlue(int(self.materialAssignments[self.activeMaterialName].shadowColor.split(" ")[2].replace(",","")))
		col = qtgui.QColorDialog.getColor(currentCol)

		if col.isValid():
			tools.toQtControl("txtColorR").setText(str(col.red()))
			tools.toQtControl("txtColorG").setText(str(col.green()))
			tools.toQtControl("txtColorB").setText(str(col.blue()))
			tools.toQtControl("squareColor").setStyleSheet("QWidget { background-color: rgb(%i, %i, %i); border:1px solid rgb(0, 0, 0); }" % (col.red(), col.green(), col.blue()))
			self.materialAssignments[self.activeMaterialName].shadowColor = str(col.red()) + " " + str(col.green()) + " " + str(col.blue())
		self.storeAssignmentsInScene()


	#--------------------------------------------------------------------------------------
	# Will update the shadow transit value
	def valueChangedShadowTransit(self, value):
		self.materialAssignments[self.activeMaterialName].shadowTransitSize = float(value) / 100.0
		tools.toQtControl("txtShadowTransitSize").setText(str(float(value) / 100.0))
		self.storeAssignmentsInScene()


	#--------------------------------------------------------------------------------------
	# Will save the active material values in the class
	def saveActiveValues(self):
		if self.activeMaterialName != "":
			if self.activeShaderName == "Zoobe Character":
				self.materialAssignments[self.activeMaterialName].diffuseTexture = tools.toQtControl("txtDiffuseTex").text()
				self.materialAssignments[self.activeMaterialName].specularTexture = tools.toQtControl("txtSpecTex").text()
				self.materialAssignments[self.activeMaterialName].normalTexture = tools.toQtControl("txtNormalTex").text()


	#--------------------------------------------------------------------------------------
	# Will store all the material-shader assignments in the scene.
	def storeAssignmentsInScene(self):
		for key in self.materialAssignments:
			cmds.fileInfo("ze_matAssign_%s___shaderName" %key, str(self.materialAssignments[key].shaderName))
			cmds.fileInfo("ze_matAssign_%s___diffuseTexture" %key, str(self.materialAssignments[key].diffuseTexture))
			cmds.fileInfo("ze_matAssign_%s___normalTexture" %key, str(self.materialAssignments[key].normalTexture))
			cmds.fileInfo("ze_matAssign_%s___specularTexture" %key, str(self.materialAssignments[key].specularTexture))
			cmds.fileInfo("ze_matAssign_%s___specularPower" %key, str(self.materialAssignments[key].specularPower))
			cmds.fileInfo("ze_matAssign_%s___specularFactor" %key, str(self.materialAssignments[key].specularFactor))
			cmds.fileInfo("ze_matAssign_%s___fresnelBias" %key, str(self.materialAssignments[key].fresnelBias))
			cmds.fileInfo("ze_matAssign_%s___fresnelFallOffAmount" %key, str(self.materialAssignments[key].fresnelFallOffAmount))
			cmds.fileInfo("ze_matAssign_%s___fresnelExponent" %key, str(self.materialAssignments[key].fresnelExponent))
			cmds.fileInfo("ze_matAssign_%s___Bump" %key, str(self.materialAssignments[key].Bump))
			cmds.fileInfo("ze_matAssign_%s___hemiCompressTransition" %key, str(self.materialAssignments[key].hemiCompressTransition))
			cmds.fileInfo("ze_matAssign_%s___hemiSkyColor" %key, str(self.materialAssignments[key].hemiSkyColor))
			cmds.fileInfo("ze_matAssign_%s___hemiGroundColor" %key, str(self.materialAssignments[key].hemiGroundColor))
			cmds.fileInfo("ze_matAssign_%s___hemiLightAmount" %key, str(self.materialAssignments[key].hemiLightAmount))
			cmds.fileInfo("ze_matAssign_%s___rimIntensity" %key, str(self.materialAssignments[key].rimIntensity))
			cmds.fileInfo("ze_matAssign_%s___rimColor" %key, str(self.materialAssignments[key].rimColor))
			cmds.fileInfo("ze_matAssign_%s___rimWidth" %key, str(self.materialAssignments[key].rimWidth))
			cmds.fileInfo("ze_matAssign_%s___vRimLightDir" %key, str(self.materialAssignments[key].vRimLightDir))
			cmds.fileInfo("ze_matAssign_%s___useGlass" %key, str(self.materialAssignments[key].useGlass))


	#--------------------------------------------------------------------------------------
	# Will store all the material-shader assignments in the scene.
	def loadAssignmentsFromScene(self):
		# Iterate over each material in the scene
		materialNames = cmds.ls(mat = True)
		for name in materialNames:
			# Create a new material assignment for the material if it doesn't exist yet
			if not name in self.materialAssignments:
				self.materialAssignments[name] = MaterialAssignmentData()

			# Check if we have data stored in the scene for this material
			shaderName = cmds.fileInfo("ze_matAssign_%s___shaderName" %name, query = True)
			if shaderName != None and len(shaderName) > 0 and len(shaderName[0]) > 2:
				self.materialAssignments[name].shaderName = "Zoobe Character"
				self.materialAssignments[name].diffuseTexture = cmds.fileInfo("ze_matAssign_%s___diffuseTexture" %name, query = True)[0] if len(cmds.fileInfo("ze_matAssign_%s___diffuseTexture" %name, query = True)) > 0 else "None"
				self.materialAssignments[name].normalTexture = cmds.fileInfo("ze_matAssign_%s___normalTexture" %name, query = True)[0] if len(cmds.fileInfo("ze_matAssign_%s___normalTexture" %name, query = True)) > 0 else "None"
				self.materialAssignments[name].specularTexture = cmds.fileInfo("ze_matAssign_%s___specularTexture" %name, query = True)[0] if len(cmds.fileInfo("ze_matAssign_%s___specularTexture" %name, query = True)) > 0 else "None"
				self.materialAssignments[name].specularPower = float(cmds.fileInfo("ze_matAssign_%s___specularPower" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___specularPower" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].specularFactor = float(cmds.fileInfo("ze_matAssign_%s___specularFactor" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___specularFactor" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].fresnelBias = float(cmds.fileInfo("ze_matAssign_%s___fresnelBias" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___fresnelBias" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].fresnelFallOffAmount = float(cmds.fileInfo("ze_matAssign_%s___fresnelFallOffAmount" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___fresnelFallOffAmount" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].fresnelExponent = float(cmds.fileInfo("ze_matAssign_%s___fresnelExponent" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___fresnelExponent" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].Bump = float(cmds.fileInfo("ze_matAssign_%s___Bump" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___Bump" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].hemiCompressTransition = float(cmds.fileInfo("ze_matAssign_%s___hemiCompressTransition" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___hemiCompressTransition" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].hemiSkyColor = eval(cmds.fileInfo("ze_matAssign_%s___hemiSkyColor" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___hemiSkyColor" %name, query = True)) > 0 else (0.0, 0.0, 0.0)
				self.materialAssignments[name].hemiGroundColor = eval(cmds.fileInfo("ze_matAssign_%s___hemiGroundColor" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___hemiGroundColor" %name, query = True)) > 0 else (0.0, 0.0, 0.0)
				self.materialAssignments[name].hemiLightAmount = float(cmds.fileInfo("ze_matAssign_%s___hemiLightAmount" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___hemiLightAmount" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].rimIntensity = float(cmds.fileInfo("ze_matAssign_%s___rimIntensity" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___rimIntensity" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].rimColor = eval(cmds.fileInfo("ze_matAssign_%s___rimColor" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___rimColor" %name, query = True)) > 0 else (0.0, 0.0, 0.0)
				self.materialAssignments[name].rimWidth = float(cmds.fileInfo("ze_matAssign_%s___rimWidth" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___rimWidth" %name, query = True)) > 0 else 0.0
				self.materialAssignments[name].rimColor = eval(cmds.fileInfo("ze_matAssign_%s___vRimLightDir" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___vRimLightDir" %name, query = True)) > 0 else (1.0, -1.0, 0.0)
				self.materialAssignments[name].useGlass = bool(cmds.fileInfo("ze_matAssign_%s___useGlass" %name, query = True)[0]) if len(cmds.fileInfo("ze_matAssign_%s___useGlass" %name, query = True)) > 0 else False