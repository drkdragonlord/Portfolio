import maya.cmds as zCmds
import maya.mel as zMel
import os
import sys
ht = 350
wt = 550
tlc = 150
zoobeRenameWin = zCmds.window

zoobeRenameRigPrefix.zoobe_RenameRigPrefix()()
	
def zoobe_RenameRigPrefix():
{
	global ht
	global wt
	global tlc
	global zoobeRenameWin
	
	if(zCmds.window(zoobeRenameWin, exists=True)):
		zCmds.deleteUI(zoobeRenameWin)
	if(zCmds.windowPref (zoobeRenameWin, exists=True)):
		zCmds.windowPref(zoobeRenameWin, edit=True, widthHeight=(wt-300) (ht-225), topLeftCorner=tlc tlc )
		
	zoobeRenameWin = zCmds.window(width=(wt-300) height=(ht-225) title="Zoobe Rename 1.0" )
	mainCL = zCmds.columnLayout(width=(wt-300), height=(ht-225))
	zoobeRenameTab= zCmds.tabLayout(tv=1 ebg=1 ''' -bgc $red $green $blue ''' sc="zoobe_RenameChangeTab()")
		#		columnLayout -w (wt-308) -h (ht-230) SingleScene;
		#			formLayout -nd 100 singleForm;
		#				textFieldGrp -cw 1 70 -cw 2 160 -l "Search String" -tx "" -w (wt-20) searchStringField;
		#				textFieldGrp -cw 1 70 -cw 2 160 -l "Replcae String" -tx "" -w (wt-20) replaceStringField;
		#				button -w (wt-395) -c ("zoobe_doRename(0);") -l "Search and Replace" executeReplaceBtn;
		#			formLayout -e 
		#				
		#				-af searchStringField "left" 5
		#				-af searchStringField "top" 10
		#				
		#				-af replaceStringField "left" 5
		#				-af replaceStringField "top" 35
		#				
		#				-af executeReplaceBtn "left" 80
		#				-af executeReplaceBtn "top" 65
		#			singleForm;
		#			setParent..;
		#		setParent..;
		#		columnLayout -w (wt-308) -h (ht-5) MultiScene;
		#			formLayout -nd 100 multipleForm;
		#				textFieldButtonGrp -cw 1 70 -cw 2 395 -cw 3 75 -ed 0 -bl "browse..." -bc "zoobe_GetScenesPath()" -l "Scenes Folder" -tx "" -w (wt-20) browseFolderField;
		#				textScrollList -numberOfRows 8 -allowMultiSelection true -w (wt-100) -h (ht-125)scenesInFolderList;
		#				textFieldGrp -cw 1 70 -cw 2 180 -l "Search String" -tx "" -w (wt-20) searchMultiStringField;
		#				textFieldGrp -cw 1 70 -cw 2 180 -l "Replcae String" -tx "" -w (wt-20) replaceMultiStringField;
		#				button -w (wt-395) -c "" -l "Search and Replace" executeMultiReplaceBtn;
		#			formLayout -e 
		#			
		#				-af browseFolderField "left" 5
		#				-af browseFolderField "top" 10		
		#				
		#				-af scenesInFolderList "left" 40
		#				-af scenesInFolderList "top" 40
		#				
		#				-af searchMultiStringField "left" 5
		#				-af searchMultiStringField "top" 270
		#				
		#				-af replaceMultiStringField "left" 270
		#				-af replaceMultiStringField "top" 270
		#				
		#				-af executeMultiReplaceBtn "left" 380
		#				-af executeMultiReplaceBtn "top" 295			
		#			multipleForm;
		#			setParent..;
		#		setParent..;
		#	setParent..;
		#setParent..;
		
	zCmds.showWindow(zoobeRenameWin)