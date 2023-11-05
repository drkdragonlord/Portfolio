import maya.cmds as cmds
import maya.OpenMayaUI as mui
import maya.mel as mel
import PyQt4.QtCore as qtcore
import PyQt4.QtGui as qtgui
import sip

#--------------------------------------------------------------------------------------
# Strips the passed string of any double backslashes ("\\" -> "\", so only single backslashes will remain)
# and returns the new, stripped string.
# @param p_origString	The string to modify
# @return	The modified string
def stripDoubleBackslashes(p_origString):
		while "\\\\" in p_origString:
			p_origString = p_origString.replace("\\\\", "\\")

		return p_origString


#--------------------------------------------------------------------------------------
# Returns the QtControl with the passed name
# @param p_mayaName
# @return	The PyQt control (QWidget, for example)
def toQtControl(p_mayaName):
	ptr = mui.MQtUtil.findControl(p_mayaName)
	if ptr is not None:
		return sip.wrapinstance(long(ptr), qtgui.QWidget)


#--------------------------------------------------------------------------------------
# Returns the QtLayout with the passed name
# @param p_mayaName
# @return	The PyQt layout (QLayout, for example)
def toQtLayout(p_mayaName):
	ptr = mui.MQtUtil.findLayout(p_mayaName)
	if ptr is not None:
		return sip.wrapinstance(long(ptr), qtgui.QLayout)


#--------------------------------------------------------------------------------------
# Makes any passed widget clickable and returns the clicked QEvent
# @param p_widget	The widget to make clickable
# @return	The clicked QEvent
def makeClickable(widget):
	class Filter(qtcore.QObject):
		clicked = qtcore.pyqtSignal()

		def eventFilter(self, obj, event):
			if obj == widget:
				if event.type() == qtcore.QEvent.MouseButtonRelease:
					self.clicked.emit()
					return True
			return False

	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked

#--------------------------------------------------------------------------------------
# Will open a file dialog in which the user has to select multiple files to import
# animation clips onto the selected skeleton
# @param p_someBool For some reason, adding a function as command will make it pass a Boolean as first parameter.
def importMultipleAnimationClips(p_someBool):
	print("importMultipleAnimationClips start")

	# Check if a skeleton is selected
	characters = mel.eval("getCharactersForAction();")
	if characters is not None and len(characters) <= 0:
		cmds.error("ERROR: You need to select the skeleton.")
		return

	print("importMultipleAnimationClips 1")

	clipsDir = cmds.workspace(q = True, rd = True) + "clips/"
	if cmds.file(clipsDir, q = True, ex = True):
		cmds.workspace(dir = clipsDir)

	# Let the user select some files
	print("importMultipleAnimationClips 2")
	files = qtgui.QFileDialog.getOpenFileNames(None, "Select animation clips to import", "", "Maya Animation Files (*.mb)")

	# No file selected?
	if files is not None and len(files) <= 0:
		cmds.warning("WARNING: No file selected.")
		return

	# Get the frame to start adding clips at
	# Required as there could be clips in the track already
	names = cmds.clip(query = True, ac = True)
	startFrame = 0
	if names is not None and len(names) > 0:
		for name in names:
			animStart = cmds.getAttr(name + ".startFrame")
			animEnd = cmds.getAttr(name + ".sourceEnd") + cmds.getAttr(name + ".startFrame")
			if animEnd > startFrame:
				startFrame = animEnd
	startFrame += 2

	# Get current clip situation
	print("importMultipleAnimationClips 3")
	preSourceClips = cmds.clip(query = True, allSourceClips = True)
	preClipCount = len(preSourceClips)

	# Iterate over each file and add it
	# INFO: From here on, most is just a MEL script translated to Python.
	# Not 100% sure why everything is done as it is
	print("importMultipleAnimationClips 4")
	clipsNotImportet = []
	for fileName in files:
		while "\\" in fileName:
			fileName = fileName.replace("\\", "/")

		# Reference the file into a namespace so we can figure out
		# which clips came from the imported file
		tmpNamespace = "clipImportTmp";
		oldNamespace = cmds.namespaceInfo(cur = True)
		if oldNamespace != ":":
			oldNamespace = ":" + oldNamespace

		print("importMultipleAnimationClips 5")
		cmds.namespace(set = ":")
		mel.eval("file -r -namespace \"" + tmpNamespace + "\" -options \"v=0;p=17\" \"" + fileName + "\";")
		cmds.namespace(set = ":" + tmpNamespace)
		nameSpaceNodes = cmds.namespaceInfo(lod = True)

		cmds.namespace(set = oldNamespace)

		# Copy the included clips to the specified characters
		currentTime = cmds.currentTime(q = True)
		toTrack = 0
		toGroup = ""

		# Copy the files onto the selected characters
		clips = cmds.ls(nameSpaceNodes, type = "animClip")
		for clip in clips:

			# Skip the clip if it exists already
			skip = False
			print("importMultipleAnimationClips 6")
			for existingClip in preSourceClips:
				if "clipImportTmp:" + existingClip == clip:
					cmds.warning("WARNING: Clip \"" + existingClip + "\" already exists. Not added.")
					clipsNotImportet.append(existingClip)
					skip = True
					break
			if skip:
				continue

			print("importMultipleAnimationClips 7")
			if cmds.getAttr(clip + ".clipInstance") == 0:
				for character in characters:
					cmds.clip(clip, copy = True)
					newClips = cmds.clip(character, paste = True, sc = True, mm = "byNodeName")
					if len(newClips) <= 0:
						newClips = cmds.clip(character, paste = True, sc = True, mm = "byAttrName")

					scheduler = cmds.character(character, query = True, scheduler = True)
					for newClip in newClips:
						clipIndex = mel.eval("getClipIndex(\"" + newClip + "\", \"" + scheduler + "\");")
						cmds.clipSchedule(scheduler, clipIndex = clipIndex, track = toTrack, s = startFrame)
						startFrame += cmds.getAttr(clip + ".sourceEnd") + 2

		# Remove the reference
		mel.eval("file -rr \"" + fileName + "\";")

	print("importMultipleAnimationClips 8")
	postSourceClips = cmds.clip(q = True, allSourceClips = True)
	postClipCount = len(postSourceClips)
	if postClipCount == preClipCount:
		print("Files did not contain clips to import.")
	else:
		numClips = postClipCount - preClipCount
		print("Importet clips: " + str(numClips))
	print("Clips not importet: " + " ".join(clipsNotImportet))