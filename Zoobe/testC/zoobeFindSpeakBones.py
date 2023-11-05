import sys
import os
import maya.cmds as cmds
import maya.mel as mel

globalScriptPath = "C:/testC/"

def zFindSpeakBonesUI():
	
	global globalScriptPath
	
	speakBonesList = ['upper_lip_center_speak', 'lower_lip_center_speak', 'lower_jaw_speak', 'upper_lip_left_speak', 'upper_lip_right_speak', 'lip_corner_left_speak', 'lip_corner_right_speak', 'lower_lip_left_speak', 'lower_lip_right_speak']
	
	cmds.select(all=True)
	sceneObjs = cmds.ls(selection=True)
	foundObjsList = []
	
	for obj in sceneObjs:
		objLen = len(obj)
		for speakBone in speakBonesList:
			if(obj[:objLen] == speakBone):
				print(obj+' found')
				foundObjsList += [str(obj)]
			else:
				#print('blank')
				break
	
	print(foundObjsList)
	
def zFindSpeakBonesNS(search):
	
	global globalScriptPath
	replace = ''	
	export = 'export_'
	
	speakBonesList = ['upper_lip_center_speak', 'lower_lip_center_speak', 'lower_jaw_speak', 'upper_lip_left_speak', 'upper_lip_right_speak', 'lip_corner_left_speak', 'lip_corner_right_speak', 'lower_lip_left_speak', 'lower_lip_right_speak']
	
	cmds.select(all=True, hierarchy=True)
	sceneObjs = cmds.ls(selection=True, type='joint')
	strLen = len(search)
	newObj = ''
	newObj_1 = ''
	newObjList = []
	expLen = len(export)
	foundObjsList = []
	
	found = 3
	x = 0
	#getting rid of additional strings in the begining due to namespace corrections within Maya
	for obj in sceneObjs:
		if(obj[0:strLen] == search):
			#print(obj)
			obj = obj[strLen:]
			newObj = obj
			#print(newObj)
			if(newObj[0:expLen] == export):
				newObj = newObj[expLen:]
				newObj = newObj
			objLen = len(newObj)
			for speakBone in speakBonesList:
				if(newObj[:objLen] == speakBone):
					#print(newObj+' found')
					foundObjsList += [str(newObj)]
					if(len(foundObjsList) == len(speakBonesList)):
						print 'Found: ' 
						print '\n\nFound: \n'.join(foundObjsList)
						zoobeFindSpeakBones.zDoExport()
						#cmds.select(foundObjsList, r=True)
						break
					continue				
				else:
					#print('blank')
					continue
	#print(foundObjsList)
	
	#print(foundObjsList)
			'''
			if(newObj[0:expLen] == export):
				newObj = newObj[expLen:]
				newObj_1 = newObj
				newObjList += newObj_1
				print(newObjList)
			else:
				newObjList += newObj
				print(newObjList)
			return(newObjList)
			#cmds.rename(obj, obj[14:])
			#print(newObj)
			'''
		#continue
	
	
	'''
	for obj in newObjList:
		objLen = len(obj)
		for speakBone in speakBonesList:
			if(obj[:objLen] == speakBone):
				print(obj+' found')
				foundObjsList += [str(obj)]
			else:
				#print('blank')
				break
	
	print(foundObjsList)
	'''
'''
jbSourceScript (globalScriptPath+'zoobeFindSpeakBones.py')

zoobeFindSpeakBones.zFindSpeakBonesUI()	
'''
def zDoExport():
	
	print ('Performing Export!')