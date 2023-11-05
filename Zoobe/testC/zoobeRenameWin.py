import os
import sys
import maya.cmds as cmds
import maya.mel as mel

#Global variables, only to be used in window size parameters
ht=100
wt=280
tlc=200

#Global variable to use in currently open scen querry
openScene = cmds.file(query=True, expandName=True)

def zoobeRenameWin():
	global ht
	global wt
	global tlc
	#s1 = "deleted"
	#s2 = "edited"
	
	#gMainWindow = mel.eval('$tmpVar=$gMainWindow')
	#cmds.window( gMainWindow, edit=True, widthHeight=(900, 777) )
	
	if(cmds.window('testWin', exists=True)):
		cmds.deleteUI('testWin')
		#print(s1)
	if(cmds.windowPref('testWin', exists=True)):
		cmds.windowPref('testWin', edit=True, width=wt, height=ht, topLeftCorner=(tlc, tlc))
		#print(s2)
	
	testWin = cmds.window('testWin', width=wt, height=ht, topLeftCorner=(tlc, tlc), title="Zoobe Prefix Replace v1.0")
	mainCl = cmds.columnLayout('mainCl', width=(wt-10), height=(ht-10))
	mainTabLO = cmds.tabLayout('mainTabLO', height=(ht-2), width=(wt-2), tabsVisible=True, enableBackground=True, sc='zoobeRenameWin.changeTabCmd()')
	
	#Single Scene Column Layout
	singleScene = cmds.columnLayout('singleScene', width=(wt), height=(ht))	
	#Single Scene Form Layout and children
	singleForm = cmds.formLayout(nd=100)	
	#Children of singleForm
	searchField = cmds.textFieldGrp('searchField', cw=((1,45),(2, 200)), label='Search', text='', width=(wt-30))	
	replaceField = cmds.textFieldGrp('replaceField', cw=((1,45),(2, 200)), label='Replace', text='', width=(wt-30))	
	performBtn = cmds.button(width=(wt-210), height=(ht-80), label='Execute', command="zoobeRenameWin.getArgsProc()")
	
	cmds.formLayout(singleForm, edit=True, 
	af=[	
	(searchField, 'left', 5), 
	(searchField, 'top', 2),	
	
	(replaceField, 'left', 5), 
	(replaceField, 'top', 25),
	
	(performBtn, 'left', 180), 
	(performBtn, 'top', 50)
	])
	
	#Parenting back to the Tab Layout
	cmds.setParent('mainTabLO')
	
	#Multiple Scenes Column Layout
	multiScene = cmds.columnLayout('multiScene', width=(wt+100), height=(ht+100))	
	#Multiple Scenes Form Layout and children
	multiForm = cmds.formLayout(nd=100)	
	#Children of singleForm
	browseDirField = cmds.textFieldButtonGrp('browseDirField', cw=((1, 110), (2, 290), (3, 120)), ed=0, bl='browse...', bc='zoobeRenameWin.getScenesDir()', l='Animations Directory: ', tx='', w=(wt+200) )
	scenesList = cmds.textScrollList('scenesList', numberOfRows=8, allowMultiSelection=True, w=(wt+185), h=(ht+95))
	multSearchField = cmds.textFieldGrp('multSearchField', cw=((1,45),(2, 180)), label='Search', text='', width=(wt-30))	
	multReplaceField = cmds.textFieldGrp('multReplaceField', cw=((1,45),(2, 180)), label='Replace', text='', width=(wt-30))	
	multPerformBtn = cmds.button(width=(wt+185), height=(ht-80), label='Execute', command="zoobeRenameWin.getMultiArgsProc()")
	
	cmds.formLayout(multiForm, edit=True, 
	af=[	
	
	(browseDirField, 'left', 5), 
	(browseDirField, 'top', 2),
	
	(scenesList, 'left', 5), 
	(scenesList, 'top', 32),
	
	(multSearchField, 'left', 0), 
	(multSearchField, 'top', 230),	
	
	(multReplaceField, 'left', 240), 
	(multReplaceField, 'top', 230),
	
	(multPerformBtn, 'left', 2), 
	(multPerformBtn, 'top', 255)
	])
	
	#Parenting Back to the Main Column Layout
	cmds.setParent('mainCl')

	#Editing the labels of the Tab Layout
	cmds.tabLayout('mainTabLO', edit=True, tabLabel=(('singleScene', 'Single Scene'), ('multiScene', 'Multi Scene') ))	
	
	cmds.showWindow(testWin)
	
if __name__ == "__zoobeRenameWin__": zoobeRenameWin()

def getArgsProc():

	search = cmds.textFieldGrp('searchField', query=True, text=True)
	replace = cmds.textFieldGrp('replaceField', query=True, text=True)
	
	if(search == ''):
		cmds.warning('No text input in the search field found! Please input some text and try again.')
	else:
		#print(search)
		sceneRename(search, replace)
		cmds.select(clear=True)
	#if(replace == ''):
	#	print("' "+replace+"'")
	#else:
	#	print(replace)
		
def getMultiArgsProc():

	search = cmds.textFieldGrp('multSearchField', query=True, text=True)
	replace = cmds.textFieldGrp('multReplaceField', query=True, text=True)
	
	if(search == ''):
		cmds.warning('No text input in the search field found! Please input some text and try again.')
	else:
		#print(search)
		multiSceneRename(search, replace)
		cmds.select(clear=True)
		
def sceneRename(search, replace):

	scene = cmds.select(all=True)
	sceneSel = cmds.ls(selection=True)
	
	sceneLen = len(sceneSel)
	newSel = ''
	
	print(sceneLen)
	strLen = len(search)
	newObj = ''
	for obj in sceneSel:
		if(replace == ""):
			if(obj[0:strLen] == search):
				#print(obj)
				obj = obj[strLen:]
				newObj = obj
				#cmds.rename(obj, obj[14:])
				#print(newObj)
			continue
		else:
			if(obj[0:strLen] == search):
				#print(obj)
				obj = replace+obj[strLen:]
				newObj = obj
				#cmds.rename(obj, obj[14:])
				#print(newObj)
			continue
	return(newObj)
	
def changeTabCmd():
	
	global ht
	global wt
	
	checkTab = cmds.tabLayout('mainTabLO', query=True, sti=True )
	#print(checkTab)
	
	if(checkTab == 1):
		#print('hello')
		cmds.window('testWin', edit=True, w=(wt), h=(ht))
		cmds.columnLayout('mainCl', edit=True, w=(wt-10), h=(ht-10))
		cmds.columnLayout('multiScene', edit=True, w=(wt+100), h=(ht+100))
		cmds.tabLayout('mainTabLO', edit=True,  height=(ht-2), width=(wt-2))
	else:
		#print('goodbye')
		cmds.window('testWin', edit=True, w=(wt+200), h=(ht+200))
		cmds.columnLayout('mainCl', edit=True, w=(wt+200), h=(ht+200))
		cmds.columnLayout('multiScene', edit=True, w=(wt+200), h=(ht+200))
		cmds.tabLayout('mainTabLO', edit=True,  height=(ht+202), width=(wt+202))
		
def getScenesDir():
	
	global ht
	global wt
	
	path = cmds.fileDialog2(fileMode=3)
	
	nPath = path
	
	pathStr = str(nPath)
	
	pathLen = len(pathStr)
	
	if(pathStr[0:3]== "[u'"):
		pathStr = pathStr.replace("[u'","")
		pathStr = pathStr.replace("']","")
	#print(pathStr)
	
	cmds.textFieldButtonGrp('browseDirField', edit=True, text=(pathStr+"/"))
	
	os.chdir(pathStr)
	for files in os.listdir("."):
		if files.endswith(".mb" or ".ma"):
			cmds.textScrollList('scenesList', edit=True, append=files)

def multiSceneRename(search, replace):
		
	selScenes = cmds.textScrollList('scenesList', query=True, selectIndexedItem=True)
	nameSelScenes = cmds.textScrollList('scenesList', query=True, selectItem=True)
	dirPath = cmds.textFieldButtonGrp('browseDirField', query=True, text=True)
	
	#print(nameSelScenes)
	
	'''
	nameList = []
	nameStr = ''
	#print(nameSelScenes)
	
	cnt = 0
	
	for name in nameSelScenes:
		if((len(selScenes) != 0)and(len(selScenes) != 1)):
			name = name.replace("[u'","")
			name = name.replace("']","")
			name = name.replace("u'","")
			nameStr = str(name)
			nameList.insert(cnt, nameStr)
			++cnt
			#print(nameStr)
		else:
			name = name.replace("[u'","")
			name = name.replace("']","")
			nameStr = str(name)
			nameList.insert(cnt, nameStr)
			++cnt
			#print(nameStr)
	'''
	
	i = 0
	j = 0
	nameList = []
	for name in nameSelScenes:
		#print(name)
		nameList += [str(name)]
		i += 1
		
		'''#This was a loop to get the index value of the selections, not needed since we executed in the form of a range loop
		for sel in selScenes:
			idx = sel
			#print(idx)
			doRename(search, replace, "blah")
		'''
		
	for x in range(0,(len(selScenes)),1):
		#print(nameList[x])
		doRename(search, replace, nameList[x], dirPath, (len(selScenes)), x)
	#print(nameList[0])
	
	'''
	scene = cmds.select(all=True)
	sceneSel = cmds.ls(selection=True)
	
	sceneLen = len(sceneSel)
	newSel = ''
	
	print(sceneLen)
	newObj = ''
	for obj in sceneSel:
		if(obj[0:14] == search):
			#print(obj)
			obj = obj[14:]
			newObj = obj
			#cmds.rename(obj, obj[14:])
			print(newObj)
		continue
	
	return(newObj)
	'''

def doRename(search, replace, fileStr, dir, iter, x):	
	
	global openScene	
	
	if(x!=iter):
		x+=1 
		if((openScene[-3:] == ".mb") or (openScene[-3:] == ".ma")):
			if((cmds.file((dir+fileStr), query=True, exists=True))):
				cmds.file((dir+fileStr), force=True, open=True)
				sceneRename(search, replace)
		else:
			if((cmds.file((dir+fileStr), query=True, exists=True))):
				cmds.file((dir+fileStr), force=True, open=True)
				sceneRename(search, replace)	
	if((openScene[-3:] == ".mb") or (openScene[-3:] == ".ma")):
		cmds.file((openScene), force=True, open=True)
	else:
		cmds.file(force=True, newFile=True)
	print("Operation Completed Successfully!")
	