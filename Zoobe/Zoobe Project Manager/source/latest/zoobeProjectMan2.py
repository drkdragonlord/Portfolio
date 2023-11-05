'''                                                                                                      #
#--------------------------------------------------------------------------------------------------------#
#|This is the Zoobe Project Manager Tool                                                                |#
#|Tool version: 1.0                                                                                     |#
#|Tool Programmer(s): Juan Borrero                                                                      |#
#|Latest Tool Update: September 26, 2013                                                                |#
#|                                                                                                      |#
#|Install Instructions:                                                                                 |#
#|Coming Soon!                                                                                          |#
#|                                                                                                      |#
#|Usage:                                                                                                |#
#|The Zoobe Project Manager tool is designed to manage all maya projects assets and their               |#
#|respective operations. These include, but are not limited to: File referencing, Setting projects,     |#
#|Creating new projects, Editing existing projects, Setting project deadlines,                          |#
#|File Naming Conventions, Ease of access to Maya tools, Ease of Access to Zoobe tools                  |#
#|                                                                                                      |#
#--------------------------------------------------------------------------------------------------------#
'''
#Import Statements
import sys
import os
import shutil
from xml.dom.minidom import Document, parse, parseString, Element
import xml.dom.minidom as md
import maya.cmds as cmds
import maya.mel as mel

#Global Variables
ht=650
wt=400
tlc=150
user = mel.eval('getenv USER')
nasPath = "P:/"
tempScriptPath = "C:/Users/Juan/Dropbox/zoobe/src/python/zoobeProjectMan2.py"
tempProjXMLPath = "C:/Users/Juan/Dropbox/zoobe/src/test/"
tempXMLFileName = "test.xml"
mswindows = (sys.platform == "win32")

'''
#This is the module sourcing script, which may be used if necessary

def zoobeSourceModule(module):
 
    file = os.path.basename( module )
    dir = os.path.dirname( module )
 
    toks = file.split( '.' )
    modname = toks[0]
 
    # Check if dirrectory is really a directory
    if( os.path.exists( dir ) ):
 
    # Check if the file directory already exists in the sys.path array
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
 
    # If the dirrectory is not part of sys.path add it
        if not pathfound:
            sys.path.append( dir )
 
    # exec works like MEL's eval but you need to add in globals() 
    # at the end to make sure the file is imported into the global 
    # namespace else it will only be in the scope of this function
    exec ('import ' + modname) in globals()
 
    # reload the file to make sure its up to date
    exec( 'reload( ' + modname + ' )' ) in globals()
 
    # This returns the namespace of the file imported
    return modname

zoobeSourceModule(tempScriptPath)

zoobeProjectMan2.zoobePManInit()
'''

def zoobeRemoveDirPrompt(selList):
    print(selList)
    global tlc
    selection = cmds.textScrollList(selList,query=True, selectItem=True)
    
    if(cmds.window('zoobeRemoveDirWin', exists=True)):
        cmds.deleteUI('zoobeRemoveDirWin')
    if(cmds.windowPref('zoobeRemoveDirWin', exists=True)):
        cmds.windowPref('zoobeRemoveDirWin', edit=True, width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)))
    
    zoobeRemoveDirWin = cmds.window('zoobeRemoveDirWin', width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)), sizeable = False, title="Remove Directory")
    
    removeDirForm = cmds.formLayout('removeDirForm', numberOfDivisions=100)
    
    removeDirNameLabel = cmds.text('removeDirNameLabel', label=('Are you sure you want to completely remove the directory\n "'+ selection[0] +'" from the project structure'))
    removeDirConfrim = cmds.button('removeDirConfrim', width=125, label='Delete')
    if(selList == ('assetTypesList')):
        cmds.button('removeDirConfrim', edit=True, command=("zoobeProjectMan2.zoobeRemoveDir('assetTypesList')"))
    elif(selList == ('assetSelList')):
        cmds.button('removeDirConfrim', edit=True, command=("zoobeProjectMan2.zoobeRemoveDir('assetSelList')"))
    elif(selList == ('assetComponentsSelList')):
        cmds.button('removeDirConfrim', edit=True, command=("zoobeProjectMan2.zoobeRemoveDir('assetComponentsSelList')"))
    removeDirCancel = cmds.button('removeDirCancel', width=125, label='Cancel', command="cmds.deleteUI('zoobeRemoveDirWin')")
    
    cmds.formLayout(removeDirForm, edit=True,
    af=[
    
    (removeDirNameLabel, 'left', 10), 
    (removeDirNameLabel, 'top', 5),

    (removeDirConfrim, 'left', 15), 
    (removeDirConfrim, 'top', 65),
    
    (removeDirCancel, 'left', 160), 
    (removeDirCancel, 'top', 65),
    
    ])    
    cmds.showWindow(zoobeRemoveDirWin)        
def zoobeRemoveDir(listName):
    print(listName) 
    mainPath = cmds.textField('pManProjectPathField', query=True, text=True)
    #typeFolder = cmds.textScrollList('assetTypesList',query=True, selectItem=True)
    #assetFolder = cmds.textScrollList('assetSelList',query=True, selectItem=True)
    #compFolder = cmds.textScrollList('assetComponentsSelList',query=True, selectItem=True)
    '''
    if(listName == 'assetComponentsSelList'):
        typeFolder = cmds.textScrollList('assetTypesList',query=True, selectItem=True)
        assetFolder = cmds.textScrollList('assetSelList', query=True, selectItem=True)
        compFolder = cmds.textScrollList(listName,query=True, selectItem=True)
    elif(listName == 'assetSelList'):
        typeFolder = cmds.textScrollList('assetTypesList',query=True, selectItem=True)
        assetFolder = cmds.textScrollList(listName, query=True, selectItem=True)
        #zoobeGetListSelection(selection[0], listName, childList)
    '''
    if(listName == ('assetTypesList')):
        typeFolder = cmds.textScrollList(listName, query=True, selectItem=True)
        remPath = (mainPath+'working_project/'+typeFolder[0]).replace('/', '\\')
        print(remPath)
        cmds.sysFile(remPath, removeEmptyDir=True)
        #os.rmdir(remPath)
        #shutil.rmtree(remPath)
        zoobeGetMainFoldersList(mainPath+'working_project')        
        if(cmds.window('zoobeRemoveDirWin', exists=True)):
            cmds.deleteUI('zoobeRemoveDirWin')
def zoobeNewAssetPrompt():
    global tlc
    
    if(cmds.window('zoobeNewAssetWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetWin')
    if(cmds.windowPref('zoobeNewAssetWin', exists=True)):
        cmds.windowPref('zoobeNewAssetWin', edit=True, width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)))
        
    zoobeNewAssetWin = cmds.window('zoobeNewAssetWin', width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)), sizeable = False, title="New Asset")
    
    newAssetForm = cmds.formLayout('newAssetForm', numberOfDivisions=100)
    newAssetNameLabel = cmds.text('newAssetNameLabel', label='New Asset: \n(Do not add special characters or spaces, use "_" instead)')
    newAssetNameField = cmds.textField('newAssetNameField', text='', width=275, editable=True)
    newAssetConfrim = cmds.button('newAssetConfrim', width=125, label='Create', command="zoobeProjectMan2.zoobeCreateNewAsset()")
    newAssetCancel = cmds.button('newAssetCancel', width=125, label='Cancel', command="cmds.deleteUI('zoobeNewAssetWin')")
    
    cmds.formLayout(newAssetForm, edit=True,
    af=[
    
    (newAssetNameLabel, 'left', 10), 
    (newAssetNameLabel, 'top', 5),
    
    (newAssetNameField, 'left', 13), 
    (newAssetNameField, 'top', 35),

    (newAssetConfrim, 'left', 15), 
    (newAssetConfrim, 'top', 65),
    
    (newAssetCancel, 'left', 160), 
    (newAssetCancel, 'top', 65),
    
    ])    
    
    cmds.showWindow(zoobeNewAssetWin)
def zoobeCreateNewAsset():
    name = cmds.textField('newAssetNameField', query=True, text=True)
    parentName = cmds.textScrollList('assetTypesList', query=True, selectItem=True)
    mainPath = (cmds.textField('pManProjectPathField', query=True, text=True)+'working_project/')
    if(name!=''):
        if((len(name))<3):
            cmds.error('length of the new asset is less than 3 characters')
        else:
            cmds.sysFile( (mainPath+parentName[0]+'/'+name), makeDir=True )
            zoobeGetListSelection('assetTypesList','assetSelList')
            if(cmds.window('zoobeNewAssetWin', exists=True)):
                cmds.deleteUI('zoobeNewAssetWin')            
def zoobeQuerryNewComponentOptions():
    name = cmds.textField('newAssetNameField', query=True, text=True)
    mode = cmds.radioCollection('newAssetOptions', query=True, select=True)
    mainPath = (cmds.textField('pManProjectPathField', query=True, text=True)+'working_project/')
    typeFolder = cmds.textScrollList('assetTypesList',query=True, selectItem=True)
    assetFolder = cmds.textScrollList('assetSelList',query=True, selectItem=True)
    path = (mainPath+typeFolder[0]+'/'+assetFolder[0]+'/')
    zoobeCreateNewComponent(name, mode, path)   
def zoobeCreateNewAssetTyp():
    name = cmds.textField('newAssetTypNameField', query=True, text=True)
    mainPath = (cmds.textField('pManProjectPathField', query=True, text=True)+'working_project/')
    if(name!=''):
        if((len(name))<3):
            cmds.error('length of the new asset type is less than 3 characters')
        else:
            cmds.sysFile( (mainPath+name), makeDir=True )
            dirPath = cmds.textField('pManProjectPathField', query=True, text=True)
            zoobeGetMainFoldersList(dirPath+'working_project')
            if(cmds.window('zoobeNewAssetTypWin', exists=True)):
                cmds.deleteUI('zoobeNewAssetTypWin')            
def zoobeNewAssetTypPrompt():
    global tlc
    
    if(cmds.window('zoobeNewAssetTypWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetTypWin')
    if(cmds.windowPref('zoobeNewAssetTypWin', exists=True)):
        cmds.windowPref('zoobeNewAssetTypWin', edit=True, width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)))
        
    zoobeNewAssetTypWin = cmds.window('zoobeNewAssetTypWin', width=300, height=95, topLeftCorner=((tlc+50), (tlc+100)), sizeable = False, title="New Asset Type")
    
    newAssetTypForm = cmds.formLayout('newAssetTypForm', numberOfDivisions=100)
    newAssetTypNameLabel = cmds.text('newAssetTypNameLabel', label='New Asset Type: \n(Do not add special characters or spaces, use "_" instead)')
    newAssetTypNameField = cmds.textField('newAssetTypNameField', text='', width=275, editable=True)
    newAssetTypConfrim = cmds.button('newAssetTypConfrim', width=125, label='Create', command="zoobeProjectMan2.zoobeCreateNewAssetTyp()")
    newAssetTypCancel = cmds.button('newAssetTypCancel', width=125, label='Cancel', command="cmds.deleteUI('zoobeNewAssetTypWin')")
    newAssetTypColumn = cmds.columnLayout('newAssetTypColumn', width=300, height=65)
    
    cmds.formLayout(newAssetTypForm, edit=True,
    af=[
    
    (newAssetTypNameLabel, 'left', 10), 
    (newAssetTypNameLabel, 'top', 5),
    
    (newAssetTypNameField, 'left', 13), 
    (newAssetTypNameField, 'top', 35),

    (newAssetTypConfrim, 'left', 15), 
    (newAssetTypConfrim, 'top', 65),
    
    (newAssetTypCancel, 'left', 160), 
    (newAssetTypCancel, 'top', 65),
    
    ])    
    
    cmds.showWindow(zoobeNewAssetTypWin)
def zoobeReadComponentXML(mainPath, dirList, parentList, listName):
    global user
    masterNames = zoobeMasterNames()
    
    mainPath = (cmds.textField(mainPath, query=True, text=True)+'working_project/') 
    assetTypSelList = cmds.textScrollList(dirList,query=True, selectItem=True)
    assetsSelList = cmds.textScrollList(parentList, query=True, selectItem=True)
    compSelList = cmds.textScrollList(listName, query=True, selectItem=True)
    compXMLPath = (mainPath+assetTypSelList[0]+'/'+assetsSelList[0]+'/'+compSelList[0]+'/')

    for userNames in masterNames:
        if(userNames == user):
            cmds.button('assetComponentsDelBtn', edit=True, enable=True)
        else:
            cmds.button('assetComponentsDelBtn', edit=True, enable=False)
    #print(compXMLPath)
    os.chdir(compXMLPath)
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            selFile = parse(compXMLPath+compSelList[0]+'.xml')
            selFileData = selFile.getElementsByTagName("file")
            dataList = []
            for newData in selFileData:
                fileData = newData.getElementsByTagName("name")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("path")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("version")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("creationdate")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("time")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("creator")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("event")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
                fileData = newData.getElementsByTagName("comment")[0]
                existingData = "%s" % zoobeGetText(fileData.childNodes)
                dataList.append(str(existingData))
            print(len(dataList))
            x=0
            cmds.scrollField('assetHistoryScroll', edit=True, clear=True)
            for dataItem in dataList:
                if(x<=(len(dataList))):
                    if(x==0):
                        cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Name: ' + dataItem+'\n'), insertionPosition=0)
                    if((x==8)or(x==16)or(x==24)or(x==32)or(x==40)or(x==48)or(x==56)or(x==64)or(x==72)or(x==80)or(x==88)or(x==96)or(x==104)or(x==112)or(x==120)or(x==128)or(x==136)or(x==144)or(x==152)or(x==160)or(x==168)or(x==176)or(x==184)or(x==192)or(x==200)or(x==208)or(x==216)or(x==224)or(x==232)or(x==240)or(x==248)or(x==256)or(x==264)or(x==272)or(x==280)or(x==288)or(x==296)or(x==304)or(x==312)or(x==320)):
                        cmds.scrollField('assetHistoryScroll', edit=True, insertText=('\nName: ' + dataItem+'\n'), insertionPosition=0)
                    if(x%8):
                        if((x==1)or(x==9)or(x==17)or(x==25)or(x==33)or(x==41)or(x==49)or(x==57)or(x==65)or(x==73)or(x==81)or(x==89)or(x==97)or(x==105)or(x==113)or(x==121)or(x==129)or(x==137)or(x==145)or(x==153)or(x==161)or(x==169)or(x==177)or(x==185)or(x==193)or(x==201)or(x==209)or(x==217)or(x==225)or(x==233)or(x==241)or(x==249)or(x==257)or(x==265)or(x==273)or(x==281)or(x==289)or(x==297)or(x==305)or(x==313)or(x==321)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('File Path: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==2)or(x==10)or(x==18)or(x==26)or(x==34)or(x==42)or(x==50)or(x==58)or(x==66)or(x==74)or(x==82)or(x==90)or(x==98)or(x==106)or(x==114)or(x==122)or(x==130)or(x==138)or(x==146)or(x==154)or(x==162)or(x==170)or(x==178)or(x==186)or(x==194)or(x==202)or(x==210)or(x==218)or(x==226)or(x==234)or(x==242)or(x==250)or(x==258)or(x==266)or(x==274)or(x==282)or(x==290)or(x==298)or(x==306)or(x==314)or(x==322)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Version: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==3)or(x==11)or(x==19)or(x==27)or(x==35)or(x==43)or(x==51)or(x==59)or(x==67)or(x==75)or(x==83)or(x==91)or(x==99)or(x==107)or(x==115)or(x==123)or(x==131)or(x==139)or(x==147)or(x==155)or(x==163)or(x==171)or(x==179)or(x==187)or(x==195)or(x==203)or(x==211)or(x==219)or(x==227)or(x==235)or(x==243)or(x==251)or(x==259)or(x==267)or(x==275)or(x==283)or(x==291)or(x==299)or(x==307)or(x==315)or(x==323)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Date: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==4)or(x==12)or(x==20)or(x==28)or(x==36)or(x==44)or(x==52)or(x==60)or(x==68)or(x==76)or(x==84)or(x==92)or(x==100)or(x==108)or(x==116)or(x==124)or(x==132)or(x==140)or(x==148)or(x==156)or(x==164)or(x==172)or(x==180)or(x==188)or(x==196)or(x==204)or(x==212)or(x==220)or(x==228)or(x==236)or(x==244)or(x==252)or(x==260)or(x==268)or(x==276)or(x==284)or(x==292)or(x==300)or(x==308)or(x==316)or(x==324)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Time: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==5)or(x==13)or(x==21)or(x==29)or(x==37)or(x==45)or(x==53)or(x==61)or(x==69)or(x==77)or(x==85)or(x==93)or(x==101)or(x==109)or(x==117)or(x==125)or(x==133)or(x==141)or(x==149)or(x==157)or(x==165)or(x==173)or(x==181)or(x==189)or(x==197)or(x==205)or(x==213)or(x==221)or(x==229)or(x==237)or(x==245)or(x==253)or(x==261)or(x==269)or(x==277)or(x==285)or(x==293)or(x==301)or(x==309)or(x==317)or(x==325)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Creator: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==6)or(x==14)or(x==22)or(x==30)or(x==38)or(x==46)or(x==54)or(x==62)or(x==70)or(x==78)or(x==86)or(x==94)or(x==102)or(x==110)or(x==118)or(x==126)or(x==134)or(x==142)or(x==150)or(x==158)or(x==166)or(x==174)or(x==182)or(x==190)or(x==198)or(x==206)or(x==214)or(x==222)or(x==230)or(x==238)or(x==246)or(x==254)or(x==262)or(x==270)or(x==278)or(x==286)or(x==294)or(x==302)or(x==310)or(x==318)or(x==326)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Event: ' + dataItem+'\n'), insertionPosition=0)
                        if((x==7)or(x==15)or(x==23)or(x==31)or(x==39)or(x==47)or(x==55)or(x==63)or(x==71)or(x==79)or(x==87)or(x==95)or(x==103)or(x==111)or(x==119)or(x==127)or(x==135)or(x==143)or(x==151)or(x==159)or(x==160)or(x==175)or(x==183)or(x==191)or(x==199)or(x==207)or(x==215)or(x==223)or(x==231)or(x==239)or(x==247)or(x==255)or(x==263)or(x==271)or(x==279)or(x==287)or(x==295)or(x==303)or(x==311)or(x==319)or(x==327)):
                            cmds.scrollField('assetHistoryScroll', edit=True, insertText=('Comment: ' + dataItem+'\n'), insertionPosition=0)
                x+=1
            #Break out of loop if file is found
            break
def zoobeCreateNewComponent(name, mode, path):
    global tempProjXMLPath 
    global tempXMLFileName

    listNames = cmds.textScrollList('assetComponentsSelList', query=True, allItems=True)
    if(listNames != True):
        print('')
    else:
        for item in listNames:
            if (name == item):
                cmds.error('item "' + name +'" already exists')
    #Queries and raised errors
    if(len(name)<3):
        cmds.error("New Asset name has to be longer than 2 characters")
    if(mode == 'NONE'):
        cmds.error("Must select an option")
    elif(mode == 'newAssetOption01'):
        mode = 1
    elif(mode == 'newAssetOption02'):
        mode = 2
    elif(mode == 'newAssetOption03'):
        mode = 3
    cmds.sysFile( (path+name), makeDir=True )#mainAssetFolder
    cmds.sysFile((path+name+'/workshops'), makeDir=True )
    cmds.sysFile((path+name+'/notes'), makeDir=True )
    cmds.sysFile((path+name+'/data'), makeDir=True )
    
    currentProject = cmds.optionMenu('pManProject', query=True, value=True)
    #get the default extension for the current project
    doc = parse(tempProjXMLPath+tempXMLFileName)
    fileFormat = []
    projects = doc.getElementsByTagName("project")
    for project in projects:
        nameXMLTag = project.getElementsByTagName("name")[0]
        existingProj = "%s" % zoobeGetText(nameXMLTag.childNodes)
        if((str(existingProj))== currentProject):
            wFormatXMLTag = project.getElementsByTagName("workshopformat")[0]
            existingFormat = "%s" % zoobeGetText(wFormatXMLTag.childNodes)
            fileFormat.append(str(existingFormat))
    format = fileFormat[0]
    
    if(mode == 1):#Make a new scene Component
        if(format == 'mb'):
            cmds.file( force=True, newFile=True,) 
            cmds.file( rename=(path+name+'/workshops/'+name+'_0001.'+format) )
            cmds.file( save=True, type='mayaBinary' )
        elif(format == 'ma'):
            cmds.file( force=True, newFile=True,)
            cmds.file( rename=(path+name+'/workshops/'+name+'_0001.'+format) )
            cmds.file( save=True, type='mayaAscii' )
    if(mode == 2):#Make a Component using the selected items
        if(format == 'mb'):
            cmds.file( (path+name+'/workshops/'+name+'_0001.'+format), force=True, exportSelected=True, preserveReferences=True, type="mayaBinary",)
        elif(format == 'ma'):
            cmds.file( (path+name+'/workshops/'+name+'_0001.'+format), force=True, exportSelected=True, preserveReferences=True, type="mayaAscii",)
    if(mode == 3):#Make a Component using all the contents of the current scene
        if(format == 'mb'):
            cmds.file( (path+name+'/workshops/'+name+'_0001.'+format), force=True, exportAll=True, preserveReferences=True, type="mayaBinary",)
        elif(format == 'ma'):
            cmds.file( (path+name+'/workshops/'+name+'_0001.'+format), force=True, exportAll=True, preserveReferences=True, type="mayaAscii",)
    cmds.textScrollList('assetComponentsSelList',edit=True, append=name)
    zoobeMakeNewComponentData(name+'_0001.'+format, path+name+'/' )
    if(cmds.window('zoobeNewAssetWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetWin')
def zoobeMakeNewComponentData(assetName, path):
    global user
    #print assetName
    #print (assetName[0:-8])
    #print path
    curDate = cmds.date( format='DD/MM/YYYY' )
    curTime = cmds.date( time=True )
    curUser = user
    version = assetName[-7:-3]
    
    doc = Document()
	
    root_node = doc.createElement("filedata")
    doc.appendChild(root_node)
	
    
    aAttrs = ['name','path','version','creationdate','time','creator','event', 'comment']
    a_node = doc.createElement("file")
    root_node.appendChild(a_node)
    for attr in aAttrs:
        attr_node= doc.createElement(str(attr))
        a_node.appendChild(attr_node)
        if(attr=='name'):
            newtext=doc.createTextNode(assetName);
            attr_node.appendChild(newtext)
        if(attr=='path'):
            newtext=doc.createTextNode(path);
            attr_node.appendChild(newtext)
        if(attr=='version'):
            newtext=doc.createTextNode(version);
            attr_node.appendChild(newtext)
        if(attr=='creationdate'):
            newtext=doc.createTextNode(curDate);
            attr_node.appendChild(newtext)
        if(attr=='time'):
            newtext=doc.createTextNode(curTime);
            attr_node.appendChild(newtext)
        if(attr=='creator'):
            newtext=doc.createTextNode(curUser);
            attr_node.appendChild(newtext)
        if(attr=='event'):
            newtext=doc.createTextNode('created');
            attr_node.appendChild(newtext)
        if(attr=='comment'):
            newtext=doc.createTextNode('initial file');
            attr_node.appendChild(newtext)        
    xml_file = open(path+assetName[0:-8]+'.xml', "w")#WORK
    #xml_file = open("C:\\Users\\Dark Dragonlord\\Dropbox\\zoobe\\src\\test\\test.xml", "w")#HOME
    xml_file.write(doc.toxml(encoding='utf-8'))
    #toprettyxml(doc, 'utf-8')
    xml_file.close()
    zoobeCleanXML(path+(assetName[0:-8])+'.xml')
def zoobeNewComponentPrompt():
    global tlc
    
    if(cmds.window('zoobeNewCompWin', exists=True)):
        cmds.deleteUI('zoobeNewCompWin')
    if(cmds.windowPref('zoobeNewCompWin', exists=True)):
        cmds.windowPref('zoobeNewCompWin', edit=True, width=300, height=168, topLeftCorner=((tlc+50), (tlc+100)))
        
    zoobeNewCompWin = cmds.window('zoobeNewCompWin', width=300, height=168, topLeftCorner=((tlc+50), (tlc+100)), sizeable = False, title="New Asset")
    
    newAssetForm = cmds.formLayout('newAssetForm', numberOfDivisions=100)
    newAssetNameLabel = cmds.text('newAssetNameLabel', label='New Component Name: \n(Do not add special characters or spaces, use "_" instead)')
    newAssetNameField = cmds.textField('newAssetNameField', text='', width=275, editable=True)
    newAssetDivider = cmds.separator('newAssetDivider', width=300, height=40, style='in' )
    newAssetOptionsLabel = cmds.text('newAssetOptionsLabel', label='Options', font='boldLabelFont')
    newAssetConfrim = cmds.button('newAssetConfrim', width=125, label='Create', command="zoobeProjectMan2.zoobeQuerryNewComponentOptions()")
    newAssetCancel = cmds.button('newAssetCancel', width=125, label='Cancel', command="cmds.deleteUI('zoobeNewCompWin')")
    newAssetColumn = cmds.columnLayout('newAssetColumn', width=300, height=65)
    newAssetOptions = cmds.radioCollection('newAssetOptions')
    newAssetOption01 = cmds.radioButton('newAssetOption01', label='Create an Empty Scene as New Component' )
    newAssetOption02 = cmds.radioButton('newAssetOption02', label='Export Selected Item(s) as New Component' )
    newAssetOption03 = cmds.radioButton('newAssetOption03', label='Export Current Scene as New Component' )
    cmds.setParent(newAssetForm)
    
    cmds.formLayout(newAssetForm, edit=True,
    af=[
    
    (newAssetNameLabel, 'left', 10), 
    (newAssetNameLabel, 'top', 5),
    
    (newAssetNameField, 'left', 13), 
    (newAssetNameField, 'top', 35),
    
    (newAssetDivider, 'left', 0), 
    (newAssetDivider, 'top', 40),
    
    (newAssetOptionsLabel, 'left', 125), 
    (newAssetOptionsLabel, 'top', 65),
    
    (newAssetColumn, 'left', 5), 
    (newAssetColumn, 'top', 80),
    
    (newAssetConfrim, 'left', 15), 
    (newAssetConfrim, 'top', 140),
    
    (newAssetCancel, 'left', 160), 
    (newAssetCancel, 'top', 140),
    
    ])    
    
    cmds.showWindow(zoobeNewCompWin)
def zoobeReadXML(xmlPath, xmlName):
    os.chdir(xmlPath)
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            if(files == tempXMLFileName): 
                file = parse(xmlPath+xmlName)
                zoobeGetProjectNodes(file)
                #Break out of loop if file is found
                break
        else:
            print 'No XML files found. Initializing an empty Project Manager.'
            zoobeNewProjectMan()
            break
def zoobeCleanXML(file):
    f = open(file,'r')
    xml = f.read()
    f.close()

    #Removing old indendations
    raw_xml = ''        
    for line in xml:
        raw_xml += line

    xml = raw_xml

    new_xml = ''
    indent = ''
    deepness = 0

    for i in range((len(xml))):

        new_xml += xml[i]   
        if(i<len(xml)-3):

            simpleSplit = xml[i:(i+2)] == '><'
            advancSplit = xml[i:(i+3)] == '></'        
            end = xml[i:(i+2)] == '/>'    
            start = xml[i] == '<'

            if(advancSplit):
                deepness += -1
                new_xml += '\n' + indent*deepness
                simpleSplit = False
                deepness += -1
            if(simpleSplit):
                new_xml += '\n' + indent*deepness
            if(start):
                deepness += 1
            if(end):
                deepness += -1

    f = open(file,'w')
    f.write(new_xml)
    f.close()
def zoobeGetListSelection(parentList, childList):
    global user
    masterNames = zoobeMasterNames()
    if(parentList != 'assetSelList'):
        selection = cmds.textScrollList(parentList, query=True, selectItem=True)
        for userNames in masterNames:
            if(userNames == user):
                cmds.button('assetsTypesDelBtn', edit=True, enable=True)
            else:
                cmds.button('assetsTypesDelBtn', edit=True, enable=False)
        zoobeGetChildDir(selection[0], parentList, childList)
    else:
        parentSelection = cmds.textScrollList('assetTypesList',query=True, selectItem=True)
        selection = cmds.textScrollList(parentList, query=True, selectItem=True)
        for userNames in masterNames:
            if(userNames == user):
                cmds.button('assetsSelDelBtn', edit=True, enable=True)
            else:
                cmds.button('assetsSelDelBtn', edit=True, enable=False)
        zoobeGetChildDir(parentSelection[0]+'/'+selection[0], parentList, childList)    
def zoobeGetChildDir(parentDir, parentList, childList):
    mainPath = (cmds.textField('pManProjectPathField', query=True, text=True)+'working_project/')
    zoobePopulateAssetsList(mainPath+parentDir, childList)
def zoobePopulateAssetsList(path, childList):
    os.chdir(path)
    cmds.textScrollList(childList, edit=True, removeAll=True)
    if(childList != 'assetComponentsSelList'):
        for dir in os.listdir('.'):
            if(cmds.window('zoobePManWin', exists=True)):
                cmds.textScrollList(childList, edit=True, append=dir)
    else:
        for files in os.listdir('.'):
            if ((files.endswith('.mb'))or(files.endswith('.ma'))or(files.startswith('.mayaSwatches'))or(files.startswith('.'))or(files.endswith('.fbx'))or(files.endswith('.obj'))or(files.endswith('.ztl'))):
                continue
            else:
                if(cmds.window('zoobePManWin', exists=True)):
                    cmds.textScrollList(childList, edit=True, append=files)
def zoobeOpenAsset(typeList, assetList, compList):
    global tempProjXMLPath
    global tempXMLFileName
    
    mainPath = (cmds.textField('pManProjectPathField', query=True, text=True)+'working_project/')
    assetTypeSelection = cmds.textScrollList(typeList,query=True, selectItem=True)
    assetsSelection = cmds.textScrollList(assetList, query=True, selectItem=True)
    componentsSelection = cmds.textScrollList(compList, query=True, selectItem=True)
    
    currentProject = cmds.optionMenu('pManProject', query=True, value=True)
    doc = parse(tempProjXMLPath+tempXMLFileName)
    fileFormat = []
    projects = doc.getElementsByTagName("project")
    for project in projects:
        nameXMLTag = project.getElementsByTagName("name")[0]
        existingProj = "%s" % zoobeGetText(nameXMLTag.childNodes)
        if((str(existingProj))== currentProject):
            wFormatXMLTag = project.getElementsByTagName("workshopformat")[0]
            existingFormat = "%s" % zoobeGetText(wFormatXMLTag.childNodes)
            fileFormat.append(str(existingFormat))
    format = fileFormat[0]
    
    filePath = (mainPath+assetTypeSelection[0]+'/'+assetsSelection[0]+'/'+componentsSelection[0]+'/workshops/'+componentsSelection[0]+'_0001.'+format)
    cmds.file(filePath, force=True, open=True)  
    print filePath
    cmds.tabLayout('pManMainTabLO', edit=True, selectTabIndex=1)
def zoobeGetProjectNodes(xmlFile):
    projects = xmlFile.getElementsByTagName("project")
    zoobeGetProjectNames(xmlFile, projects)
def zoobeChangeProjectSelectPath():
    global tempProjXMLPath
    global tempXMLFileName

    newName = cmds.optionMenu('pManProject', query=True, value=True)
    xmlPath = tempProjXMLPath
    xmlName = tempXMLFileName
    os.chdir(xmlPath)
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            if(files == tempXMLFileName): 
                file = parse(xmlPath+xmlName)
                projects = file.getElementsByTagName("project")
                doc = file
                pathsList = []
                #Get the project text between the name tags
                for project in projects:
                    nameXMLTag = project.getElementsByTagName("name")[0]
                    existingProj = "%s" % zoobeGetText(nameXMLTag.childNodes)
                    #If the project in the list is the same as the project name in the option menu, get the path text tag, and append it to the list
                    if(str(existingProj)==newName):
                        pathXMLTag = project.getElementsByTagName("path")[0]
                        existingPath = "%s" % zoobeGetText(pathXMLTag.childNodes)
                        pathsList.append(str(existingPath))
                #Change the text in the text field        
                for path in pathsList:
                   zoobeChangeProjectPath(path)                   
                   break
                #Break out of loop if file is found
                zoobeGetMainFoldersList(path+'working_project')
                break
            else:
                continue
        else:
            break            
def zoobeGetMainFoldersList(xmlPath):
    os.chdir(xmlPath)
    cmds.textScrollList('assetTypesList', edit=True, removeAll=True)
    cmds.textScrollList('assetSelList', edit=True, removeAll=True)
    cmds.textScrollList('assetComponentsSelList', edit=True, removeAll=True)
    for dir in os.listdir('.'):
        if(dir.endswith('.mel')):
            continue
        else:
            if(cmds.window('zoobePManWin', exists=True)):
                cmds.textScrollList('assetTypesList', edit=True, append=dir)   
def zoobeGetInitialProjectPath():
    xmlPath = tempProjXMLPath
    xmlName = tempXMLFileName
    os.chdir(xmlPath)
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            if(files == tempXMLFileName): 
                file = parse(xmlPath+xmlName)
                zoobeGetProjectPathNodes(file)
                #Break out of loop if file is found
                break
            else:
                continue
        else:
            break
def zoobeGetProjectPathNodes(xmlFile):
    projects = xmlFile.getElementsByTagName("project")
    zoobeGetProjectPaths(xmlFile, projects)
def zoobeGetProjectPaths(xmlFile, projects):
    doc = xmlFile
    pathsList = []
    for project in projects:
        pathXMLTag = project.getElementsByTagName("path")[0]
        existingPath = "%s" % zoobeGetText(pathXMLTag.childNodes)
        pathsList.append(str(existingPath))
    for path in pathsList:
       zoobeChangeProjectPath(path)
       break
def zoobeChangeProjectPath(path):
    cmds.textField('pManProjectPathField', edit=True, text=path)   
def zoobeGetProjectNames(xmlFile, projects):
    doc = xmlFile
    projectsList = []
    for project in projects:
        nameXMLTag = project.getElementsByTagName("name")[0]
        existingProj = "%s" % zoobeGetText(nameXMLTag.childNodes)
        projectsList.append(str(existingProj))
    zoobeInitProjectMan(projectsList)
def zoobeGetText(nodelist):
    textArray = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            textArray.append(node.data)
    return ''.join(textArray)   
def zoobeAnimBinder():
    import tools.AnimationBinder as AB
    AB.AnimBinderUI.Show()   
def zoobePManInit():
    zoobeReadXML(tempProjXMLPath, tempXMLFileName)
def zoobeGetUser():
    global user
    #sys.stdout.write(user)
    cmds.menuItem(label=user)  
def zoobeMasterNames():
    masterNames = 'Oleg', 'Katja', 'Stephan', 'Juan'
    return(masterNames) 
def zoobeGetProjects(projects):
    for project in projects:
        cmds.menuItem(label=project)
def zoobeProjectSettings():
    global ht
    global wt
    global tlc
    
    if(cmds.window('zoobePSettingsWin', exists=True)):
        cmds.deleteUI('zoobePSettingsWin')
    if(cmds.windowPref('zoobePSettingsWin', exists=True)):
        cmds.windowPref('zoobePSettingsWin', edit=True, width=(wt+140), height=(ht-250), topLeftCorner=((tlc+100), (tlc+50)))
        
	zoobePSettingsWin = cmds.window('zoobePSettingsWin', width=(wt+140), height=(ht-250), topLeftCorner=((tlc+100), (tlc+50)), menuBar = False, sizeable = False, title="Zoobe Project Settings")
	#Project Settings Form Layout and children
    zoobeProjSettingsForm = cmds.formLayout('zoobeProjSettingsForm', numberOfDivisions=100)
    defaultProjLocLabel = cmds.text('defaultProjLocLabel', label='Default Projects Location')
    defaultProjectPathField = cmds.textField('defaultProjectPathField', text='P:/', width=(wt-95), editable=False)
    defaultProjFileLabel = cmds.text('defaultProjFileLabel', label='Default Projects File')
    defaultProjectFilePathField = cmds.textField('defaultProjectFilePathField', text='P:/zoobeProjects', width=(wt-95), editable=False)
    editDefaultLocBtn = cmds.button('editDefaultLocBtn', label='Edit Location...', width= 100, height=45)
    
    #Project Settings Projects List Controls
    projectsSelListLabel = cmds.text('projectsSelListLabel', label='Projects List' )
    projectsSelList = cmds.textScrollList('projectsSelList', width=160 ,height=240 )
    projectsNewBtn = cmds.button('projectsNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=77, command='zoobeProjectMan.zoobeCreateNewProject()')
    projectsDelBtn = cmds.button('projectsDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=77)
    projectsEditBtn = cmds.button('projectsEditBtn', enable=False, backgroundColor=((0.559),(0.781),(0.781)), label='Edit...', width=160)
    
    #Project Settings Project Info Controls
    projectsInfoLabel = cmds.text('projectsInfoLabel', label='Project Info' )
    projectsInfoList = cmds.scrollField('projectsInfoList',editable=False, wordWrap=True, width=335 ,height=290 )    
    
    #Project Settings UI Controls
    projectsRefreshListBtn = cmds.button('projectsRefreshListBtn', label='Refresh List', height=30, width=((wt+125)/2))
    projectsCloseBtn = cmds.button('projectsCloseBtn', label='Close', height=30, width=((wt+125)/2))

    #Start Project Settings Form Edit
    cmds.formLayout(zoobeProjSettingsForm, edit=True,
    af=[
    
    (defaultProjLocLabel, 'left', 3),
    (defaultProjLocLabel, 'top', 8),
    
    (defaultProjectPathField, 'left', 125),
    (defaultProjectPathField, 'top', 5),
    
    (defaultProjFileLabel, 'left', 3),
    (defaultProjFileLabel, 'top', 28),
    
    (defaultProjectFilePathField, 'left', 125),
    (defaultProjectFilePathField, 'top', 26),
    
    (editDefaultLocBtn, 'left', 435),
    (editDefaultLocBtn, 'top', 3),
    
    (projectsSelListLabel, 'left', 5),
    (projectsSelListLabel, 'top', 60),
    
    (projectsSelList, 'left', 5),
    (projectsSelList, 'top', 80),
    
    (projectsNewBtn, 'left', 5),
    (projectsNewBtn, 'top', 320),
    
    (projectsDelBtn, 'left', 87),
    (projectsDelBtn, 'top', 320),
    
    (projectsEditBtn, 'left', 5),
    (projectsEditBtn, 'top', 345),
    
    (projectsInfoLabel, 'left', 200),
    (projectsInfoLabel, 'top', 60),
    
    (projectsInfoList, 'left', 200),
    (projectsInfoList, 'top', 80),
    
    (projectsRefreshListBtn, 'left', 5),
    (projectsRefreshListBtn, 'top', 375),
    
    (projectsCloseBtn, 'left', 273),
    (projectsCloseBtn, 'top', 375),
    
    ])
    cmds.showWindow(zoobePSettingsWin)     
def zoobeNewProjectMan():
    global ht
    global wt
    global tlc
    global user
    masterNames = zoobeMasterNames()
    
    #Clear pre-existing windows
    if(cmds.window('zoobePSettingsWin', exists=True)):
        cmds.deleteUI('zoobePSettingsWin')
    if(cmds.window('zoobeNewProjectWin', exists=True)):
        cmds.deleteUI('zoobeNewProjectWin')
    if(cmds.window('zoobePManWin', exists=True)):
        cmds.deleteUI('zoobePManWin')
    if(cmds.windowPref('zoobePManWin', exists=True)):
        cmds.windowPref('zoobePManWin', edit=True, width=wt, height=ht, topLeftCorner=(tlc, tlc))

    zoobePManWin = cmds.window('zoobePManWin', width=wt, height=ht, topLeftCorner=(tlc, tlc), menuBar = True, sizeable = False, title="Zoobe Project Manager v1.0")
    #Start Window Menu Item creation
    cmds.menu( label='File')
    cmds.menuItem( label='Save Workshop...' )
    cmds.menuItem( label='Save Master...' )
    cmds.menu( label='Edit')
    cmds.menuItem( label='Revive File...' )
    cmds.menu( label='Maya Tools')
    cmds.menuItem( label='Reference Editor...' )
    cmds.menuItem( label='Project Window...' )
    cmds.menuItem( label='Set Project...' )
    cmds.menuItem( divider=True )
    cmds.menuItem( label='Namespace Editor...' )
    cmds.menuItem( label='Hypershade...' )
    cmds.menuItem( label='Outliner...' )
    cmds.menuItem( divider=True )
    cmds.menuItem( label='Normals Toggle' )
    cmds.menu( label='Add-Ons')
    
    cmds.menu( label='Preferences')
    cmds.menuItem( label='High Quality Playblast', checkBox = False )    
    cmds.menu( label='Help')
    cmds.menuItem( label='Documentation...' )
    cmds.menuItem( label='About Zoobe...' )
    cmds.menuItem( label='About Zoobe Project Manager...' )
    #End Window Menu Item Creation
    
    #Start Window Contents
    pManMainCl = cmds.columnLayout('pManMainCl', width=(wt-10), height=(ht-10))
    pManMainForm = cmds.formLayout('pManMainForm', numberOfDivisions=100)
    #User option Menu Controls
    pManUserLabel = cmds.text('pManUserLabel',label='User Name: ')
    pManUser = cmds.optionMenu('pManUser', width=(wt-200), enable=True)
    #Edit User Name Dropdown contents
    zoobeGetUser()
    cmds.optionMenu('pManUser', edit=True, enable=False)
    #Project option Menu Controls
    pManProjectLabel = cmds.text('pManProjectLabel',label='Project Name: ')
    pManProject = cmds.optionMenu('pManProject', width=(wt-250), enable=True)
    
    #Project Manager Button if user is part of the master's list it will be enabled
    pManProjectSetup = cmds.button('pManProjectSetup', command='zoobeProjectMan2.zoobeProjectSettings()', label='Project Manager...', width=110, height=36)
    for userNames in masterNames:
        if(userNames == user):
            cmds.button('pManProjectSetup', edit=True, enable=True)
            break
        else:
            cmds.button('pManProjectSetup', edit=True, enable=False)
    #Project Manager Project Path Controls
    pManProjectPathLabel = cmds.text('pManProjectPathLabel',label='Project Path: ')
    pManProjectPathField = cmds.textField('pManProjectPathField', text='', width=(wt-85), editable=False)
    
    #Project Manager Footer Controls
    pManRefreshUIBtn = cmds.button('pManRefreshUIBtn',label='Refresh UI', width=190, height=36, command='zoobeProjectMan.zoobeRefreshProjectManUI()')
    pManCloseUIBtn = cmds.button('pManCloseUIBtn',label='Close UI', width=190, height=36)
    
    #Project Manager Header Icon
    pManHeaderIcon= cmds.image('pManHeaderIcon', width=400, height=80,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobePMHeaderIcon.png'))
    
    #Tab Layout Contents
    pManMainTabLO = cmds.tabLayout('pManMainTabLO', height=430, width=(wt-10), tabsVisible=True, enableBackground=True)
    
    #Open Tab
    pManOpenTab = cmds.columnLayout('pManOpenTab', width=380, height=430)	
    #Currently Open Form Layout and children
    pManOpenForm = cmds.formLayout('pManOpenForm', numberOfDivisions=100)
    #Open Form Header Controls
    currentLabel = cmds.text('currentLabel', label='CURRENTLY OPEN:', font='boldLabelFont')
    currentFileOpenLabel =  cmds.text('currentFileOpenLabel', label='none')
    currentVersionLabel =  cmds.text('currentVersionLabel', backgroundColor=((1.0),(0.665),(0.498)), label='', width=375)
    currentSeparator = cmds.separator('currentSeparator', width=390, height=40, style='in' )
    #Open Workshop Actions
    currentActionsLabel = cmds.text('currentActionsLabel', label='Actions', font='boldLabelFont')
    currentSaveWSBtn = cmds.button('currentSaveWSBtn',backgroundColor=((0),(0.667),(0)), label='Save Workshop...', width=155)
    currentSaveMasterBtn = cmds.button('currentSaveMasterBtn',backgroundColor=((1.0),(0.667),(0)), label='Save Master...', width=155)
    currentReviveBtn = cmds.button('currentReviveBtn',backgroundColor=((0.333),(0.667),(1.0)), label='Revive...', width=75)
    currentCloseBtn = cmds.button('currentCloseBtn',backgroundColor=((0.839),(0.839),(0.839)), label='Close', width=75)
    #Project Manager History Contents
    currentHistoryLabel = cmds.text('currentHistoryLabel', label='History', font='boldLabelFont')
    currentHistoryScroll = cmds.scrollField('currentHistoryScroll', editable=False, wordWrap=True, text='', width=200 ,height=90 )  
    #Project Manager Shots Contents
    currentNotesLabel = cmds.text('currentNotesLabel', label='Notes', font='boldLabelFont')
    currentNotesScroll = cmds.scrollField('currentNotesScroll', editable=False, wordWrap=True, text='', width=200 ,height=125 )
    currentClearNotesBtn = cmds.button('currentClearNotesBtn',label='Clear', width=95)
    currentSaveNotesBtn = cmds.button('currentSaveNotesBtn',enable=False, label='Save', width=95)
    #Project Manager Preview Contents
    currentPreviewLabel = cmds.text('currentPreviewLabel', label='Preview', font='boldLabelFont')    
    currentPreviewIcon= cmds.image('currentPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    currentTakeSnapBtn = cmds.button('currentTakeSnapBtn',label='Take Snapshot', width=155)
    currentRecPBBtn = cmds.button('currentRecPBBtn',label='Rec Playblast', width=77)
    currentViewPBBtn = cmds.button('currentViewPBBtn',enable=False, label='View Playblast', width=77)
    #Project Manager Open Tab Location Controls
    currentOpenLocTxt = cmds.text('currentOpenLocTxt', label='Location')
    currentOpenAssetLocField = cmds.textField('currentOpenAssetLocField', text='', width=(wt-102), editable=False)
    currentOpenAssetLocExploreBtn = cmds.button('currentOpenAssetLocExploreBtn',label='Explore...', width=75)
    #Start Edit of Open Form Contents
    cmds.formLayout(pManOpenForm, edit=True, 
    af=[	
    
    (currentLabel, 'left', 5), 
    (currentLabel, 'top', 5),
    
    (currentFileOpenLabel, 'left', 5), 
    (currentFileOpenLabel, 'top', 20),
    
    (currentVersionLabel, 'left', 0), 
    (currentVersionLabel, 'top', 40),
    
    (currentSeparator, 'left', 0), 
    (currentSeparator, 'top', 40),
    
    (currentActionsLabel, 'left', 5), 
    (currentActionsLabel, 'top', 70),
    
    (currentSaveWSBtn, 'left', 10), 
    (currentSaveWSBtn, 'top', 90),
    
    (currentSaveMasterBtn, 'left', 10), 
    (currentSaveMasterBtn, 'top', 120),
    
    (currentReviveBtn, 'left', 10), 
    (currentReviveBtn, 'top', 150),
    
    (currentCloseBtn, 'left', 90), 
    (currentCloseBtn, 'top', 150),
    
    (currentHistoryLabel, 'left', 180), 
    (currentHistoryLabel, 'top', 70),
    
    (currentHistoryScroll, 'left', 180), 
    (currentHistoryScroll, 'top', 90),
    
    (currentPreviewLabel, 'left', 5), 
    (currentPreviewLabel, 'top', 190),
    
    (currentPreviewIcon, 'left', 10), 
    (currentPreviewIcon, 'top', 205),
    
    (currentTakeSnapBtn, 'left', 10), 
    (currentTakeSnapBtn, 'top', 309),
    
    (currentRecPBBtn, 'left', 10), 
    (currentRecPBBtn, 'top', 331),
    
    (currentViewPBBtn, 'left', 87), 
    (currentViewPBBtn, 'top', 331),
    
    (currentNotesLabel, 'left', 180), 
    (currentNotesLabel, 'top', 190),
    
    (currentNotesScroll, 'left', 180), 
    (currentNotesScroll, 'top', 205),
    
    (currentClearNotesBtn, 'left', 180), 
    (currentClearNotesBtn, 'top', 331),
    
    (currentSaveNotesBtn, 'left', 285), 
    (currentSaveNotesBtn, 'top', 331),
    
    (currentOpenLocTxt, 'left', 175), 
    (currentOpenLocTxt, 'top', 365),
    
    (currentOpenAssetLocField, 'left', 5), 
    (currentOpenAssetLocField, 'top', 382),
    
    (currentOpenAssetLocExploreBtn, 'left', 305), 
    (currentOpenAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Open Form Contents
    cmds.setParent('pManMainTabLO')
    
    
    #Asset Browser Tab
    pManAssetTab = cmds.columnLayout('pManAssetTab', width=380, height=430)	
    #Asset Browser Form Layout and children
    pManAssetForm = cmds.formLayout('pManAssetForm', numberOfDivisions=100)
    #Asset Browser Tab Header Controls
    assetSeparator01 = cmds.separator('assetSeparator01', width=390, style='in' )
    assetLabel = cmds.text('assetLabel', label='ASSET BROWSER', font='boldLabelFont')
    assetSeparator02 = cmds.separator('assetSeparator02', width=390, style='in' )
    #Asset Browser Main Controls
    #Asset Types Controls
    assetTypesSelLabel = cmds.text('assetTypesSelLabel', label='Asset Types', font='boldLabelFont')
    assetTypesList = cmds.textScrollList('assetTypesList', width=123 ,height=110 )
    assetTypesNewBtn = cmds.button('assetsTypesNewBtn',backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60, command='zoobeProjectMan.zoobeNewAssetUI()')
    assetTypesDelBtn = cmds.button('assetsTypesDelBtn',enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Asset Selection Controls
    assetsSelLabel = cmds.text('assetsSelLabel', label='Assets', font='boldLabelFont')
    assetsSelActionsBtn = cmds.iconTextButton('assetsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    assetSelList = cmds.textScrollList('assetSelList', width=123 ,height=90 )
    assetsSelNewBtn = cmds.button('assetsSelNewBtn',backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    assetsSelDelBtn = cmds.button('assetsSelDelBtn',enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    assetsSelRenameBtn = cmds.button('assetsSelRenameBtn',enable=False, backgroundColor=((0.494),(1.0),(0.580)), label='Rename...', width=123)
    #Components Selection Controls
    assetComponentsSelLabel = cmds.text('assetComponentsSelLabel', label='Components', font='boldLabelFont')
    assetComponentsSelActionsBtn = cmds.iconTextButton('assetComponentsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    assetComponentsSelList = cmds.textScrollList('assetComponentsSelList', width=123 ,height=90 )
    assetComponentsNewBtn = cmds.button('assetComponentsNewBtn',backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    assetComponentsDelBtn = cmds.button('assetComponentsDelBtn',enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Asset Browser Preview Controls
    assetPreviewLabel = cmds.text('assetPreviewLabel', label='Preview', font='boldLabelFont')    
    assetPreviewIcon= cmds.image('assetPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    assetViewPBBtn = cmds.button('assetViewPBBtn', enable=False, label='View Playblast', width=155, height=30)
    #Asset Browser History Controls
    assetHistoryLabel = cmds.text('assetHistoryLabel', label='History', font='boldLabelFont')
    assetHistoryScroll = cmds.scrollField('assetHistoryScroll', editable=False, wordWrap=True, text='', width=210 ,height=65 )  
    #Asset Browser Notes Controls
    assetNotesLabel = cmds.text('assetNotesLabel', label='Notes', font='boldLabelFont')
    assetNotesScroll = cmds.scrollField('assetNotesScroll', editable=False, wordWrap=True, text='', width=210 ,height=55 )    
    #Project Manager Asset Browser Tab Location Controls
    assetLocTxt = cmds.text('assetLocTxt', label='Location')
    pManAssetAssetLocField = cmds.textField('pManAssetAssetLocField', text='', width=(wt-102), editable=False)
    pManAssetAssetLocExploreBtn = cmds.button('pManAssetAssetLocExploreBtn',label='Explore...', width=75)
    #Start Edit of Asset Browser Form Contents
    cmds.formLayout(pManAssetForm, edit=True, 
    af=[	
    
    (assetSeparator01, 'left', 0), 
    (assetSeparator01, 'top', 5),
    
    (assetLabel, 'left', 5), 
    (assetLabel, 'top', 10),
    
    (assetSeparator02, 'left', 0), 
    (assetSeparator02, 'top', 25),
    
    (assetTypesSelLabel, 'left', 5), 
    (assetTypesSelLabel, 'top', 30),
    
    (assetTypesList, 'left', 5), 
    (assetTypesList, 'top', 50),
    
    (assetTypesNewBtn, 'left', 5), 
    (assetTypesNewBtn, 'top', 160),
    
    (assetTypesDelBtn, 'left', 68), 
    (assetTypesDelBtn, 'top', 160),
    
    (assetsSelLabel, 'left', 133), 
    (assetsSelLabel, 'top', 30),
    
    (assetsSelActionsBtn, 'left', 133), 
    (assetsSelActionsBtn, 'top', 45),
    
    (assetSelList, 'left', 133), 
    (assetSelList, 'top', 70),
    
    (assetsSelNewBtn, 'left', 133), 
    (assetsSelNewBtn, 'top', 160),
    
    (assetsSelDelBtn, 'left', 195), 
    (assetsSelDelBtn, 'top', 160),
    
    (assetsSelRenameBtn, 'left', 133), 
    (assetsSelRenameBtn, 'top', 185),
    
    (assetComponentsSelLabel, 'left', 260), 
    (assetComponentsSelLabel, 'top', 30),
    
    (assetComponentsSelActionsBtn, 'left', 260), 
    (assetComponentsSelActionsBtn, 'top', 45),
    
    (assetComponentsSelList, 'left', 260), 
    (assetComponentsSelList, 'top', 70),
    
    (assetComponentsNewBtn, 'left', 260), 
    (assetComponentsNewBtn, 'top', 160),
    
    (assetComponentsDelBtn, 'left', 323), 
    (assetComponentsDelBtn, 'top', 160),
    
    (assetPreviewLabel, 'left', 5), 
    (assetPreviewLabel, 'top', 210),
    
    (assetPreviewIcon, 'left', 5), 
    (assetPreviewIcon, 'top', 225),    
    
    (assetViewPBBtn, 'left', 5), 
    (assetViewPBBtn, 'top', 329),    
    
    (assetHistoryLabel, 'left', 170), 
    (assetHistoryLabel, 'top', 210),
    
    (assetHistoryScroll, 'left', 170), 
    (assetHistoryScroll, 'top', 225),
    
    (assetNotesLabel, 'left', 170), 
    (assetNotesLabel, 'top', 290),
    
    (assetNotesScroll, 'left', 170), 
    (assetNotesScroll, 'top', 305),    
    
    (assetLocTxt, 'left', 175), 
    (assetLocTxt, 'top', 365),
    
    (pManAssetAssetLocField, 'left', 5), 
    (pManAssetAssetLocField, 'top', 382),
    
    (pManAssetAssetLocExploreBtn, 'left', 305), 
    (pManAssetAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Asset Browser Form Contents
    cmds.setParent('pManMainTabLO')
    
    #Shot Tab
    pManShotTab = cmds.columnLayout('pManShotTab', width=380, height=430)	
    #Shot Browser Form Layout and children
    pManShotForm = cmds.formLayout('pManShotForm', numberOfDivisions=100)
    #Shot Browser Tab Header Controls
    shotSeparator01 = cmds.separator('shotSeparator01', width=390, style='in' )
    shotLabel = cmds.text('shotLabel', label='SHOT BROWSER', font='boldLabelFont')
    shotSeparator02 = cmds.separator('shotSeparator02', width=390, style='in' )
    #Shot Browser Main Controls
    #Shot Types Controls
    shotSequenceSelLabel = cmds.text('shotSequenceSelLabel', label='Sequence', font='boldLabelFont')
    shotSequenceList = cmds.textScrollList('shotSequenceList', width=123 ,height=110 )
    shotSequenceNewBtn = cmds.button('shotSequenceNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotSequenceDelBtn = cmds.button('shotSequenceDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Shot Selection Controls
    shotsSelLabel = cmds.text('shotsSelLabel', label='Shot', font='boldLabelFont')
    shotsSelActionsBtn = cmds.iconTextButton('shotsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    shotSelList = cmds.textScrollList('shotSelList', width=123 ,height=90 )
    shotsSelNewBtn = cmds.button('shotsSelNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotsSelDelBtn = cmds.button('shotsSelDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Components Selection Controls
    shotComponentsSelLabel = cmds.text('shotComponentsSelLabel', label='Components', font='boldLabelFont')
    shotComponentsSelActionsBtn = cmds.iconTextButton('shotComponentsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    shotComponentsSelList = cmds.textScrollList('shotComponentsSelList', width=123 ,height=90 )
    shotComponentsNewBtn = cmds.button('shotComponentsNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotComponentsDelBtn = cmds.button('shotComponentsDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Shot Browser Preview Controls
    shotPreviewLabel = cmds.text('shotPreviewLabel', label='Preview', font='boldLabelFont')    
    shotPreviewIcon= cmds.image('shotPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    shotViewPBBtn = cmds.button('shotViewPBBtn', enable=False, label='View Playblast', width=155, height=30)
    #Shot Browser History Controls
    shotHistoryLabel = cmds.text('shotHistoryLabel', label='History', font='boldLabelFont')
    shotHistoryScroll = cmds.scrollField('shotHistoryScroll', editable=False, wordWrap=True, text='', width=210 ,height=65 )  
    #Shot Browser Notes Controls
    shotNotesLabel = cmds.text('shotNotesLabel', label='Notes', font='boldLabelFont')
    shotNotesScroll = cmds.scrollField('shotNotesScroll', editable=False, wordWrap=True, text='', width=210 ,height=55 )
    shotLocTxt = cmds.text('assetLocTxt', label='Location')
    pManShotAssetLocField = cmds.textField('pManShotAssetLocField', text='', width=(wt-102), editable=False)
    pManShotAssetLocExploreBtn = cmds.button('pManShotAssetLocExploreBtn',label='Explore...', width=75)
    #Start Edit of Shot Browser Form Contents
    cmds.formLayout(pManShotForm, edit=True, 
    af=[	
    
    (shotSeparator01, 'left', 0), 
    (shotSeparator01, 'top', 5),
    
    (shotLabel, 'left', 5), 
    (shotLabel, 'top', 10),
    
    (shotSeparator02, 'left', 0), 
    (shotSeparator02, 'top', 25),
    
    (shotSequenceSelLabel, 'left', 5), 
    (shotSequenceSelLabel, 'top', 30),
    
    (shotSequenceList, 'left', 5), 
    (shotSequenceList, 'top', 50),
    
    (shotSequenceNewBtn, 'left', 5), 
    (shotSequenceNewBtn, 'top', 160),
    
    (shotSequenceDelBtn, 'left', 68), 
    (shotSequenceDelBtn, 'top', 160),
    
    (shotsSelLabel, 'left', 133), 
    (shotsSelLabel, 'top', 30),
    
    (shotsSelActionsBtn, 'left', 133), 
    (shotsSelActionsBtn, 'top', 45),
    
    (shotSelList, 'left', 133), 
    (shotSelList, 'top', 70),
    
    (shotsSelNewBtn, 'left', 133), 
    (shotsSelNewBtn, 'top', 160),
    
    (shotsSelDelBtn, 'left', 195), 
    (shotsSelDelBtn, 'top', 160),
    
    (shotComponentsSelLabel, 'left', 260), 
    (shotComponentsSelLabel, 'top', 30),
    
    (shotComponentsSelActionsBtn, 'left', 260), 
    (shotComponentsSelActionsBtn, 'top', 45),
    
    (shotComponentsSelList, 'left', 260), 
    (shotComponentsSelList, 'top', 70),
    
    (shotComponentsNewBtn, 'left', 260), 
    (shotComponentsNewBtn, 'top', 160),
    
    (shotComponentsDelBtn, 'left', 323), 
    (shotComponentsDelBtn, 'top', 160),
    
    (shotPreviewLabel, 'left', 5), 
    (shotPreviewLabel, 'top', 210),
    
    (shotPreviewIcon, 'left', 5), 
    (shotPreviewIcon, 'top', 225),    
    
    (shotViewPBBtn, 'left', 5), 
    (shotViewPBBtn, 'top', 329),    
    
    (shotHistoryLabel, 'left', 170), 
    (shotHistoryLabel, 'top', 210),
    
    (shotHistoryScroll, 'left', 170), 
    (shotHistoryScroll, 'top', 225),
    
    (shotNotesLabel, 'left', 170), 
    (shotNotesLabel, 'top', 290),
    
    (shotNotesScroll, 'left', 170), 
    (shotNotesScroll, 'top', 305), 
    
    (shotLocTxt, 'left', 175), 
    (shotLocTxt, 'top', 365),
    
    (pManShotAssetLocField, 'left', 5), 
    (pManShotAssetLocField, 'top', 382),
    
    (pManShotAssetLocExploreBtn, 'left', 305), 
    (pManShotAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Shot Browser Form Contents
    cmds.setParent('pManMainTabLO')
    #End Window Contents
    
    #Start Main Form Edit
    cmds.formLayout(pManMainForm, edit=True, 
    af=[	
    
    (pManUserLabel, 'left', 5), 
    (pManUserLabel, 'top', 6),
    
    (pManUser, 'left', 80), 
    (pManUser, 'top', 5),
    
    (pManProjectLabel, 'left', 5), 
    (pManProjectLabel, 'top', 31),
    
    (pManProject, 'left', 80), 
    (pManProject, 'top', 30),
    
    (pManProjectSetup, 'left', 285), 
    (pManProjectSetup, 'top', 5),
    
    (pManProjectPathLabel, 'left', 5), 
    (pManProjectPathLabel, 'top', 56),
    
    (pManProjectPathField, 'left', 80), 
    (pManProjectPathField, 'top', 55),
    
    (pManHeaderIcon, 'left', 0), 
    (pManHeaderIcon, 'top', 80),
    
    (pManRefreshUIBtn, 'left', 5), 
    (pManRefreshUIBtn, 'top', 600),
    
    (pManCloseUIBtn, 'left', 205), 
    (pManCloseUIBtn, 'top', 600),
    
    (pManMainTabLO, 'left', 5), 
    (pManMainTabLO, 'top', 165),
    ])
    #End Main Form Edit
    
    #Editing the labels of the Tab Layout
    cmds.tabLayout('pManMainTabLO', edit=True, tabLabel=(('pManOpenTab', 'Currently Open'), ('pManAssetTab', 'Asset Browser'), ('pManShotTab', 'Shot Browser') ))	
    
    cmds.showWindow(zoobePManWin)
def zoobeInitProjectMan(projects):
    global ht
    global wt
    global tlc
    global user
    masterNames = zoobeMasterNames()
    
    if(cmds.window('zoobeRemoveDirWin', exists=True)):
        cmds.deleteUI('zoobeRemoveDirWin')
    if(cmds.window('zoobeNewAssetTypWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetTypWin')
    if(cmds.window('zoobeNewAssetWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetWin')
    if(cmds.window('zoobeNewCompWin', exists=True)):
        cmds.deleteUI('zoobeNewCompWin')
    if(cmds.window('zoobePSettingsWin', exists=True)):
        cmds.deleteUI('zoobePSettingsWin')
    if(cmds.window('zoobeNewProjectWin', exists=True)):
        cmds.deleteUI('zoobeNewProjectWin')
    if(cmds.window('zoobePManWin', exists=True)):
        cmds.deleteUI('zoobePManWin')
    if(cmds.windowPref('zoobePManWin', exists=True)):
        cmds.windowPref('zoobePManWin', edit=True, width=wt, height=ht, topLeftCorner=(tlc, tlc))

    zoobePManWin = cmds.window('zoobePManWin', width=wt, height=ht, topLeftCorner=(tlc, tlc), menuBar = True, sizeable = False, title="Zoobe Project Manager v1.0")
    #Start Window Menu Item creation
    cmds.menu( label='File')
    cmds.menuItem( label='Save Workshop...' )
    cmds.menuItem( label='Save Master...' )
    cmds.menu( label='Edit')
    cmds.menuItem( label='Revive File...' )
    cmds.menu( label='Maya Tools')
    cmds.menuItem( label='Reference Editor...', command="mel.eval('ReferenceEditor')" )
    cmds.menuItem('projectWin', label='Project Window...', command='zoobeProjectMan2.zoobeProjectSettings()' )
    for userNames in masterNames:
        if(userNames == user):
            cmds.menuItem('projectWin', edit=True, enable=True)
        else:
            cmds.menuItem('projectWin', edit=True, enable=False)
    cmds.menuItem( label='Set Project...', command="mel.eval('SetProject')" )
    cmds.menuItem( divider=True )
    cmds.menuItem( label='Namespace Editor...', command="mel.eval('NamespaceEditor')" )
    cmds.menuItem( label='Hypershade...', command="mel.eval('HypershadeWindow')" )
    cmds.menuItem( label='Outliner...', command="mel.eval('OutlinerWindow')"  )
    cmds.menuItem( divider=True )
    cmds.menuItem( label='Normals Toggle', command="mel.eval('ToggleFaceNormalDisplay')"  )
    cmds.menu( label='Add-Ons')
    cmds.menuItem( label='Animation Binder', command='zoobeProjectMan2.zoobeAnimBinder()'  )
    
    cmds.menu( label='Preferences')
    cmds.menuItem( label='High Quality Playblast', checkBox = False )    
    cmds.menu( label='Help')
    cmds.menuItem( label='Documentation...' )
    cmds.menuItem( label='About Zoobe...' )
    cmds.menuItem( label='About Zoobe Project Manager...' )
    #End Window Menu Item Creation
    
    #Start Window Contents
    pManMainCl = cmds.columnLayout('pManMainCl', width=(wt-10), height=(ht-10))
    pManMainForm = cmds.formLayout('pManMainForm', numberOfDivisions=100)
    #User option Menu Controls
    pManUserLabel = cmds.text('pManUserLabel',label='User Name: ')
    pManUser = cmds.optionMenu('pManUser', width=(wt-200), enable=True)
    #Edit User Name Dropdown contents
    zoobeGetUser()
    cmds.optionMenu('pManUser', edit=True, enable=False)
    #Project option Menu Controls
    pManProjectLabel = cmds.text('pManProjectLabel',label='Project Name: ')
    pManProject = cmds.optionMenu('pManProject', width=(wt-250), enable=True, changeCommand='zoobeProjectMan2.zoobeChangeProjectSelectPath()')
    #Add Projects to the Dropdown menu
    zoobeGetProjects(projects)
    
    #Project Manager Button if user is part of the master's list it will be enabled
    pManProjectSetup = cmds.button('pManProjectSetup', command='zoobeProjectMan2.zoobeProjectSettings()', label='Project Manager...', width=110, height=36)
    for userNames in masterNames:
        if(userNames == user):
            cmds.button('pManProjectSetup', edit=True, enable=True)
            break
        else:
            cmds.button('pManProjectSetup', edit=True, enable=False)
    #Project Manager Project Path Controls
    pManProjectPathLabel = cmds.text('pManProjectPathLabel',label='Project Path: ')
    pManProjectPathField = cmds.textField('pManProjectPathField', text='', width=(wt-85), editable=False)
    
    #Project Manager Footer Controls
    pManRefreshUIBtn = cmds.button('pManRefreshUIBtn',label='Refresh UI', width=190, height=36, command='zoobeProjectMan2.zoobePManInit()')
    pManCloseUIBtn = cmds.button('pManCloseUIBtn',label='Close UI', width=190, height=36)
    
    #Project Manager Header Icon
    pManHeaderIcon= cmds.image('pManHeaderIcon', width=400, height=80,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobePMHeaderIcon.png'))
    
    #Tab Layout Contents
    pManMainTabLO = cmds.tabLayout('pManMainTabLO', height=430, width=(wt-10), tabsVisible=True, enableBackground=True)
    
    #Open Tab
    pManOpenTab = cmds.columnLayout('pManOpenTab', width=380, height=430)	
    #Currently Open Form Layout and children
    pManOpenForm = cmds.formLayout('pManOpenForm', numberOfDivisions=100)
    #Open Form Header Controls
    currentLabel = cmds.text('currentLabel', label='CURRENTLY OPEN:', font='boldLabelFont')
    currentFileOpenLabel =  cmds.text('currentFileOpenLabel', label='none')
    currentVersionLabel =  cmds.text('currentVersionLabel', backgroundColor=((1.0),(0.665),(0.498)), label='', width=375)
    currentSeparator = cmds.separator('currentSeparator', width=390, height=40, style='in' )
    #Open Workshop Actions
    currentActionsLabel = cmds.text('currentActionsLabel', label='Actions', font='boldLabelFont')
    currentSaveWSBtn = cmds.button('currentSaveWSBtn', enable=False, backgroundColor=((0),(0.667),(0)), label='Save Workshop...', width=155)
    currentSaveMasterBtn = cmds.button('currentSaveMasterBtn', enable=False, backgroundColor=((1.0),(0.667),(0)), label='Save Master...', width=155)
    currentReviveBtn = cmds.button('currentReviveBtn', enable=False, backgroundColor=((0.333),(0.667),(1.0)), label='Revive...', width=75)
    currentCloseBtn = cmds.button('currentCloseBtn', enable=False, backgroundColor=((0.839),(0.839),(0.839)), label='Close', width=75)
    #Project Manager History Contents
    currentHistoryLabel = cmds.text('currentHistoryLabel', label='History', font='boldLabelFont')
    currentHistoryScroll = cmds.scrollField('currentHistoryScroll', editable=False, wordWrap=True, text='', width=200 ,height=90 )  
    #Project Manager Shots Contents
    currentNotesLabel = cmds.text('currentNotesLabel', label='Notes', font='boldLabelFont')
    currentNotesScroll = cmds.scrollField('currentNotesScroll', editable=False, wordWrap=True, text='', width=200 ,height=125 )
    currentClearNotesBtn = cmds.button('currentClearNotesBtn', enable=False, label='Clear', width=95)
    currentSaveNotesBtn = cmds.button('currentSaveNotesBtn',enable=False, label='Save', width=95)
    #Project Manager Preview Contents
    currentPreviewLabel = cmds.text('currentPreviewLabel', label='Preview', font='boldLabelFont')    
    currentPreviewIcon= cmds.image('currentPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    currentTakeSnapBtn = cmds.button('currentTakeSnapBtn', enable=False, label='Take Snapshot', width=155)
    currentRecPBBtn = cmds.button('currentRecPBBtn', enable=False, label='Rec Playblast', width=77)
    currentViewPBBtn = cmds.button('currentViewPBBtn',enable=False, label='View Playblast', width=77)
    #Project Manager Open Tab Location Controls
    currentOpenLocTxt = cmds.text('currentOpenLocTxt', label='Location')
    currentOpenAssetLocField = cmds.textField('currentOpenAssetLocField', text='', width=(wt-102), editable=False)
    currentOpenAssetLocExploreBtn = cmds.button('currentOpenAssetLocExploreBtn', enable=False, label='Explore...', width=75)
    #Start Edit of Open Form Contents
    cmds.formLayout(pManOpenForm, edit=True, 
    af=[	
    
    (currentLabel, 'left', 5), 
    (currentLabel, 'top', 5),
    
    (currentFileOpenLabel, 'left', 5), 
    (currentFileOpenLabel, 'top', 20),
    
    (currentVersionLabel, 'left', 0), 
    (currentVersionLabel, 'top', 40),
    
    (currentSeparator, 'left', 0), 
    (currentSeparator, 'top', 40),
    
    (currentActionsLabel, 'left', 5), 
    (currentActionsLabel, 'top', 70),
    
    (currentSaveWSBtn, 'left', 10), 
    (currentSaveWSBtn, 'top', 90),
    
    (currentSaveMasterBtn, 'left', 10), 
    (currentSaveMasterBtn, 'top', 120),
    
    (currentReviveBtn, 'left', 10), 
    (currentReviveBtn, 'top', 150),
    
    (currentCloseBtn, 'left', 90), 
    (currentCloseBtn, 'top', 150),
    
    (currentHistoryLabel, 'left', 180), 
    (currentHistoryLabel, 'top', 70),
    
    (currentHistoryScroll, 'left', 180), 
    (currentHistoryScroll, 'top', 90),
    
    (currentPreviewLabel, 'left', 5), 
    (currentPreviewLabel, 'top', 190),
    
    (currentPreviewIcon, 'left', 10), 
    (currentPreviewIcon, 'top', 205),
    
    (currentTakeSnapBtn, 'left', 10), 
    (currentTakeSnapBtn, 'top', 309),
    
    (currentRecPBBtn, 'left', 10), 
    (currentRecPBBtn, 'top', 331),
    
    (currentViewPBBtn, 'left', 87), 
    (currentViewPBBtn, 'top', 331),
    
    (currentNotesLabel, 'left', 180), 
    (currentNotesLabel, 'top', 190),
    
    (currentNotesScroll, 'left', 180), 
    (currentNotesScroll, 'top', 205),
    
    (currentClearNotesBtn, 'left', 180), 
    (currentClearNotesBtn, 'top', 331),
    
    (currentSaveNotesBtn, 'left', 285), 
    (currentSaveNotesBtn, 'top', 331),
    
    (currentOpenLocTxt, 'left', 175), 
    (currentOpenLocTxt, 'top', 365),
    
    (currentOpenAssetLocField, 'left', 5), 
    (currentOpenAssetLocField, 'top', 382),
    
    (currentOpenAssetLocExploreBtn, 'left', 305), 
    (currentOpenAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Open Form Contents
    cmds.setParent('pManMainTabLO')
    
    
    #Asset Browser Tab
    pManAssetTab = cmds.columnLayout('pManAssetTab', width=380, height=430)	
    #Asset Browser Form Layout and children
    pManAssetForm = cmds.formLayout('pManAssetForm', numberOfDivisions=100)
    #Asset Browser Tab Header Controls
    assetSeparator01 = cmds.separator('assetSeparator01', width=390, style='in' )
    assetLabel = cmds.text('assetLabel', label='ASSET BROWSER', font='boldLabelFont')
    assetSeparator02 = cmds.separator('assetSeparator02', width=390, style='in' )
    #Asset Browser Main Controls
    #Asset Types Controls
    assetTypesSelLabel = cmds.text('assetTypesSelLabel', label='Asset Types', font='boldLabelFont')
    assetTypesList = cmds.textScrollList('assetTypesList', width=123 ,height=110, selectCommand="zoobeProjectMan2.zoobeGetListSelection('assetTypesList','assetSelList')" )
    assetTypesNewBtn = cmds.button('assetsTypesNewBtn',backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60, command='zoobeProjectMan2.zoobeNewAssetTypPrompt()')
    assetTypesDelBtn = cmds.button('assetsTypesDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60, command="zoobeProjectMan2.zoobeRemoveDirPrompt('assetTypesList')")
    #Asset Selection Controls
    assetsSelLabel = cmds.text('assetsSelLabel', label='Assets', font='boldLabelFont')
    assetsSelActionsBtn = cmds.iconTextButton('assetsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    assetSelList = cmds.textScrollList('assetSelList', width=123 ,height=90, selectCommand="zoobeProjectMan2.zoobeGetListSelection('assetSelList','assetComponentsSelList')" )
    assetsSelNewBtn = cmds.button('assetsSelNewBtn',backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60, command='zoobeProjectMan2.zoobeNewAssetPrompt()')
    assetsSelDelBtn = cmds.button('assetsSelDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #assetsSelRenameBtn = cmds.button('assetsSelRenameBtn',enable=False, backgroundColor=((0.494),(1.0),(0.580)), label='Rename...', width=123)
    #Components Selection Controls
    assetComponentsSelLabel = cmds.text('assetComponentsSelLabel', label='Components', font='boldLabelFont')
    assetComponentsSelActionsBtn = cmds.iconTextButton('assetComponentsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    assetComponentsSelList = cmds.textScrollList('assetComponentsSelList', width=123 ,height=90, selectCommand="zoobeProjectMan2.zoobeReadComponentXML('pManProjectPathField','assetTypesList','assetSelList','assetComponentsSelList')", doubleClickCommand="zoobeProjectMan2.zoobeOpenAsset('assetTypesList', 'assetSelList','assetComponentsSelList')" )
    assetComponentsNewBtn = cmds.button('assetComponentsNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60, command='zoobeProjectMan2.zoobeNewComponentPrompt()')
    for userNames in masterNames:
        if(userNames == user):
            cmds.button('assetComponentsNewBtn', edit=True, enable=True)
            break
        elif(userNames != user):
            cmds.button('assetComponentsNewBtn', edit=True, enable=False)
    assetComponentsDelBtn = cmds.button('assetComponentsDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Asset Browser Preview Controls
    assetPreviewLabel = cmds.text('assetPreviewLabel', label='Preview', font='boldLabelFont')    
    assetPreviewIcon= cmds.image('assetPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    assetViewPBBtn = cmds.button('assetViewPBBtn', enable=False, label='View Playblast', width=155, height=30)
    #Asset Browser History Controls
    assetHistoryLabel = cmds.text('assetHistoryLabel', label='History', font='boldLabelFont')
    assetHistoryScroll = cmds.scrollField('assetHistoryScroll', editable=False, wordWrap=True, font="smallPlainLabelFont", text='', width=210 ,height=65 )  
    #Asset Browser Notes Controls
    assetNotesLabel = cmds.text('assetNotesLabel', label='Notes', font='boldLabelFont')
    assetNotesScroll = cmds.scrollField('assetNotesScroll', editable=False, wordWrap=True, text='', width=210 ,height=55 )    
    #Project Manager Asset Browser Tab Location Controls
    assetLocTxt = cmds.text('assetLocTxt', label='Location')
    pManAssetAssetLocField = cmds.textField('pManAssetAssetLocField', text='', width=(wt-102), editable=False)
    pManAssetAssetLocExploreBtn = cmds.button('pManAssetAssetLocExploreBtn',label='Explore...', width=75)
    #Start Edit of Asset Browser Form Contents
    cmds.formLayout(pManAssetForm, edit=True, 
    af=[	
    
    (assetSeparator01, 'left', 0), 
    (assetSeparator01, 'top', 5),
    
    (assetLabel, 'left', 5), 
    (assetLabel, 'top', 10),
    
    (assetSeparator02, 'left', 0), 
    (assetSeparator02, 'top', 25),
    
    (assetTypesSelLabel, 'left', 5), 
    (assetTypesSelLabel, 'top', 30),
    
    (assetTypesList, 'left', 5), 
    (assetTypesList, 'top', 50),
    
    (assetTypesNewBtn, 'left', 5), 
    (assetTypesNewBtn, 'top', 160),
    
    (assetTypesDelBtn, 'left', 68), 
    (assetTypesDelBtn, 'top', 160),
    
    (assetsSelLabel, 'left', 133), 
    (assetsSelLabel, 'top', 30),
    
    (assetsSelActionsBtn, 'left', 133), 
    (assetsSelActionsBtn, 'top', 45),
    
    (assetSelList, 'left', 133), 
    (assetSelList, 'top', 70),
    
    (assetsSelNewBtn, 'left', 133), 
    (assetsSelNewBtn, 'top', 160),
    
    (assetsSelDelBtn, 'left', 195), 
    (assetsSelDelBtn, 'top', 160),
    
    #(assetsSelRenameBtn, 'left', 133), 
    #(assetsSelRenameBtn, 'top', 185),
    
    (assetComponentsSelLabel, 'left', 260), 
    (assetComponentsSelLabel, 'top', 30),
    
    (assetComponentsSelActionsBtn, 'left', 260), 
    (assetComponentsSelActionsBtn, 'top', 45),
    
    (assetComponentsSelList, 'left', 260), 
    (assetComponentsSelList, 'top', 70),
    
    (assetComponentsNewBtn, 'left', 260), 
    (assetComponentsNewBtn, 'top', 160),
    
    (assetComponentsDelBtn, 'left', 323), 
    (assetComponentsDelBtn, 'top', 160),
    
    (assetPreviewLabel, 'left', 5), 
    (assetPreviewLabel, 'top', 210),
    
    (assetPreviewIcon, 'left', 5), 
    (assetPreviewIcon, 'top', 225),    
    
    (assetViewPBBtn, 'left', 5), 
    (assetViewPBBtn, 'top', 329),    
    
    (assetHistoryLabel, 'left', 170), 
    (assetHistoryLabel, 'top', 210),
    
    (assetHistoryScroll, 'left', 170), 
    (assetHistoryScroll, 'top', 225),
    
    (assetNotesLabel, 'left', 170), 
    (assetNotesLabel, 'top', 290),
    
    (assetNotesScroll, 'left', 170), 
    (assetNotesScroll, 'top', 305),    
    
    (assetLocTxt, 'left', 175), 
    (assetLocTxt, 'top', 365),
    
    (pManAssetAssetLocField, 'left', 5), 
    (pManAssetAssetLocField, 'top', 382),
    
    (pManAssetAssetLocExploreBtn, 'left', 305), 
    (pManAssetAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Asset Browser Form Contents
    cmds.setParent('pManMainTabLO')
    
    #Shot Tab
    pManShotTab = cmds.columnLayout('pManShotTab', width=380, height=430)	
    #Shot Browser Form Layout and children
    pManShotForm = cmds.formLayout('pManShotForm', numberOfDivisions=100)
    #Shot Browser Tab Header Controls
    shotSeparator01 = cmds.separator('shotSeparator01', width=390, style='in' )
    shotLabel = cmds.text('shotLabel', label='SHOT BROWSER', font='boldLabelFont')
    shotSeparator02 = cmds.separator('shotSeparator02', width=390, style='in' )
    #Shot Browser Main Controls
    #Shot Types Controls
    shotSequenceSelLabel = cmds.text('shotSequenceSelLabel', label='Sequence', font='boldLabelFont')
    shotSequenceList = cmds.textScrollList('shotSequenceList', width=123 ,height=110 )
    shotSequenceNewBtn = cmds.button('shotSequenceNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotSequenceDelBtn = cmds.button('shotSequenceDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Shot Selection Controls
    shotsSelLabel = cmds.text('shotsSelLabel', label='Shot', font='boldLabelFont')
    shotsSelActionsBtn = cmds.iconTextButton('shotsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    shotSelList = cmds.textScrollList('shotSelList', width=123 ,height=90 )
    shotsSelNewBtn = cmds.button('shotsSelNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotsSelDelBtn = cmds.button('shotsSelDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Components Selection Controls
    shotComponentsSelLabel = cmds.text('shotComponentsSelLabel', label='Components', font='boldLabelFont')
    shotComponentsSelActionsBtn = cmds.iconTextButton('shotComponentsSelActionsBtn',style='textOnly', label='ACTIONS...', width=75)
    shotComponentsSelList = cmds.textScrollList('shotComponentsSelList', width=123 ,height=90 )
    shotComponentsNewBtn = cmds.button('shotComponentsNewBtn', backgroundColor=((0.494),(1.0),(0.580)), label='New..', width=60)
    shotComponentsDelBtn = cmds.button('shotComponentsDelBtn', enable=False, backgroundColor=((1.0),(0.220),(0.220)), label='Delete', width=60)
    #Shot Browser Preview Controls
    shotPreviewLabel = cmds.text('shotPreviewLabel', label='Preview', font='boldLabelFont')    
    shotPreviewIcon= cmds.image('shotPreviewIcon', width=155, height=104,image=('C:/Users/Juan/Dropbox/zoobe/icons/zoobeNoPreview.png'))
    shotViewPBBtn = cmds.button('shotViewPBBtn', enable=False, label='View Playblast', width=155, height=30)
    #Shot Browser History Controls
    shotHistoryLabel = cmds.text('shotHistoryLabel', label='History', font='boldLabelFont')
    shotHistoryScroll = cmds.scrollField('shotHistoryScroll', editable=False, wordWrap=True, text='', width=210 ,height=65 )  
    #Shot Browser Notes Controls
    shotNotesLabel = cmds.text('shotNotesLabel', label='Notes', font='boldLabelFont')
    shotNotesScroll = cmds.scrollField('shotNotesScroll', editable=False, wordWrap=True, text='', width=210 ,height=55 )
    shotLocTxt = cmds.text('assetLocTxt', label='Location')
    pManShotAssetLocField = cmds.textField('pManShotAssetLocField', text='', width=(wt-102), editable=False)
    pManShotAssetLocExploreBtn = cmds.button('pManShotAssetLocExploreBtn',label='Explore...', width=75)
    #Start Edit of Shot Browser Form Contents
    cmds.formLayout(pManShotForm, edit=True, 
    af=[	
    
    (shotSeparator01, 'left', 0), 
    (shotSeparator01, 'top', 5),
    
    (shotLabel, 'left', 5), 
    (shotLabel, 'top', 10),
    
    (shotSeparator02, 'left', 0), 
    (shotSeparator02, 'top', 25),
    
    (shotSequenceSelLabel, 'left', 5), 
    (shotSequenceSelLabel, 'top', 30),
    
    (shotSequenceList, 'left', 5), 
    (shotSequenceList, 'top', 50),
    
    (shotSequenceNewBtn, 'left', 5), 
    (shotSequenceNewBtn, 'top', 160),
    
    (shotSequenceDelBtn, 'left', 68), 
    (shotSequenceDelBtn, 'top', 160),
    
    (shotsSelLabel, 'left', 133), 
    (shotsSelLabel, 'top', 30),
    
    (shotsSelActionsBtn, 'left', 133), 
    (shotsSelActionsBtn, 'top', 45),
    
    (shotSelList, 'left', 133), 
    (shotSelList, 'top', 70),
    
    (shotsSelNewBtn, 'left', 133), 
    (shotsSelNewBtn, 'top', 160),
    
    (shotsSelDelBtn, 'left', 195), 
    (shotsSelDelBtn, 'top', 160),
    
    (shotComponentsSelLabel, 'left', 260), 
    (shotComponentsSelLabel, 'top', 30),
    
    (shotComponentsSelActionsBtn, 'left', 260), 
    (shotComponentsSelActionsBtn, 'top', 45),
    
    (shotComponentsSelList, 'left', 260), 
    (shotComponentsSelList, 'top', 70),
    
    (shotComponentsNewBtn, 'left', 260), 
    (shotComponentsNewBtn, 'top', 160),
    
    (shotComponentsDelBtn, 'left', 323), 
    (shotComponentsDelBtn, 'top', 160),
    
    (shotPreviewLabel, 'left', 5), 
    (shotPreviewLabel, 'top', 210),
    
    (shotPreviewIcon, 'left', 5), 
    (shotPreviewIcon, 'top', 225),    
    
    (shotViewPBBtn, 'left', 5), 
    (shotViewPBBtn, 'top', 329),    
    
    (shotHistoryLabel, 'left', 170), 
    (shotHistoryLabel, 'top', 210),
    
    (shotHistoryScroll, 'left', 170), 
    (shotHistoryScroll, 'top', 225),
    
    (shotNotesLabel, 'left', 170), 
    (shotNotesLabel, 'top', 290),
    
    (shotNotesScroll, 'left', 170), 
    (shotNotesScroll, 'top', 305), 
    
    (shotLocTxt, 'left', 175), 
    (shotLocTxt, 'top', 365),
    
    (pManShotAssetLocField, 'left', 5), 
    (pManShotAssetLocField, 'top', 382),
    
    (pManShotAssetLocExploreBtn, 'left', 305), 
    (pManShotAssetLocExploreBtn, 'top', 380),
    
    ])
    #End Edit of Shot Browser Form Contents
    cmds.setParent('pManMainTabLO')
    #End Window Contents
    
    #Start Main Form Edit
    cmds.formLayout(pManMainForm, edit=True, 
    af=[	
    
    (pManUserLabel, 'left', 5), 
    (pManUserLabel, 'top', 6),
    
    (pManUser, 'left', 80), 
    (pManUser, 'top', 5),
    
    (pManProjectLabel, 'left', 5), 
    (pManProjectLabel, 'top', 31),
    
    (pManProject, 'left', 80), 
    (pManProject, 'top', 30),
    
    (pManProjectSetup, 'left', 285), 
    (pManProjectSetup, 'top', 5),
    
    (pManProjectPathLabel, 'left', 5), 
    (pManProjectPathLabel, 'top', 56),
    
    (pManProjectPathField, 'left', 80), 
    (pManProjectPathField, 'top', 55),
    
    (pManHeaderIcon, 'left', 0), 
    (pManHeaderIcon, 'top', 80),
    
    (pManRefreshUIBtn, 'left', 5), 
    (pManRefreshUIBtn, 'top', 600),
    
    (pManCloseUIBtn, 'left', 205), 
    (pManCloseUIBtn, 'top', 600),
    
    (pManMainTabLO, 'left', 5), 
    (pManMainTabLO, 'top', 165),
    ])
    #End Main Form Edit
    
    #Editing the labels of the Tab Layout
    cmds.tabLayout('pManMainTabLO', edit=True, tabLabel=(('pManOpenTab', 'Currently Open'), ('pManAssetTab', 'Asset Browser'), ('pManShotTab', 'Shot Browser') ))	
    
    cmds.showWindow(zoobePManWin) 

    zoobeGetInitialProjectPath()
    dirPath = cmds.textField('pManProjectPathField', query=True, text=True)
    zoobeGetMainFoldersList(dirPath+'working_project')
    
    #Temp scripts for testing
    