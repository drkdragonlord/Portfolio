import maya.cmds as cmds
import maya.utils as utils
import maya.mel as mel
import PyQt4.QtCore as qtcore
import PyQt4.QtGui as qtgui
import sys
import zoobeMaterialManager
import zoobeMaterialParameterSharing
import zoobeLightsetManager
import zoobeCameraManager
import zoobeTools as tools
import batcher
import os
from batcher import Batcher

g_matMan = None
g_matParamSharing = None
g_lightsetMan = None
g_camMan = None
g_pluginLoaded = False
g_uiLaunched = False
g_skelAnimations = {}

#--------------------------------------------------------------------------------------
# Load the plugin
def startUp():
	sys.stdout.write("startUp\n")

	global g_pluginLoaded
	global g_matParamSharing
	global g_lightsetMan
	global g_camMan
	if not g_pluginLoaded:
		cmds.loadPlugin("zoobe_maya_exporter")

		# Create lightset and camera managers
		g_lightsetMan = zoobeLightsetManager.LightsetManager()
		g_camMan = zoobeCameraManager.CameraManager()

		# Create exporter menu entry
		cmds.menu("zoobeOgreWindow", to = 1, aob = 1, parent = "MayaWindow", label = "Zoobe Ogre")
		cmds.menuItem(label = "Character Exporter", command = launchOgreExporter)
		cmds.menuItem(divider=True)
		cmds.menuItem(label = "Import Multiple Animation Clips", command = tools.importMultipleAnimationClips)
		cmds.menuItem(divider=True)
		cmds.menuItem(label = "Export Lightset", command = g_lightsetMan.exportLightset)
		cmds.menuItem(label = "Import Lightset", command = g_lightsetMan.importLightset)
		cmds.menuItem(divider=True)
		cmds.menuItem(label = "Export Selected Camera", command = g_camMan.exportCamera)

		# Assign parameter sharing
		g_matParamSharing = zoobeMaterialParameterSharing.MaterialParameterSharing()

		g_pluginLoaded = True

	sys.stdout.write("startUp - end\n")


#--------------------------------------------------------------------------------------
# Launch exporter UI
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def launchOgreExporter(p_someBool):
	sys.stdout.write("launchExporter\n")
	# Only load once
	global g_uiLaunched
	global g_matMan
	if not cmds.window("ZoobeMainWindow", exists = True):
		# Load QT UI file
		userPath = cmds.internalVar(usd = True)
		cmds.loadUI(f = userPath + "zoobeOgreExporter.ui")

		# Assign material manager
		g_matMan = zoobeMaterialManager.MaterialManager()

		# Add scriptJob to save data when the window is closed
		cmds.scriptJob(uiDeleted = ["ZoobeMainWindow", saveData], runOnce = True)

		# Bind the UI commands
		bindUICommands()

		# Mark UI as launched
		g_uiLaunched = 42;

	# Show the window
	cmds.showWindow("ZoobeMainWindow")

	# Update the animation lists
	updateSkeletonAnimations(False)
	g_matMan.updateMaterialList(False)

	# Load data if saved
	loadData(False)

	sys.stdout.write("launchExporter - end\n")

#--------------------------------------------------------------------------------------
# Binds commands to UI buttons
def bindUICommands():
	sys.stdout.write("bindUICommands\n")
	# Menu bar
	cmds.menuItem("actionExport", edit = True, command = doExport)
	cmds.menuItem("actionSave", edit = True, command = saveData)
	cmds.menuItem("actionLoad", edit = True, command = loadData)
	cmds.menuItem("actionClose", edit = True, command = closeExporter)

	# Material tab
	global g_matMan
	cmds.textScrollList("lstOriginalMaterials", edit = True, sc = g_matMan.showSelectedMaterial)
	cmds.button("btnUpdateMaterialList", edit = True, command = g_matMan.updateMaterialList)
	cmds.button("btnSetAllAnimations", edit = True, command = setAllAnimations)
	cmds.button("btnUnsetAllAnimations", edit = True, command = unsetAllAnimations)

	# Animation tab
	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")
	table.itemDoubleClicked.connect(switchSkeletonAnimSelection)
	cmds.button("btnUpdateSkeletonAnimations", edit = True, command = updateSkeletonAnimations)
	sys.stdout.write("bindUICommands - end\n")

	# Add listeners
	tools.toQtControl("txtMeshFilename").textEdited.connect(meshFilenameEdited)
	tools.toQtControl("txtMeshFilename").textEdited.connect(saveOnChange)
	tools.toQtControl("txtOutputPath").textEdited.connect(saveOnChange)
	tools.toQtControl("txtSingleMaterialName").textEdited.connect(saveOnChange)
	tools.toQtControl("chkExportAnimations").clicked.connect(saveOnChange)
	tools.toQtControl("chkExportMaterials").clicked.connect(saveOnChange)
	tools.toQtControl("chkApplyGammaCorrection").clicked.connect(saveOnChange)
	tools.toQtControl("chkApplyScaling").clicked.connect(saveOnChange)
	tools.toQtControl("chkExportMesh").clicked.connect(saveOnChange)
	tools.toQtControl("mainTabs").currentChanged.connect(saveOnChange)

	# Animation tab             
	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")
	table.itemDoubleClicked.connect(switchSkeletonAnimSelection)
	cmds.button("btnUpdateSkeletonAnimations", edit = True, command = updateSkeletonAnimations)
	
	# Batch export animation #######################################
	table = tools.toQtControl('tblBatchAnimations')
	w = 600
	table.setColumnWidth(0, int(w/10))
	table.setColumnWidth(1, int(w-w/5))#500
	table.setColumnWidth(2, int(w/10))
	table.itemDoubleClicked.connect(switchBatcherAnimSelection)
	cmds.button("browseInDirPushButton", edit = True, command = browseInDir)
	cmds.button("browseOutDirPushButton", edit = True, command = browseOutDir)
	cmds.button("browseRigPushButton", edit = True, command = browseRig)
	cmds.button("batchExportAnimPushButton", edit = True, command = runBatchAnimExport)

	cmds.button("filesSelectAllPushButton", edit = True, command = batchSelAllFiles)
	cmds.button("filesInvSelectionPushButton", edit = True, command = batchInvertSelFiles)
	cmds.button("filesDeselectPushButton", edit = True, command = batchSelNoneFiles)
	
	pb = tools.toQtControl('batcherProgressBar')
	pb.setMinimum(1)
	pb.setMaximum(100)
	#QtCore.QObject.connect(pb, updatePBar)
	pb.hide()
	
#################################################################

##################################################################
#
# Functions to support batch animation export from Maya files
#
##################################################################
import os
from PyQt4 import  QtCore, QtGui
import maya.cmds as mc

def batchSetAllFilesToValue(val):
	table = tools.toQtControl('tblBatchAnimations')
	selFlag = val
	print 'table row count = ', table.rowCount()
	for row in range(table.rowCount()):
		print 'in row ',  row 
		item = table.item(row, 0)
		item.setText(selFlag)
		#item = qtgui.QTableWidgetItem(selFlag)
		#item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		#table.setItem(row, 0, item)
		
def batchSelAllFiles(*args):
	print 'running batchSelAllFiles()'
	batchSetAllFilesToValue('Yes')

def batchSelNoneFiles(*args):
	print 'running batchSelNoneFiles()'
	batchSetAllFilesToValue('No')
	
def batchInvertSelFiles(*args):
	table = tools.toQtControl('tblBatchAnimations')
	for row in range(table.rowCount()):
		selFlag = str(table.item(row, 0).text())
		if selFlag == 'Yes':
			selFlag = 'No'
		elif selFlag == 'No':
			selFlag = 'Yes'
		else:
			raise NameError, "Undefined flag in export files table '%s'. Must be 'Yes' or 'No'" % selFlag
		
		item = qtgui.QTableWidgetItem(selFlag)
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(row, 0, item)

def updatePBar(val):
	pb = tools.toQtControl('batcherProgressBar')
	pb.setValue(val)
	
def getDefaultPathFromOptionVar(var):
	if not mc.optionVar(exists=var):
		mc.optionVar(sv=(var, ''))
		return ''
	return  mc.optionVar(q=var)

def browseInDir(*args):
	mainWindow = tools.toQtControl("ZoobeMainWindow")
	var = 'ogre_batchExport_inDir'
	d = str(QtGui.QFileDialog.getExistingDirectory(mainWindow, "Specify input directory", getDefaultPathFromOptionVar(var))).replace('\\','/')
	cmds.textField('inDirLineEdit', e = True, text = d)

	# save last directory in optionVar
	mc.optionVar(sv=(var, d))

	# fill table
	fileList =  getFilteredFileList(d, isMayaFile)
	fileList.sort()
	table = tools.toQtControl("tblBatchAnimations")
	if not fileList:
		return  False
	
	table.setRowCount(len(fileList))
	for i, f in enumerate(fileList):
		animName = os.path.basename(f).replace('.mb', '')
		animLength = animName.split('_')[-1]
		
		item = qtgui.QTableWidgetItem("Yes")
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(i, 0, item)
		item = qtgui.QTableWidgetItem(animName)
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(i, 1, item)   
		item = qtgui.QTableWidgetItem(animLength)
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(i, 2, item)
	
def isMayaFile(f):
	''' Return true if given file is valid Maya filr, otherwise false. '''
	if f is None or not os.path.isfile(f):
		return False
	_, ext = os.path.splitext(f)
	if not ext == '.mb':
		return False
	return True

def getFilteredFileList(d, filterFunc):
	''' Get all files in given directory. '''
	if d is None or not os.path.isdir(d):
		msg = "Can't find given directory '%s'." % d
		raise NameError, msg
		
	resultList = []
	for f in os.listdir(d):
		f = d + '/' + f
		if os.path.isfile(f):
			if filterFunc(f):
				resultList.append(f.replace('\\', '/'))

	return resultList

def browseRig(*args):
	mainWindow = tools.toQtControl("ZoobeMainWindow")
	var = 'ogre_batchExport_rigFile'
	f = str(QtGui.QFileDialog.getOpenFileName(mainWindow, "Specify anim. rig", getDefaultPathFromOptionVar(var), "Maya (*.mb)")).replace('\\', '/')
	cmds.textField('rigLineEdit', e = True, text = f)
	
	# save last rig file in optionVar
	mc.optionVar(sv=(var, f))
	
def browseOutDir(*args):
	mainWindow = tools.toQtControl("ZoobeMainWindow")
	var = 'ogre_batchExport_outDir'
	d = str(QtGui.QFileDialog.getExistingDirectory(mainWindow, "Specify output directory", getDefaultPathFromOptionVar(var))).replace('\\','/')
	cmds.textField('outDirLineEdit', e = True, text = d)
	#
	# save last directory in optionVar
	mc.optionVar(sv=(var, d))
	#

def runBatchAnimExport(*args):
	inDir = str(cmds.textField('inDirLineEdit', query = True, text = True)).replace('\\', '/')
	outDir = str(cmds.textField('outDirLineEdit', query = True, text = True)).replace('\\', '/')
	rigFileName = str(cmds.textField('rigLineEdit', query = True, text = True)).replace('\\', '/')
	#removePrefixName = str(cmds.textField('searchLineEdit', query = True, text = True))
	scriptName = os.path.dirname(batcher.__file__).replace('\\', '/') + '/exportAnimationToOgre.py'
	#
	sys.stdout.write("scriptName:" + scriptName + "\n")
	# get files to export from table
	table = tools.toQtControl('tblBatchAnimations')
	filesToProcess = []
	for i in range(table.rowCount()):
		if str(table.item(i, 0).text()) == 'No':
			continue
		#
		fName = str(table.item(i, 1).text())
		filesToProcess.append(inDir + '/' + fName + '.mb')
		#
	pb = tools.toQtControl('batcherProgressBar')
	pb.show()
	#
	br = Batcher(inDir=None, outDir=outDir, rigFileName=rigFileName, scriptName=scriptName, filesToProcess=filesToProcess, doSaveFile=False)
	#
	kwargs = {'frameRange':'timeline'}
	if mc.checkBox('bakeAnimExportCheckBox', q=True, v=True):
		kwargs['bakeAnimation'] = True
	#
	if mc.checkBox('stageAnimExportCheckBox', q=True, v=True):
		kwargs['isStageAnimation'] = True
	#
	if mc.checkBox('remPrefixCheckBox', q=True, v=True):
		search = cmds.textField('searchLineEdit', query=True, text=True)
		print(search)
	#
	br.setScriptKwargs(kwargs)
	br.setProgressBarWidget(pb)
	br.run()
	del(br)
	#
	pb.hide()
	#

def switchBatcherAnimSelection(p_clicked):
	# Get table
	table = tools.toQtControl("tblBatchAnimations")   
	   
	# Get selected name and reverse selection
	row = p_clicked.row()
	column = p_clicked.column()
	selFlag = str(table.item(row, 0).text())
	
	if selFlag == 'Yes':
		selFlag = 'No'
	else:
		selFlag = 'Yes'
		
	item = qtgui.QTableWidgetItem(selFlag)
	item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
	table.setItem(row, 0, item)	
	
	
	# Keep item selected
	table.setCurrentCell(row, column)
	
##################################################################
#
# END of batch animation export from Maya files
#
##################################################################

#--------------------------------------------------------------------------------------
# Will copy the edited mesh name to the material name
def meshFilenameEdited():
	tools.toQtControl("txtSingleMaterialName").setText(tools.toQtControl("txtMeshFilename").text())


#--------------------------------------------------------------------------------------
# Save the exporter user data
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def closeExporter(p_someBool):
	sys.stdout.write("closeExporter\n")
	saveData(False)
	cmds.deleteUI("MainWindow")
	sys.stdout.write("closeExporter - end\n")


#--------------------------------------------------------------------------------------
# Save the exporter user data
def saveOnChange():
	saveData(False);

#--------------------------------------------------------------------------------------
# Save the exporter user data (this must be done per Scene)
# In true German Manier, I precede all Variablen with a "ze". ze_exportMesh, ze_meshFilename, etc. ;)
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def saveData(p_someBool):
	sys.stdout.write("WARNING: Close the exporter via Exporter->Close or the data will not be correctly saved.\n Closing via the big X will NOT save the data.\n")

	global g_matMan
	#g_matMan.storeAssignmentsInScene()
	sys.stdout.write("Stored material assignments")

	# Settings tab
	cmds.fileInfo("ze_outputBasePath", cmds.textField("txtOutputPath", query = True, text = True))
	cmds.fileInfo("ze_exportEverything", str(cmds.checkBox("chkEverything", query = True, value = True)))

	# Mesh tab
	cmds.fileInfo("ze_exportMesh", str(cmds.checkBox("chkExportMesh", query = True, value = True)))
	cmds.fileInfo("ze_exportVertexNormals", str(cmds.checkBox("chkVertexNormals", query = True, value = True)))
	cmds.fileInfo("ze_exportVertexBinormals", str(cmds.checkBox("chkVertexBinormals", query = True, value = True)))
	cmds.fileInfo("ze_exportVertexBoneAssignments", str(cmds.checkBox("chkVertexBoneAssignments", query = True, value = True)))
	cmds.fileInfo("ze_exportTextureCoords", str(cmds.checkBox("chkTextureCoords", query = True, value = True)))
	cmds.fileInfo("ze_meshFilename", cmds.textField("txtMeshFilename", query = True, text = True))
	cmds.fileInfo("ze_buildTangents", str(cmds.checkBox("chkBuildTangents", query = True, value = True)))
	cmds.fileInfo("ze_buildEdgesList", str(cmds.checkBox("chkBuildEdgesList", query = True, value = True)))

	# Material tab
	cmds.fileInfo("ze_exportMaterials", str(cmds.checkBox("chkExportMaterials", query = True, value = True)))
	cmds.fileInfo("ze_singleMaterial", str(cmds.checkBox("chkSingleMaterial", query = True, value = True)))
	cmds.fileInfo("ze_singleMaterialName", cmds.textField("txtSingleMaterialName", query = True, text = True))
	cmds.fileInfo("ze_useLightingOff", str(cmds.checkBox("chkUseLightingOff", query = True, value = True)))
	cmds.fileInfo("ze_copyTextures", str(cmds.checkBox("chkCopyTextures", query = True, value = True)))
	cmds.fileInfo("ze_applyGamma", str(cmds.checkBox("chkApplyGammaCorrection", query = True, value = True)))
	cmds.fileInfo("ze_applyScaling", str(cmds.checkBox("chkApplyScaling", query = True, value = True)))

	# Animation tab
	cmds.fileInfo("ze_exportSkeletonAnimations", str(cmds.checkBox("chkExportAnimations", query = True, value = True)))
	cmds.fileInfo("ze_isStageAnim", str(cmds.checkBox("chkIsStageAnim", query = True, value = True)))

	# Skeleton animations
	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")
	if table.rowCount() > 0:
		cmds.fileInfo("ze_numSkeletonAnimations", str(table.rowCount()))
		global g_skelAnimations
		for i in range(0, table.rowCount()):
			name = str(table.item(i, 1).text())
			cmds.fileInfo("ze_skeletonAnim" + str(i), name)
			cmds.fileInfo("ze_skeletonAnim" + str(i) + "length", str(table.item(i, 2).text()))
			if not name in g_skelAnimations:
				g_skelAnimations[name] = cmds.fileInfo("ze_skeletonAnim" + str(i) + "selected", query = True)[0] if len(cmds.fileInfo("ze_skeletonAnim" + str(i) + "selected", query = True)) > 0 else True
			cmds.fileInfo("ze_skeletonAnim" + str(i) + "selected", str(g_skelAnimations[name]))

	# If this flag is set, we know that we have saved data
	cmds.fileInfo("ze_savedData", "True")

	sys.stdout.write("Settings saved.\n")

#--------------------------------------------------------------------------------------
# @param p_string The string to check.
# @return	True if the string is "True", False if else
def stringIsTrue(p_string):
	return str(p_string) == "True"

#--------------------------------------------------------------------------------------
# Loads the data from fileInfo and applies it to the exporter UI
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def loadData(p_someBool):
	sys.stdout.write("loadData\n")

	g_matMan.loadAssignmentsFromScene()
	sys.stdout.write("Loaded material assignments")

	# Only load if data was saved before
	if bool(cmds.fileInfo("ze_savedData", query = True)):
		# Settings tab
		# Replace all \\
		path = str(cmds.fileInfo("ze_outputBasePath", query = True)[0]);
		path = tools.stripDoubleBackslashes(path)
		cmds.textField("txtOutputPath", edit = True, text = path)
		cmds.checkBox("chkEverything", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportEverything", query = True)[0]))

		# Mesh tab
		cmds.checkBox("chkExportMesh", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportMesh", query = True)[0]))
		cmds.checkBox("chkVertexNormals", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportVertexNormals", query = True)[0]) if len(cmds.fileInfo("ze_exportVertexNormals", query = True)) > 0 else True)
		cmds.checkBox("chkVertexBinormals", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportVertexBinormals", query = True)[0]) if len(cmds.fileInfo("ze_exportVertexBinormals", query = True)) > 0 else True)
		cmds.checkBox("chkVertexBoneAssignments", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportVertexBoneAssignments", query = True)[0]))
		cmds.checkBox("chkTextureCoords", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportTextureCoords", query = True)[0]))
		cmds.textField("txtMeshFilename", edit = True, text = str(cmds.fileInfo("ze_meshFilename", query = True)[0]))
		cmds.checkBox("chkBuildTangents", edit = True, value = stringIsTrue(cmds.fileInfo("ze_buildTangents", query = True)[0]))
		cmds.checkBox("chkBuildEdgesList", edit = True, value = stringIsTrue(cmds.fileInfo("ze_buildEdgesList", query = True)[0]))

		# Material tab
		cmds.checkBox("chkExportMaterials", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportMaterials", query = True)[0]))
		cmds.checkBox("chkSingleMaterial", edit = True, value = stringIsTrue(cmds.fileInfo("ze_singleMaterial", query = True)[0]))
		cmds.textField("txtSingleMaterialName", edit = True, text = str(cmds.fileInfo("ze_singleMaterialName", query = True)[0]))
		cmds.checkBox("chkUseLightingOff", edit = True, value = stringIsTrue(cmds.fileInfo("ze_useLightingOff", query = True)[0]))
		cmds.checkBox("chkCopyTextures", edit = True, value = stringIsTrue(cmds.fileInfo("ze_copyTextures", query = True)[0]))
		cmds.checkBox("chkApplyGammaCorrection", edit = True, value = stringIsTrue(cmds.fileInfo("ze_applyGamma", query = True)[0]) if len(cmds.fileInfo("ze_applyGamma", query = True)) > 0 else False)
		cmds.checkBox("chkApplyScaling", edit = True, value = stringIsTrue(cmds.fileInfo("ze_applyScaling", query = True)[0]) if len(cmds.fileInfo("ze_applyScaling", query = True)) > 0 else True)

		# Animation tab
		cmds.checkBox("chkExportAnimations", edit = True, value = stringIsTrue(cmds.fileInfo("ze_exportSkeletonAnimations", query = True)[0]))
		cmds.checkBox("chkIsStageAnim", edit = True, value = stringIsTrue(cmds.fileInfo("ze_isStageAnim", query = True)[0]) if len(cmds.fileInfo("ze_isStageAnim", query = True)) > 0 else False)

		# Skeleton animations
		global g_skelAnimations
		g_skelAnimations.clear()
		numAnims = int(cmds.fileInfo("ze_numSkeletonAnimations", query = True)[0]) if len(cmds.fileInfo("ze_numSkeletonAnimations", query = True)) > 0 else 0
		if numAnims > 0:
			animName = ""
			animLength = ""
			animSelected = ""

			# Get and fill table
			table = tools.toQtControl("tblSkeletonAnimations")
			table.setRowCount(numAnims)
			for i in range(0, numAnims):
				animName = str(cmds.fileInfo("ze_skeletonAnim" + str(i), query = True)[0])
				animLength = str(cmds.fileInfo("ze_skeletonAnim" + str(i) + "length", query = True)[0])
				animSelected = str(cmds.fileInfo("ze_skeletonAnim" + str(i) + "selected", query = True)[0])

				g_skelAnimations[animName] = bool(animSelected)
				if g_skelAnimations[animName]:
					item = qtgui.QTableWidgetItem("Yes")
					item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
					table.setItem(i, 0, item)
				else:
					item = qtgui.QTableWidgetItem("No")
					item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
					table.setItem(i, 0, item)

				item = qtgui.QTableWidgetItem(animName)
				item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
				table.setItem(i, 1, item)
				item = qtgui.QTableWidgetItem(animLength)
				item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
				table.setItem(i, 2, item)

			# Format table
			table.resizeRowsToContents()
			table.setColumnWidth(0, 50)
			table.setColumnWidth(1, 360)
			table.setColumnWidth(2, 50)
	# If not saved before, just print a message
	else:
		sys.stdout.write("Could not load settings: Settings haven't been saved yet.\n")
	sys.stdout.write("loadData - end\n")

#--------------------------------------------------------------------------------------
# Update the skeleton animation list
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def updateSkeletonAnimations(p_someBool):
	sys.stdout.write("updateSkeletonAnimations\n")

	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")

	# Iterate over all animation clip names and add them to the table
	global g_skelAnimations
	names = cmds.clip(query = True, ac = True)
	print(names)
	line = ""
	if not names is None:
		row = 0
		for name in names:
			if not "Source" in name:
				print(name)

				# If not in the list yet, add as selected
				if not name in g_skelAnimations.keys():
					print("New to list")
					g_skelAnimations[name] = True

				# Assign the correct number of rows
				print("Setting row count to: " + str(row + 1))
				table.setRowCount(row + 1)

				# Add the skeleton to the table
				addSkeletonAnimEntry(name, row)
				row += 1

	# Format table
	table.setColumnWidth(0, 50)
	table.setColumnWidth(1, 360)
	table.setColumnWidth(2, 50)
	table.resizeRowsToContents()

	sys.stdout.write("updateSkeletonAnimations - end\n")

#--------------------------------------------------------------------------------------
# Adds a skeleton animation entry to the pseudo table
# @param p_name	The name of the animation to add
# @param p_row	The row to insert the item in
def addSkeletonAnimEntry(p_name, p_row):
	sys.stdout.write("addSkeletonAnimEntry\n")
	print(str(p_name) + " " + str(p_row))

	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")

	# Selected?
	global g_skelAnimations
	print(g_skelAnimations[p_name])
	if g_skelAnimations[p_name]:
		item = qtgui.QTableWidgetItem("Yes")
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(p_row, 0, item)
	else:
		item = qtgui.QTableWidgetItem("No")
		item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
		table.setItem(p_row, 0, item)

	# Name
	item = qtgui.QTableWidgetItem(p_name)
	item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
	table.setItem(p_row, 1, item)

	# Length, actually resides in the sourceEnd attribute... oh, well.
	length = int(cmds.getAttr(p_name + ".sourceEnd"))
	item = qtgui.QTableWidgetItem(str(length))
	item.setFlags(item.flags() & ~qtcore.Qt.ItemIsEditable)
	table.setItem(p_row, 2, item)

	sys.stdout.write("addSkeletonAnimEntry - end\n")


#--------------------------------------------------------------------------------------
# Sets all animations to be exported
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def setAllAnimations(p_someBool):
	global g_skelAnimations
	for key in g_skelAnimations:
		g_skelAnimations[key] = True

	updateSkeletonAnimations(False)


#--------------------------------------------------------------------------------------
# Sets all animations to NOT be exported
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def unsetAllAnimations(p_someBool):
	global g_skelAnimations
	for key in g_skelAnimations:
		g_skelAnimations[key] = False

	updateSkeletonAnimations(False)


#--------------------------------------------------------------------------------------
# @param p_clicked	The clicked item.
def switchSkeletonAnimSelection(p_clicked):
	sys.stdout.write("switchSkeletonAnimSelection\n")
	global g_skelAnimations

	# Get table
	table = tools.toQtControl("tblSkeletonAnimations")

	# Get selected name and reverse selection
	row = p_clicked.row()
	column = p_clicked.column()
	name = str(table.item(row, 1).text())
	g_skelAnimations[name] = not g_skelAnimations[name]

	# Update table
	updateSkeletonAnimations(False)

	# Keep item selected
	table.setCurrentCell(row, column)
	sys.stdout.write("switchSkeletonAnimSelection - end\n")

#--------------------------------------------------------------------------------------
# Exports everything as selected
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def doExport(p_someBool):
	sys.stdout.write("doExport\n")
	saveData(False)
	options = ""

	# Select all meshes and set them to bind pose
	selectedObjs = cmds.ls(selection = True)
	meshes = cmds.ls(type = "mesh")
	toSelect = []
	for meshName in meshes:
		toSelect.append(cmds.listRelatives(meshName, p=1, type='transform')[0])
	cmds.select(toSelect)

	# If this has no animations, we can't go to bind pose
	try:
		mel.eval("gotoBindPose")
	except:
		print("gotoBindPose failed. Export may still work, though.")

	# Restore original selection
	if len(selectedObjs) > 0:
		cmds.select(selectedObjs)
	else:
		cmds.select(clear = True)

	# Settings tab options
	basePath = str(cmds.fileInfo("ze_outputBasePath", query = True)[0])
	basePath = basePath.replace("/", "\\")
	basePath = basePath.replace("\\\\", "\\")
	if not basePath.endswith("\\"):
		basePath += "\\"
	options += " -outDir \"" + basePath + "\""

	if stringIsTrue(cmds.fileInfo("ze_exportEverything", query = True)[0]):
		options += " -all"
	else:
		options += " -sel"

	options += " -lu pref -scale 1.00"

	# Mesh tab options
	if stringIsTrue(cmds.fileInfo("ze_exportMesh", query = True)[0]):
		# Mesh file path
		meshName = str(cmds.fileInfo("ze_meshFilename", query = True)[0])
		if not meshName.endswith(".mesh"):
			meshName += ".mesh"
		options += " -mesh \"" + basePath + meshName + "\""

		# Various mesh options
		if stringIsTrue(cmds.fileInfo("ze_exportVertexNormals", query = True)[0]):
			options += " -n"
		if stringIsTrue(cmds.fileInfo("ze_exportVertexBinormals", query = True)[0]):
			options += " -bn"
		if stringIsTrue(cmds.fileInfo("ze_exportVertexBoneAssignments", query = True)[0]):
			options += " -v"
		if stringIsTrue(cmds.fileInfo("ze_exportTextureCoords", query = True)[0]):
			options += " -t"
		if stringIsTrue(cmds.fileInfo("ze_buildTangents", query = True)[0]):
			options += " -tangents TANGENT"
		options += " -preventZeroTangent 100.0"
		if stringIsTrue(cmds.fileInfo("ze_buildEdgesList", query = True)[0]):
			options += " -edges"

	# Material tab options
	if stringIsTrue(cmds.fileInfo("ze_exportMaterials", query = True)[0]):
		# Single material file
		if stringIsTrue(cmds.fileInfo("ze_singleMaterial", query = True)[0]):
			# Material file path
			matName = str(cmds.fileInfo("ze_singleMaterialName", query = True)[0])
			if not matName.endswith(".material"):
				matName += ".material"
			options += " -mat \"" + basePath + matName + "\""

			# Various material options
			if stringIsTrue(cmds.fileInfo("ze_useLightingOff", query = True)[0]):
				options += " -lightOff"
			if stringIsTrue(cmds.fileInfo("ze_copyTextures", query = True)[0]):
				options += " -copyTex \"" + basePath + "\""
			if stringIsTrue(cmds.fileInfo("ze_applyGamma", query = True)[0]):
				options += " -applyGamma"
			if stringIsTrue(cmds.fileInfo("ze_applyScaling", query = True)[0]):
				options += " -applyScaling"
		# Split material files (not yet)
		else:
			sys.stdout.write("ERROR: Split material files not yet implemented.\n")

	# Animation tab options
	# Skeleton animations
	numAnims = int(cmds.fileInfo("ze_numSkeletonAnimations", query = True)[0]) if len(cmds.fileInfo("ze_numSkeletonAnimations", query = True)) > 0 else 0
	if stringIsTrue(cmds.fileInfo("ze_exportSkeletonAnimations", query = True)[0]) and numAnims > 0:
		# Is this a stage animation?
		isStageAnim = stringIsTrue(cmds.fileInfo("ze_isStageAnim", query = True)[0]) if len(cmds.fileInfo("ze_isStageAnim", query = True)) > 0 else False
		if isStageAnim:
			options += " -stageAnim"

		options += " -skeletonAnims -skelBB -np bindPose"

		# Clips
		animName = ""
		startFrame = ""
		endFrame = ""
		global g_skelAnimations
		for i in range(0, numAnims):
			animName = str(cmds.fileInfo("ze_skeletonAnim" + str(i), query = True)[0])
			if g_skelAnimations[animName]:
				startFrame = str(cmds.getAttr(animName + ".startFrame"))
				endFrame = str(cmds.getAttr(animName + ".sourceEnd") + cmds.getAttr(animName + ".startFrame"))
				options += " -skeletonClip \"" + animName + "\""
				options += " startEnd " + startFrame + " " + endFrame + " frames"
				options += " sampleByFrames 1"

	# Run the exporter
	sys.stdout.write("Running Zoobe Ogre exporter with options:\n" + options + "\n")
	options = options.replace("\\", "\\\\")
	try:
		mel.eval( "ogreExport"+options)
	except:
		cmds.confirmDialog( title='Error', message='Export failed! See command window log for more infos...', button=['Ok'], defaultButton='Ok')

	sys.stdout.write("doExport - end\n")


# We need to execute the startup deferred as this python script is loaded before maya has been fully initialized
cmds.evalDeferred("zoobeOgreExporter.startUp()")
