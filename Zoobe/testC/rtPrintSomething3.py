import os
import sys
import maya.cmds as cmds
import maya.mel as mel

#Start Global Variables
ht = 350
wt = 550
tlc = 150
zoobeWinTestUI = cmds.window
mainCL = cmds.columnLayout
zoobeRenameTab = cmds.tabLayout
multiScene = cmds.columnLayout
searchStringField = cmds.textFieldGrp
replaceStringField = cmds.textFieldGrp
#End Global Variables

def psource(module):
    file = os.path.basename(module)
    dir = os.path.dirname(module)
    
    toks = file.split('.')
    modname = toks[0]
    
    if(os.path.exists(dir)):
        paths=sys.path
        pathfound=0
        for path in paths:
            if(dir==path):
                pathfound =1
        if not pathfound:
            sys.path.append(dir)
    exec('import '+modname) in globals()
    exec('reload( '+modname+' ) ') in globals()
    
    return modname

psource ('C:/testC/rtPrintSomething3.py')
#rtPrintSomething3.rtTest()
#rtPrintSomething3.zoobeWinTest()

def rtTest():
	print 'hello'
	print 'Im finally working!'
	
def zoobe_RenameChangeTab():

	global ht
	global wt
	global zoobeWinTestUI
	global mainCL
	global zoobeRenameTab
	global multiScene
	
	checkTab = cmds.tabLayout(zoobeRenameTab, query=True, sti=True )
	#print(checkTab)
	
	if(checkTab==1):
		#print('hello')
		cmds.window(zoobeWinTestUI, edit=True, w=(wt-300), h=(ht-225))
		cmds.columnLayout(mainCL, edit=True, w=(wt-300), h=(ht-225))
		cmds.columnLayout(multiScene, edit=True, w=(wt-308), h=(ht-5))
		cmds.tabLayout(zoobeRenameTab, edit=True, h=(ht-225))
	else:
		#print('goodbye')
		cmds.window(zoobeWinTestUI, edit=True, w=(wt), h=(ht))
		cmds.columnLayout(mainCL, edit=True, w=(wt), h=(ht-5))
		cmds.columnLayout(multiScene, edit=True, w=(wt-8), h=(ht-8))
		cmds.tabLayout(zoobeRenameTab, edit=True, h=(ht))
		
def zoobeWinTest():	
	
	#global variables
	global ht
	global wt
	global tlc
	global zoobeWinTestUI
	global mainCL
	global zoobeRenameTab
	global multiScene
	global searchStringField
	global replaceStringField
	
	if(cmds.window("zoobeWinTestUI", exists=True)):
		cmds.deleteUI("zoobeWinTestUI")
		print('blah')
	if(cmds.windowPref ("zoobeWinTestUI", exists=True)):
		cmds.windowPref("zoobeWinTestUI", edit=True, widthHeight=((wt-300), (ht-225)), topLeftCorner=(tlc, tlc) )
		print('silly')
	
	zoobeWinTestUI = cmds.window(width=(wt-300),  height=(ht-225), topLeftCorner=(tlc, tlc), title='Zoobe Test Win UI 1.0', sizeable=False)
	mainCL = cmds.columnLayout(width=(wt-300), height=(ht-230))
	zoobeRenameTab = cmds.tabLayout(height=(ht-230), tabsVisible=True, enableBackground=True, sc='rtPrintSomething3.zoobe_RenameChangeTab()')
	singleScene = cmds.columnLayout(width=(wt-308), height=(ht-230))		
	singleForm = cmds.formLayout(numberOfDivisions=100)
	searchStringField = cmds.textFieldGrp(cw=((1, 70),(2, 160)), l='Search String', tx='', w=(wt-20))
	replaceStringField = cmds.textFieldGrp(cw=((1, 70),(2, 160)), l='Replcae String', tx='', w=(wt-20))
	executeReplaceBtn = cmds.button(w=(wt-395), c=('rtPrintSomething3.zoobe_doRename(0)'), l='Search and Replace')
	
	#Editing the Single Scene Form Layout
	cmds.formLayout(singleForm, edit=True, 
	af=[
	(searchStringField, 'left', 5), 
	(searchStringField, 'top', 10), 
	
	(replaceStringField, 'left', 5), 
	(replaceStringField, 'top', 35), 
	
	(executeReplaceBtn, 'left', 80), 
	(executeReplaceBtn, 'top', 65)])
	
	#Parenting back to the Tab Layout
	cmds.setParent(zoobeRenameTab)
	
	#Creating the Multi Scene Tab Contents
	multiScene = cmds.columnLayout(width=(wt-308), height=(ht-5))
	multiForm = cmds.formLayout(numberOfDivisions=100)
	browseFolderField = cmds.textFieldButtonGrp(cw=((1, 70), (2, 395), (3, 75)), ed=0, bl='browse...', bc='rtPrintSomething3.zoobe_GetScenesPath()', l='Scenes Folder', tx='', w=(wt-20) )
	scenesInFolderList = cmds.textScrollList(numberOfRows=8, allowMultiSelection=True, w=(wt-100), h=(ht-125))
	searchMultiStringField = cmds.textFieldGrp(cw=((1, 70), (2, 180)), l='Search String', tx='', w=(wt-20)) 
	replaceMultiStringField = cmds.textFieldGrp(cw=((1, 70), (2, 180)), l='Replcae String', tx='', w=(wt-20))
	executeMultiReplaceBtn = cmds.button(w=(wt-395), c='', l='Search and Replace')
	
	#Editing the Multi Scene Form Layout
	cmds.formLayout(multiForm, edit=True, 		
	af=[
	(browseFolderField, 'left', 5), 
	(browseFolderField, 'top', 10), 
	
	(scenesInFolderList, 'left', 40), 
	(scenesInFolderList, 'top', 40), 
	
	(searchMultiStringField, 'left', 5), 
	(searchMultiStringField, 'top', 270),
	
	(replaceMultiStringField, 'left', 270), 
	(replaceMultiStringField, 'top', 270),
	
	(executeMultiReplaceBtn, 'left', 380), 
	(executeMultiReplaceBtn, 'top', 295)])

	#Parenting Back to the Main Column Layout
	cmds.setParent(mainCL)

	#Editing the labels of the Tab Layout
	cmds.tabLayout(zoobeRenameTab, edit=True, tabLabel=((singleScene, 'Single Scene'), (multiScene, 'Multi Scene') ))
	
	#cmds.tabLayout(zoobeRenameTab, edit=True, sc='rtPrintSomething3.zoobe_RenameChangeTab()')
		
	cmds.showWindow(zoobeWinTestUI)	

def zoobe_doRename(mode):
	global searchStringField
	global replaceStringField

	cmds.select(all=True)
	objs = cmds.ls(selection=True, long=True)
	objCnt = len(objs)
	#print(objCnt)

	i=''

	search = cmds.textFieldGrp(searchStringField, q=True, tx=True)
	replace = cmds.textFieldGrp(replaceStringField, q=True, tx=True)
	
	shortName = ''
	newName = ''
	newShortName = ''
	
	for i in range(0, objCnt, 1):
		obj = objs[i]
		shortName = rtPrintSomething3.zoobe_getShortName(obj)
	'''
		switch(mode):
			case 0:
				if (search == ''):
					cmds.warning(sl=False, ("Can't search and replace, search entry field is blank!"))
					return
				newShortName = zoobe_stringReplace(shortName, search, replace)
				break
		
		newName = cmds.rename(obj, newShortName)
		
		cmds.select(r=True, newName)
		newLongNames = cmds.ls(sl=True, long=True)
		newLongName = newLongNames[0]
		
		for (j=0; j < objCnt; ++j):	    
	    tmp = objs[j]

	    tmp += '|'	# add to end for easy replacing
	    #tmp = cmds.substitute((obj+'|') tmp ('|'+newLongName+'|'))
		#tmp = (obj+'|').replace('|'+newLongName+'|')
	    #tmp = zoobe_Chop(tmp)
	    
	    #objs[j] = tmp
	    '''
	
	#cmds.select(objs)
		

def zoobe_getShortName(obj):
	ret = ''
	
	if (obj == ""):
		return ret
	#parts[]
	#cnt = cmds.tokenize(obj, "|", parts)
	cnt = obj.split()
	parts = obj.split('|')
	
	if (cnt <= 0):
		ret = obj
	else:
		print(cnt)
		print('\n')
		print(parts)
		#newCnt = (len(cnt)-1)
		#print(newCnt)
		#ret = parts(newCnt)
	return ret
	

def zoobe_Chop(str):

    ret = ''

    cnt = len(str)
    
    if (cnt <= 1):
        return ret
    
    ret = str.substring(1, (cnt-1))

    return ret

	
	
	


