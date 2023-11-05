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
class LightInfo():
	def __init__(self):
		self.color = ()
		self.position = ()
		self.direction = ()
		self.attenuation = ()

#--------------------------------------------------------------------------------------
# @param p_string The string to check.
# @return	True if the string is "True", False if else
def stringIsTrue(p_string):
	return str(p_string) == "True"

#--------------------------------------------------------------------------------------
# This class enables the export and import of the light situation in the Maya scene to/from a format readable by our engine.
class LightsetManager():
	#--------------------------------------------------------------------------------------
	# Opens a window to select the file to save to. Then collects the information of the lighting in the scene and finally does the export.
	# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
	def exportLightset(self, p_someBool):
		# Check if we even have a material using our shaders
		materials = cmds.ls(mat = True)
		if len(materials) > 0:
			for matName in materials:
				if cmds.objExists("%s.ZoobeShader" %matName):
					print("Using material \"" + matName + "\" for export.")

					# Open file selection dialog
					fileName = qtgui.QFileDialog.getSaveFileName(None, "Export Lightset", "", "Lightset XML(*.xml)")

					# Abort if nothing was chosen
					if fileName == "":
						print("No file selected. Aborting Lighset export.")
						return

					# Get the values
					print("Reading values.")
					lightDivisor = cmds.getAttr(matName + ".NumLights")
					dirLight0 = LightInfo()
					dirLight0.color = cmds.getAttr(matName + ".DirLight0Color")[0]
					dirLight0.direction = cmds.getAttr(matName + ".DirLight0")[0]
					dirLight1 = LightInfo()
					dirLight1.color = cmds.getAttr(matName + ".DirLight1Color")[0]
					dirLight1.direction = cmds.getAttr(matName + ".DirLight1")[0]
					dirLight2 = LightInfo()
					dirLight2.color = cmds.getAttr(matName + ".DirLight2Color")[0]
					dirLight2.direction = cmds.getAttr(matName + ".DirLight2")[0]
					pointLight0 = LightInfo()
					pointLight0.color = cmds.getAttr(matName + ".PointLight0Color")[0]
					pointLight0.position = cmds.getAttr(matName + ".PointLight0")[0]
					pointLight0.attenuation = (cmds.getAttr(matName + ".PointLight0AttC"), cmds.getAttr(matName + ".PointLight0AttL"), cmds.getAttr(matName + ".PointLight0AttQ"))
					pointLight1 = LightInfo()
					pointLight1.color = cmds.getAttr(matName + ".PointLight1Color")[0]
					pointLight1.position = cmds.getAttr(matName + ".PointLight1")[0]
					pointLight1.attenuation = (cmds.getAttr(matName + ".PointLight1AttC"), cmds.getAttr(matName + ".PointLight1AttL"), cmds.getAttr(matName + ".PointLight1AttQ"))
					pointLight2 = LightInfo()
					pointLight2.color = cmds.getAttr(matName + ".PointLight2Color")[0]
					pointLight2.position = cmds.getAttr(matName + ".PointLight2")[0]
					pointLight2.attenuation = (cmds.getAttr(matName + ".PointLight2AttC"), cmds.getAttr(matName + ".PointLight2AttL"), cmds.getAttr(matName + ".PointLight2AttQ"))

					# Perform gamma correction if desired
					doGammaCorrection = stringIsTrue(cmds.fileInfo("ze_applyGamma", query = True)[0]) if len(cmds.fileInfo("ze_applyGamma", query = True)) > 0 else False
					if doGammaCorrection:
						dirLight0.color[0] = math.pow(dirLight0.color[0], 2.2)
						dirLight0.color[1] = math.pow(dirLight0.color[1], 2.2)
						dirLight0.color[2] = math.pow(dirLight0.color[2], 2.2)
						dirLight1.color[0] = math.pow(dirLight1.color[0], 2.2)
						dirLight1.color[1] = math.pow(dirLight1.color[1], 2.2)
						dirLight1.color[2] = math.pow(dirLight1.color[2], 2.2)
						dirLight2.color[0] = math.pow(dirLight2.color[0], 2.2)
						dirLight2.color[1] = math.pow(dirLight2.color[1], 2.2)
						dirLight2.color[2] = math.pow(dirLight2.color[2], 2.2)
						pointLight0.color[0] = math.pow(pointLight0.color[0], 2.2)
						pointLight0.color[1] = math.pow(pointLight0.color[1], 2.2)
						pointLight0.color[2] = math.pow(pointLight0.color[2], 2.2)
						pointLight1.color[0] = math.pow(pointLight1.color[0], 2.2)
						pointLight1.color[1] = math.pow(pointLight1.color[1], 2.2)
						pointLight1.color[2] = math.pow(pointLight1.color[2], 2.2)
						pointLight2.color[0] = math.pow(pointLight2.color[0], 2.2)
						pointLight2.color[1] = math.pow(pointLight2.color[1], 2.2)
						pointLight2.color[2] = math.pow(pointLight2.color[2], 2.2)

					# Create the XML
					# Open file
					print("Opening file.")
					fileHandle = open(fileName, "wb")

					# Root
					doc = minidom.Document()
					root = doc.createElement("lightset")
					root.setAttribute("lightDivisor", str(lightDivisor))
					doc.appendChild(root)

					# Write lights if they are used
					print("Writing lights.")
					if dirLight0.color[0] > 0.0 or dirLight0.color[1] > 0.0 or dirLight0.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "directional")
						tempChild.setAttribute("x", str(dirLight0.direction[0]))
						tempChild.setAttribute("y", str(dirLight0.direction[1]))
						tempChild.setAttribute("z", str(dirLight0.direction[2]))
						tempChild.setAttribute("colR", str(dirLight0.color[0]))
						tempChild.setAttribute("colG", str(dirLight0.color[1]))
						tempChild.setAttribute("colB", str(dirLight0.color[2]))
						root.appendChild(tempChild)
					if dirLight1.color[0] > 0.0 or dirLight1.color[1] > 0.0 or dirLight1.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "directional")
						tempChild.setAttribute("x", str(dirLight1.direction[0]))
						tempChild.setAttribute("y", str(dirLight1.direction[1]))
						tempChild.setAttribute("z", str(dirLight1.direction[2]))
						tempChild.setAttribute("colR", str(dirLight1.color[0]))
						tempChild.setAttribute("colG", str(dirLight1.color[1]))
						tempChild.setAttribute("colB", str(dirLight1.color[2]))
						root.appendChild(tempChild)
					if dirLight2.color[0] > 0.0 or dirLight2.color[1] > 0.0 or dirLight2.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "directional")
						tempChild.setAttribute("x", str(dirLight2.direction[0]))
						tempChild.setAttribute("y", str(dirLight2.direction[1]))
						tempChild.setAttribute("z", str(dirLight2.direction[2]))
						tempChild.setAttribute("colR", str(dirLight2.color[0]))
						tempChild.setAttribute("colG", str(dirLight2.color[1]))
						tempChild.setAttribute("colB", str(dirLight2.color[2]))
						root.appendChild(tempChild)
					if pointLight0.color[0] > 0.0 or pointLight0.color[1] > 0.0 or pointLight0.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "point")
						tempChild.setAttribute("x", str(pointLight0.position[0]))
						tempChild.setAttribute("y", str(pointLight0.position[1]))
						tempChild.setAttribute("z", str(pointLight0.position[2]))
						tempChild.setAttribute("colR", str(pointLight0.color[0]))
						tempChild.setAttribute("colG", str(pointLight0.color[1]))
						tempChild.setAttribute("colB", str(pointLight0.color[2]))
						tempChild.setAttribute("constF", str(pointLight0.attenuation[0]))
						tempChild.setAttribute("linearF", str(pointLight0.attenuation[1]))
						tempChild.setAttribute("quadF", str(pointLight0.attenuation[2]))
						tempChild.setAttribute("range", str(3000.0))
						root.appendChild(tempChild)
					if pointLight1.color[0] > 0.0 or pointLight1.color[1] > 0.0 or pointLight1.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "point")
						tempChild.setAttribute("x", str(pointLight1.position[0]))
						tempChild.setAttribute("y", str(pointLight1.position[1]))
						tempChild.setAttribute("z", str(pointLight1.position[2]))
						tempChild.setAttribute("colR", str(pointLight1.color[0]))
						tempChild.setAttribute("colG", str(pointLight1.color[1]))
						tempChild.setAttribute("colB", str(pointLight1.color[2]))
						tempChild.setAttribute("constF", str(pointLight1.attenuation[0]))
						tempChild.setAttribute("linearF", str(pointLight1.attenuation[1]))
						tempChild.setAttribute("quadF", str(pointLight1.attenuation[2]))
						tempChild.setAttribute("range", str(3000.0))
						root.appendChild(tempChild)
					if pointLight2.color[0] > 0.0 or pointLight2.color[1] > 0.0 or pointLight2.color[2] > 0.0:
						tempChild = doc.createElement("light")
						tempChild.setAttribute("type", "point")
						tempChild.setAttribute("x", str(pointLight2.position[0]))
						tempChild.setAttribute("y", str(pointLight2.position[1]))
						tempChild.setAttribute("z", str(pointLight2.position[2]))
						tempChild.setAttribute("colR", str(pointLight2.color[0]))
						tempChild.setAttribute("colG", str(pointLight2.color[1]))
						tempChild.setAttribute("colB", str(pointLight2.color[2]))
						tempChild.setAttribute("constF", str(pointLight2.attenuation[0]))
						tempChild.setAttribute("linearF", str(pointLight2.attenuation[1]))
						tempChild.setAttribute("quadF", str(pointLight2.attenuation[2]))
						tempChild.setAttribute("range", str(3000.0))
						root.appendChild(tempChild)

					# Write to and close file
					print("Writing XML file.")
					doc.writexml(fileHandle, indent="", addindent="  ", newl='\n')
					doc.unlink()
					fileHandle.close()
					return

		# If we reach this point, no zoobe shader was found
		cmds.error("Could not find a zoobe shader to read the light information from.")


	#--------------------------------------------------------------------------------------
	# Opens a window to select the file to save to. Then collects the information of the lighting in the scene and finally does the export.
	# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
	def importLightset(self, p_someBool):
		# Open file selection dialog
		fileName = qtgui.QFileDialog.getOpenFileName(None, "Load Lightset File", "", "Lightset XML(*.xml)")

		# Abort if nothing was chosen
		if fileName == "":
			print("No file selected. Aborting Lighset import.")
			return

		# Parse the XML file
		doc = minidom.parse(str(fileName))

		# Get root
		root = doc.getElementsByTagName("lightset")[0]
		lightDivisor = float(root.getAttribute("lightDivisor"))
		print("Light divisor: " + str(lightDivisor))

		# Iterate over all lights
		lights = root.getElementsByTagName("light")
		dirLightCount = 0
		pointLightCount = 0
		for light in lights:
			print("------------------------------")
			lightType = light.getAttribute("type")
			print("Type: " + lightType)
			color = (float(light.getAttribute("colR")), float(light.getAttribute("colG")), float(light.getAttribute("colB")))
			print("Color: " + str(color))

			# Directional? Get direction
			if lightType == "directional":
				direction = (float(light.getAttribute("x")) * 180 / 3.14, float(light.getAttribute("y")) * 180 / 3.14, float(light.getAttribute("z")) * 180 / 3.14)
				print("Direction: " + str(direction))

				# Create light
				lightName = "import_dirLight%d" %dirLightCount
				mayaLight = cmds.directionalLight(name = lightName, position = (8, 6, 8), rotation = direction)

				# Get materials
				materialNames = cmds.ls(mat = True)
				if len(materialNames) > 0:
					for matName in materialNames:
						# If this is a zoobe shader, assign the light to the correct directional slot and set the otther values
						if cmds.nodeType(matName) == "cgfxShader" and cmds.objExists("%s.ZoobeShader" %matName):
							# Light Assignment
							evalString = "cgfxShader_connectVector %s.DirLight%d \"%s\";" % (matName, dirLightCount, lightName)
							print("Assigning light with: " + evalString)
							mel.eval(evalString)

							# Color
							cmds.setAttr("%s.DirLight%dColor" % (matName, dirLightCount), color[0], color[1], color[2])

				# Increase light count
				dirLightCount += 1

			# Point light? Get position, falloff and range
			elif lightType == "point":
				positionVar = (float(light.getAttribute("x")), float(light.getAttribute("y")), float(light.getAttribute("z")))
				print("Position: " + str(positionVar))
				falloff = (float(light.getAttribute("constF")), float(light.getAttribute("linearF")), float(light.getAttribute("quadF")))
				print("Falloff: " + str(falloff))
				rangeVar = float(light.getAttribute("range"))
				print("Range: " + str(rangeVar))

				# Create light
				lightName = "import_pointLight%d" %pointLightCount
				mayaLight = cmds.pointLight(name = lightName, position = positionVar)

				# Get materials
				materialNames = cmds.ls(mat = True)
				if len(materialNames) > 0:
					for matName in materialNames:
						# If this is a zoobe shader, assign the light to the correct directional slot and set the otther values
						if cmds.nodeType(matName) == "cgfxShader" and cmds.objExists("%s.ZoobeShader" %matName):
							# Light Assignment
							evalString = "cgfxShader_connectVector %s.PointLight%d \"%s\";" % (matName, pointLightCount, lightName)
							print("Assigning light with: " + evalString)
							mel.eval(evalString)

							# Color
							cmds.setAttr("%s.PointLight%dColor" % (matName, pointLightCount), color[0], color[1], color[2])

							# Falloff
							cmds.setAttr("%s.PointLight%dAttC" % (matName, pointLightCount), falloff[0])
							cmds.setAttr("%s.PointLight%dAttL" % (matName, pointLightCount), falloff[1])
							cmds.setAttr("%s.PointLight%dAttQ" % (matName, pointLightCount), falloff[2])


				# Increase light count
				pointLightCount += 1