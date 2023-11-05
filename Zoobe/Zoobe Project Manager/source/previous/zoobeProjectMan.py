import sys
import os
from xml.dom.minidom import Document, parse, parseString, Element
import maya.cmds as cmds
import maya.mel as mel


#Global Variables
ht=650
wt=400
tlc=150
user = mel.eval('getenv USER')
#masterName = zoobeProjectMan.zoobeMasterNames()
#zoobeProjectPathField = cmds.textFieldButtonGrp('zoobeProjectPathField')

def zoobeProjectMan():
    global ht
    global wt
    global tlc
    global user
    masterName = zoobeMasterNames()
    
    #sys.stdout.write(masterName+'\n\n')
    
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
    #Add Projects to the Dropdown menu
    zoobeGetProjects()
    
    #Project Manager Button if user is part of the master's list it will be enabled
    pManProjectSetup = cmds.button('pManProjectSetup', command='zoobeProjectMan.zoobeProjectSettings()', label='Project Manager...', width=110, height=36)
    if(masterName == user):
        cmds.button('pManProjectSetup', edit=True, enable=True)
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
    
    if __name__ == "__zoobeProjectMan__": zoobeProjectMan()
    
def zoobeGetUser():

    global user
    #sys.stdout.write(user)
    cmds.menuItem(label=user)
    
def zoobeGetProjects():

    cmds.menuItem(label='project01')
    cmds.menuItem(label='project02')
    
def zoobeChangeTabCmd():
    sys.stdout.write('Still Working on it')
    
def zoobeMasterNames():

    masterNames = 'Juan'
    
    return(masterNames)
    
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
    
def zoobeCreateNewProject():
    global ht
    global wt
    global tlc
    #global zoobeProjectPathField
    
    newDate = cmds.date( format='DD/MM/YYYY' )
    
    if(cmds.window('zoobeNewProjectWin', exists=True)):
        cmds.deleteUI('zoobeNewProjectWin')
    if(cmds.windowPref('zoobeNewProjectWin', exists=True)):
        cmds.windowPref('zoobeNewProjectWin', edit=True, width=(wt), height=(ht+90), topLeftCorner=((tlc+100), (tlc+50)))
    
    zoobeNewProjectWin = cmds.window('zoobeNewProjectWin', width=(wt), height=(ht+90), topLeftCorner=((tlc+100), (tlc+100)), menuBar = False, sizeable = False, title="Zoobe Create New Project")
    zoobeNewProjectMainCL = cmds.columnLayout('zoobeNewProjectMainCL', width=(wt), height=(ht+90))
    
    #New Project Controls
    zoobeNewProjectForm = cmds.formLayout('zoobeNewProjectForm', numberOfDivisions=100)
    #Project Name
    zoobeProjectNameLabel = cmds.text('zoobeProjectNameLabel', font='boldLabelFont', label='Project Name (max length 20):')
    zoobeProjectNameField = cmds.textField('zoobeProjectNameField', width=130, text='')
    zoobeProjectSep01 = cmds.separator('zoobeProjectSep01', style='in', width=wt)
    #Project Path
    zoobeProjectPathLabel = cmds.text('zoobeProjectPathLabel', font='boldLabelFont', label="Project Path:")
    zoobeProjectPathLabelWarning = cmds.text('zoobeProjectPathLabelWarning', label="(folders which don't already exist will be created)")
    zoobeProjectPathField = cmds.textFieldButtonGrp('zoobeProjectPathField', editable=False, buttonLabel="Browse...", columnWidth=((1, 330),(2,60)), text='', buttonCommand='zoobeProjectMan.zoobeGetProjectPath()')
    zoobeProjectSep02 = cmds.separator('zoobeProjectSep02', style='in', width=wt)
    #Project Description
    zoobeProjectDescriptionField= cmds.textFieldGrp('zoobeProjectDescriptionField', label="Description:  ", columnWidth=((1, 65),(2,325)), text='')
    zoobeProjectSep03 = cmds.separator('zoobeProjectSep03', style='in', width=wt)
    #Project Status
    zoobeProjectStatusLabel = cmds.text('zoobeProjectStatusLabel', font='boldLabelFont', label='Project Status:')
    zoobeProjectStatusOM = cmds.optionMenu('zoobeProjectStatusOM', width=(wt-250), enable=True )
    cmds.menuItem(label='active')
    cmds.menuItem(label='inactive')
    zoobeProjectStatusLabelWarning = cmds.text('zoobeProjectStatusLabelWarning', font='smallPlainLabelFont', label="(inactive projects won't appear in the main Project Manager window)")
    zoobeProjectSep04 = cmds.separator('zoobeProjectSep04', style='in', width=wt)
    #Project Dates
    zoobeProjectCreationField= cmds.textFieldGrp('zoobeProjectCreationField', columnWidth=((1, 100),(2,80)), label='Creation Date:        ', text=newDate)
    zoobeProjectDeadlineField= cmds.textFieldGrp('zoobeProjectDeadlineField', columnWidth=((1, 100),(2,80)), label='Deadline:        ', text=newDate)
    zoobeProjectSep05 = cmds.separator('zoobeProjectSep05', style='in', width=wt)
    #Project Maya Version
    zoobeProjectMayaVersion = cmds.checkBox('zoobeProjectMayaVersion', label='Enforce Maya Version', onCommand='zoobeProjectMan.zoobeForceMayaVersionOn()',offCommand='zoobeProjectMan.zoobeForceMayaVersionOff()')
    zoobeProjectMayaVersionFieldLabel = cmds.text('zoobeProjectMayaVersionFieldLabel', font='boldLabelFont', label='Maya Version to Enforce:')
    zoobeProjectMayaVersionField = cmds.textField('zoobeProjectMayaVersionField', enable=False, text='', width=60)    
    zoobeProjectSep06 = cmds.separator('zoobeProjectSep06', style='in', width=wt)
    #Project Folders and File Names Options
    #Master Files
    zoobeProjectMasterFilesLabel = cmds.text('zoobeProjectMasterFilesLabel', font='boldLabelFont', label='Master Files:')
    zoobeProjectMasterFilesWarning = cmds.text('zoobeProjectMasterFilesWarning', font='smallPlainLabelFont', label='(finalized versions with flattened references)')
    zoobeProjectMasterFilesField = cmds.textFieldGrp('zoobeProjectMasterFilesField', columnWidth=((1, 55),(2,100)), label='Name:      ', text='master')
    zoobeProjectMasterFilesExt = cmds.optionMenu('zoobeProjectMasterFilesExt', width=(wt-250), label='File Format:    ', enable=True )
    cmds.menuItem(label='mb')
    cmds.menuItem(label='ma')
    zoobeProjectSep07 = cmds.separator('zoobeProjectSep07', style='in', width=wt)
    #Workshop Files
    zoobeProjectWorkshopFilesLabel = cmds.text('zoobeProjectWorkshopFilesLabel', font='boldLabelFont', label='Workshop Files:')
    zoobeProjectWorkshopFilesWarning = cmds.text('zoobeProjectWorkshopFilesWarning', font='smallPlainLabelFont', label='(preliminary and test versions)')
    zoobeProjectWorkshopFilesField = cmds.textFieldGrp('zoobeProjectWorkshopFilesField', columnWidth=((1, 55),(2,100)), label='Name:      ', text='workshop')
    zoobeProjectWorkshopFilesExt = cmds.optionMenu('zoobeProjectWorkshopFilesExt', width=(wt-250), label='File Format:    ', enable=True )
    cmds.menuItem(label='mb')
    cmds.menuItem(label='ma')
    zoobeProjectSep08 = cmds.separator('zoobeProjectSep08', style='in', width=wt)
    #Sub-Folders 
    zoobeProjectSubFoldersLabel = cmds.text('zoobeProjectSubFoldersLabel', font='boldLabelFont', label='Sub-Folder Names:')
    zoobeProjectCamerasField = cmds.textFieldGrp('zoobeProjectCamerasField', columnWidth=((1, 75),(2,90)), label='Cameras:      ', text='cameras')
    zoobeProjectCGFXShaderField = cmds.textFieldGrp('zoobeProjectCGFXShaderField', columnWidth=((1, 75),(2,90)), label='Shaders:      ', text='cgfx_shader')
    zoobeProjectConceptsField = cmds.textFieldGrp('zoobeProjectConceptsField', columnWidth=((1, 75),(2,90)), label='Concepts:      ', text='concepts')
    zoobeProjectDataField = cmds.textFieldGrp('zoobeProjectDataField', columnWidth=((1, 75),(2,90)), label='Data:      ', text='data')
    zoobeProjectImagesField = cmds.textFieldGrp('zoobeProjectImagesField', columnWidth=((1, 75),(2,90)), label='Images:      ', text='images')
    zoobeProjectScenesField = cmds.textFieldGrp('zoobeProjectScenesField', columnWidth=((1, 75),(2,90)), label='Scenes:      ', text='scenes')
    zoobeProjectSourceImagesField = cmds.textFieldGrp('zoobeProjectSourceImagesField', columnWidth=((1, 75),(2,90)), label='Textures:      ', text='sourceimages')    
    zoobeProjectSep09 = cmds.separator('zoobeProjectSep09', style='in', width=wt)
    #Confirmation Controls
    zoobeProjectAcceptBtn = cmds.button('zoobeProjectAcceptBtn', width=175 , label='Accept', command='zoobeProjectMan.zoobeCheckProjectParams()')
    zoobeProjectCancelBtn = cmds.button('zoobeProjectCancelBtn', width=175 , label='Cancel', command='zoobeProjectMan.zoobeCancelNewProject()')
    
    cmds.setParent(zoobeNewProjectMainCL)
    
    cmds.formLayout(zoobeNewProjectForm, edit=True,    
    af=[
    
    (zoobeProjectNameLabel, 'left', 5),
    (zoobeProjectNameLabel, 'top', 3),
    
    (zoobeProjectNameField, 'left', 265),
    (zoobeProjectNameField, 'top', 2),
    
    (zoobeProjectSep01, 'left', 0),
    (zoobeProjectSep01, 'top', 25),
    
    (zoobeProjectPathLabel, 'left', 5),
    (zoobeProjectPathLabel, 'top', 30),
    
    (zoobeProjectPathLabelWarning, 'left', 150),
    (zoobeProjectPathLabelWarning, 'top', 30),
    
    (zoobeProjectPathField, 'left', 5),
    (zoobeProjectPathField, 'top', 50),
    
    (zoobeProjectSep02, 'left', 0),
    (zoobeProjectSep02, 'top', 80),
    
    (zoobeProjectDescriptionField, 'left', 0),
    (zoobeProjectDescriptionField, 'top', 85),
    
    (zoobeProjectSep03, 'left', 0),
    (zoobeProjectSep03, 'top', 110),
    
    (zoobeProjectStatusLabel, 'left', 5),
    (zoobeProjectStatusLabel, 'top', 116),
    
    (zoobeProjectStatusOM, 'left', 110),
    (zoobeProjectStatusOM, 'top', 115),
    
    (zoobeProjectStatusLabelWarning, 'left', 0),
    (zoobeProjectStatusLabelWarning, 'top', 140),
    
    (zoobeProjectSep04, 'left', 0),
    (zoobeProjectSep04, 'top', 160),
    
    (zoobeProjectCreationField, 'left', 0),
    (zoobeProjectCreationField, 'top', 165),
    
    (zoobeProjectDeadlineField, 'left', 200),
    (zoobeProjectDeadlineField, 'top', 165),
    
    (zoobeProjectSep05, 'left', 0),
    (zoobeProjectSep05, 'top', 190),
    
    (zoobeProjectMayaVersion, 'left', 5),
    (zoobeProjectMayaVersion, 'top', 200),
    
    (zoobeProjectMayaVersionFieldLabel, 'left', 5),
    (zoobeProjectMayaVersionFieldLabel, 'top', 222),
    
    (zoobeProjectMayaVersionField, 'left', 170),
    (zoobeProjectMayaVersionField, 'top', 220),
    
    (zoobeProjectSep06, 'left', 0),
    (zoobeProjectSep06, 'top', 245),
    
    (zoobeProjectMasterFilesLabel, 'left', 5),
    (zoobeProjectMasterFilesLabel, 'top', 250),
    
    (zoobeProjectMasterFilesWarning, 'left', 120),
    (zoobeProjectMasterFilesWarning, 'top', 250),
    
    (zoobeProjectMasterFilesField, 'left', 0),
    (zoobeProjectMasterFilesField, 'top', 270),
    
    (zoobeProjectMasterFilesExt, 'left', 230),
    (zoobeProjectMasterFilesExt, 'top', 270),
    
    (zoobeProjectSep07, 'left', 0),
    (zoobeProjectSep07, 'top', 295),
    
    (zoobeProjectWorkshopFilesLabel, 'left', 5),
    (zoobeProjectWorkshopFilesLabel, 'top', 305),
    
    (zoobeProjectWorkshopFilesWarning, 'left', 120),
    (zoobeProjectWorkshopFilesWarning, 'top', 305),
    
    (zoobeProjectWorkshopFilesField, 'left', 0),
    (zoobeProjectWorkshopFilesField, 'top', 325),
    
    (zoobeProjectWorkshopFilesExt, 'left', 230),
    (zoobeProjectWorkshopFilesExt, 'top', 325),
    
    (zoobeProjectSep08, 'left', 0),
    (zoobeProjectSep08, 'top', 350),    
    
    (zoobeProjectSubFoldersLabel, 'left', 5),
    (zoobeProjectSubFoldersLabel, 'top', 355),
    
    (zoobeProjectCamerasField, 'left', 5),
    (zoobeProjectCamerasField, 'top', 375),
    
    (zoobeProjectCGFXShaderField, 'left', 210),
    (zoobeProjectCGFXShaderField, 'top', 375),
    
    (zoobeProjectConceptsField, 'left', 5),
    (zoobeProjectConceptsField, 'top', 400),
    
    (zoobeProjectDataField, 'left', 210),
    (zoobeProjectDataField, 'top', 400),
    
    (zoobeProjectImagesField, 'left', 5),
    (zoobeProjectImagesField, 'top', 425),
    
    (zoobeProjectScenesField, 'left', 210),
    (zoobeProjectScenesField, 'top', 425),
    
    (zoobeProjectSourceImagesField, 'left', 5),
    (zoobeProjectSourceImagesField, 'top', 450),
    
    (zoobeProjectSep09, 'left', 0),
    (zoobeProjectSep09, 'top', 475),
    
    (zoobeProjectAcceptBtn, 'left', 20),
    (zoobeProjectAcceptBtn, 'top', 480),
    
    (zoobeProjectCancelBtn, 'left', 205),
    (zoobeProjectCancelBtn, 'top', 480),
    
    ])
    
    
    cmds.showWindow(zoobeNewProjectWin)
    
def zoobeGetProjectPath():
    
    #global zoobeProjectPathField
    
    newPath = mel.eval('string $docsPath[] = `fileDialog2 -fm 3`;string $docsFolder = ($docsPath[0]+"/");')    
    #projectPath = mel.eval('string $docsFolder = $docsPath[0];')
    
    cmds.textFieldButtonGrp('zoobeProjectPathField', edit=True, text=newPath)  

def zoobeForceMayaVersionOn():

    cmds.textField('zoobeProjectMayaVersionField', edit=True, enable=True) 
    
def zoobeForceMayaVersionOff():

    cmds.textField('zoobeProjectMayaVersionField', edit=True, text='', enable=False) 
    
def zoobeCheckProjectParams():

    projName = cmds.textField('zoobeProjectNameField', query=True, text=True)
    projPath = cmds.textFieldButtonGrp('zoobeProjectPathField', query=True, text=True)
    projDescription = cmds.textFieldGrp('zoobeProjectDescriptionField', query=True, text=True)
    projStatus = cmds.optionMenu('zoobeProjectStatusOM', query=True, value=True)
    projDate = cmds.textFieldGrp('zoobeProjectCreationField', query=True, text=True)
    projDeadline = cmds.textFieldGrp('zoobeProjectDeadlineField', query=True, text=True)
    projEnforceVersion = cmds.checkBox('zoobeProjectMayaVersion', query=True, value=True)
    if(projEnforceVersion == 1):
        projVersion = cmds.textField('zoobeProjectMayaVersionField', query=True, text=True)
    else:
        projVersion = ''
    projMasterFiles = cmds.textFieldGrp('zoobeProjectMasterFilesField', query=True, text=True)
    projMasterFormat = cmds.optionMenu('zoobeProjectMasterFilesExt', query=True, value=True)
    projWorkshopFiles = cmds.textFieldGrp('zoobeProjectWorkshopFilesField', query=True, text=True)
    projWorkshopFormat = cmds.optionMenu('zoobeProjectWorkshopFilesExt', query=True, value=True)
    projCameras = cmds.textFieldGrp('zoobeProjectCamerasField', query=True, text=True)
    projConcepts = cmds.textFieldGrp('zoobeProjectConceptsField', query=True, text=True)
    projImages = cmds.textFieldGrp('zoobeProjectImagesField', query=True, text=True)
    projTextures = cmds.textFieldGrp('zoobeProjectSourceImagesField', query=True, text=True)
    projShaders = cmds.textFieldGrp('zoobeProjectCGFXShaderField', query=True, text=True)
    projData = cmds.textFieldGrp('zoobeProjectDataField', query=True, text=True)
    projScenes = cmds.textFieldGrp('zoobeProjectScenesField', query=True, text=True)
    
    if(projName == ''):    
        cmds.error('Error: Must provide a project name, try again.')
    elif(len(projName)<3):
        cmds.error('Error: Project name has to be longer than 2 characters.')
    else:
        if(projPath == ''):
            cmds.error('Error: Project path not set, Please set a project path')
        else:
            if(projDescription == ''):
                cmds.error('Error: Project description not set, Please set a project description')
            else:
                if(len(projDate) < 10):
                    cmds.error('Error: Project creation date is too short, please check and try again')
                elif(len(projDate) > 10):
                    cmds.error('Error: Project creation date is too long, please check and try again')
                elif(len(projDeadline) < 10):
                    cmds.error('Error: Project deadline date is too short, please check and try again')
                elif(len(projDeadline) > 10):
                    cmds.error('Error: Project deadline date is too long, please check and try again')
                else:
                    if(projMasterFiles == ''):
                        cmds.error('Error: Please set a default master file name')
                    else:
                        if(projWorkshopFiles == ''):
                            cmds.error('Error: Please set a default workshop file name')
                        else:
                            if(projCameras == ''):
                                cmds.error('Error: Please set a default cameras folder name')
                            elif(projConcepts == ''):
                                cmds.error('Error: Please set a default concepts folder name')
                            elif(projImages == ''):
                                cmds.error('Error: Please set a default images folder name')
                            elif(projTextures == ''):
                                cmds.error('Error: Please set a default textures folder name')    
                            elif(projShaders == ''):
                                cmds.error('Error: Please set a default shaders folder name')
                            elif(projData == ''):
                                cmds.error('Error: Please set a default data folder name')
                            elif(projScenes == ''):
                                cmds.error('Error: Please set a default scenes folder name')
                            else:                                
                                #Close the project creation options window
                                zoobeReadXML(projName, projPath, projDescription, projStatus, projDate, projDeadline, projVersion, projMasterFiles, projMasterFormat, projWorkshopFiles, projWorkshopFormat, projCameras, projConcepts, projImages, projTextures, projShaders, projData, projScenes )
                                #Sets the project based on the UI selections and paths
                                #mel.eval('string $projPath = `textFieldButtonGrp -q -text zoobeProjectPathField`;string $projName = `textField -q -text zoobeProjectNameField`;setProject($projPath+$projName+"/working_project")')
                                #cmds.deleteUI('zoobeNewProjectWin')
                            
                                
                                
    '''
    sys.stdout.write(projName)
    sys.stdout.write('\n')
    sys.stdout.write(projPath)
    sys.stdout.write('\n')
    sys.stdout.write(projDescription)
    sys.stdout.write('\n')
    sys.stdout.write(projStatus)
    sys.stdout.write('\n')
    sys.stdout.write(projDate)
    sys.stdout.write('\n')
    sys.stdout.write(projDealine)
    sys.stdout.write('\n')
    sys.stdout.write(projEnforceVersion)
    sys.stdout.write('\n')
    sys.stdout.write(projVersion)
    sys.stdout.write('\n')
    sys.stdout.write(projMasterFiles)
    sys.stdout.write('\n')
    sys.stdout.write(projMasterFormat)
    sys.stdout.write('\n')
    sys.stdout.write(projWorkshopFiles)
    sys.stdout.write('\n')
    sys.stdout.write(projWorkshopFormat)
    sys.stdout.write('\n')
    sys.stdout.write(projCameras)
    sys.stdout.write('\n')
    sys.stdout.write(projConcepts)
    sys.stdout.write('\n')
    sys.stdout.write(projImages)
    sys.stdout.write('\n')
    sys.stdout.write(projTextures)
    sys.stdout.write('\n')
    sys.stdout.write(projShaders)
    sys.stdout.write('\n')
    sys.stdout.write(projData)
    sys.stdout.write('\n')
    sys.stdout.write(projScenes)
    '''
def zoobeRefreshProjectManUI():

    if(cmds.window('zoobePSettingsWin', exists=True)):
        cmds.deleteUI('zoobePSettingsWin')
    if(cmds.window('zoobeNewProjectWin', exists=True)):
        cmds.deleteUI('zoobeNewProjectWin')
    if(cmds.window('zoobePManWin', exists=True)):
        cmds.deleteUI('zoobePManWin')
        
    zoobeProjectMan()
    
def zoobeCancelNewProject():

    cmds.deleteUI('zoobeNewProjectWin')

def zoobeReadXML(name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
    os.chdir('C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\')#WORK
    #os.chdir('C:\\Users\\Dark Dragonlord\\Dropbox\\zoobe\\src\\test\\')#HOME
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            if(files == 'test.xml'):
                #file = md.parse("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")#WORK
				#file = md.parse("C:\\Users\\Dark Dragonlord\\Dropbox\\zoobe\\src\\test\\test.xml")#HOME
                #for line in file:
                #    if(line == 'zoobeprojects'):
                #        root_node = line
                #        print root_node.toxml()
                #root_node = file.documentElement
                #print root_node  
                file = parse("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")#WORK
				#file = md.parse("C:\\Users\\Dark Dragonlord\\Dropbox\\zoobe\\src\\test\\test.xml")#HOME
                zoobeGetProjectNode(file, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder)
            else:
                print 'No file found, creating a new Projects XML document!'
        else:
            print 'No XML Douments found, creating ane Projects XML document!'

def zoobeGetProjectNode(file, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
    projects = file.getElementsByTagName("project")
    #print projects
    zoobeGetPNames(file, projects, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder)

def zoobeGetPNames(file, projects, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
    doc = file#parse("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")
    for project in projects:
        nameXMLTag = project.getElementsByTagName("name")[0]
        eProj = "%s" % zoobeGetText(nameXMLTag.childNodes)
        if (len(eProj) == len(name)):
            if(eProj==name):
                print "Project name '" + name + "' already exists"
            else:
                zoobeAppendNewProject(doc, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder)

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
    
def zoobeGetText(nodelist):
    textArray = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            textArray.append(node.data)
    return ''.join(textArray)

def zoobeAppendNewProject(doc, name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
    
    projAttrs = ['path', 'description', 'status', 'date', 'deadline', 'version', 'mastername', 'masterformat','workshopname', 'workshopformat', 'camerafolder', 'conceptfolder', 'imagesfolder', 'texturesfolder', 'shadersfolder', 'datafolder', 'scenefolder']
    #newdoc = Document()
    root_node = doc.getElementsByTagName("zoobeprojects")[0]
    proj_node = doc.createElement("project")
    root_node.appendChild(proj_node)
    projName_node = doc.createElement("name")
    proj_node.appendChild(projName_node)
    projNameTxt=doc.createTextNode(name)
    projName_node.appendChild(projNameTxt)
    
    for attr in projAttrs:
        attr_node= doc.createElement(str(attr))
        proj_node.appendChild(attr_node)
        if(attr=='path'):
            newtext=doc.createTextNode(path + name+'/');
            attr_node.appendChild(newtext)
        if(attr=='description'):
            newtext=doc.createTextNode(description);
            attr_node.appendChild(newtext)
        if(attr=='status'):
            newtext=doc.createTextNode(status);
            attr_node.appendChild(newtext)
        if(attr=='date'):
            newtext=doc.createTextNode(date);
            attr_node.appendChild(newtext) 
        if(attr=='deadline'):
            newtext=doc.createTextNode(deadline);
            attr_node.appendChild(newtext)
        if(attr=='version'):
            newtext=doc.createTextNode(version);
            attr_node.appendChild(newtext)
        if(attr=='mastername'):
            newtext=doc.createTextNode(mastername);
            attr_node.appendChild(newtext)
        if(attr=='masterformat'):
            newtext=doc.createTextNode(masterformat);
            attr_node.appendChild(newtext)
        if(attr=='workshopname'):
            newtext=doc.createTextNode(workshopname);
            attr_node.appendChild(newtext)
        if(attr=='workshopformat'):
            newtext=doc.createTextNode(workshopformat);
            attr_node.appendChild(newtext)
        if(attr=='camerafolder'):
            newtext=doc.createTextNode(camerafolder);
            attr_node.appendChild(newtext)
        if(attr=='conceptfolder'):
            newtext=doc.createTextNode(conceptfolder);
            attr_node.appendChild(newtext)
        if(attr=='imagesfolder'):
            newtext=doc.createTextNode(imagesfolder);
            attr_node.appendChild(newtext)
        if(attr=='texturesfolder'):
            newtext=doc.createTextNode(texturesfolder);
            attr_node.appendChild(newtext)
        if(attr=='shadersfolder'):
            newtext=doc.createTextNode(shadersfolder);
            attr_node.appendChild(newtext)
        if(attr=='datafolder'):
            newtext=doc.createTextNode(datafolder);
            attr_node.appendChild(newtext)
        if(attr=='scenefolder'):
            newtext=doc.createTextNode(scenefolder);
            attr_node.appendChild(newtext)    
    
    openFile = open("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml", 'w')
    openFile.write(doc.toxml())
    openFile.close()
    zoobeCleanXML("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")
    
    zoobeCreateProjStruct(name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder)
    
def zoobeCreateProjXML(name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
    
    os.chdir('P:\\zoobeProjects\\')
    for files in os.listdir('.'):
        if files.endswith('.xml'):
            if(files == 'test.xml'):
                file = open("P:\\zoobeProjects\\test.xml")
                for line in file:
                    if(line == name):
                        break
                    else:
                        #file.close()
                        
                        doc = parse("P:/zoobeProjects/test.xml")
                        if(line == 'zoobeprojects'):
                            root_node = line
                            print root_node
                            break
                        #root_node = parseString('zoobeprojects')

                        #root_node = doc.getElementsByTagName('zoobeprojects')
                    file.close()       
                    '''    
                        projName = name
                        projAttr = ['path', 'description', 'status', 'date', 'deadline', 'version', 'mastername', 'masterformat','workshopname', 'workshopformat', 'camerafolder', 'conceptfolder', 'imagesfolder', 'texturesfolder', 'shadersfolder', 'datafolder', 'scenefolder']

                        proj_node = doc.createElement("project")
                        zoobeprojects.appendChild(proj_node)
                        projName_node = doc.createElement("name")
                        proj_node.appendChild(projName_node)
                        projNameTxt=doc.createTextNode(projName)
                        projName_node.appendChild(projNameTxt)
                            
                        for attr in projAttr:
                            attr_node= doc.createElement(str(attr))
                            proj_node.appendChild(attr_node)
                            if(attr=='path'):
                                newtext=doc.createTextNode(path + projName+'/');
                                attr_node.appendChild(newtext)
                            if(attr=='description'):
                                newtext=doc.createTextNode(description);
                                attr_node.appendChild(newtext)
                            if(attr=='status'):
                                newtext=doc.createTextNode(status);
                                attr_node.appendChild(newtext)
                            if(attr=='date'):
                                newtext=doc.createTextNode(date);
                                attr_node.appendChild(newtext) 
                            if(attr=='deadline'):
                                newtext=doc.createTextNode(deadline);
                                attr_node.appendChild(newtext)
                            if(attr=='version'):
                                newtext=doc.createTextNode(version);
                                attr_node.appendChild(newtext)
                            if(attr=='mastername'):
                                newtext=doc.createTextNode(mastername);
                                attr_node.appendChild(newtext)
                            if(attr=='masterformat'):
                                newtext=doc.createTextNode(masterformat);
                                attr_node.appendChild(newtext)
                            if(attr=='workshopname'):
                                newtext=doc.createTextNode(workshopname);
                                attr_node.appendChild(newtext)
                            if(attr=='workshopformat'):
                                newtext=doc.createTextNode(workshopformat);
                                attr_node.appendChild(newtext)
                            if(attr=='camerafolder'):
                                newtext=doc.createTextNode(camerafolder);
                                attr_node.appendChild(newtext)
                            if(attr=='conceptfolder'):
                                newtext=doc.createTextNode(conceptfolder);
                                attr_node.appendChild(newtext)
                            if(attr=='imagesfolder'):
                                newtext=doc.createTextNode(imagesfolder);
                                attr_node.appendChild(newtext)
                            if(attr=='texturesfolder'):
                                newtext=doc.createTextNode(texturesfolder);
                                attr_node.appendChild(newtext)
                            if(attr=='shadersfolder'):
                                newtext=doc.createTextNode(shadersfolder);
                                attr_node.appendChild(newtext)
                            if(attr=='datafolder'):
                                newtext=doc.createTextNode(datafolder);
                                attr_node.appendChild(newtext)
                            if(attr=='scenefolder'):
                                newtext=doc.createTextNode(scenefolder);
                                attr_node.appendChild(newtext)        
                                
    
                        xml_file = open("P:\\zoobeProjects\\test.xml", "a")
                        xml_file.write(doc.toprettyxml())
                        xml_file.close()
                    '''    
    '''
    file = open("P:\\zoobeProjects\\test.xml")
    for line in f:
        print line
    f.close()

    doc = Document()

    root_node = doc.createElement("zoobeprojects")
    doc.appendChild(root_node)

    projName = name
    projAttr = ['path', 'description', 'status', 'date', 'deadline', 'version', 'mastername', 'masterformat','workshopname', 'workshopformat', 'camerafolder', 'conceptfolder', 'imagesfolder', 'texturesfolder', 'shadersfolder', 'datafolder', 'scenefolder']

    proj_node = doc.createElement("project")
    root_node.appendChild(proj_node)
    projName_node = doc.createElement("name")
    proj_node.appendChild(projName_node)
    projNameTxt=doc.createTextNode(projName)
    projName_node.appendChild(projNameTxt)
        
    for attr in projAttr:
        attr_node= doc.createElement(str(attr))
        proj_node.appendChild(attr_node)
        if(attr=='path'):
            newtext=doc.createTextNode(path + projName+'/');
            attr_node.appendChild(newtext)
        if(attr=='description'):
            newtext=doc.createTextNode(description);
            attr_node.appendChild(newtext)
        if(attr=='status'):
            newtext=doc.createTextNode(status);
            attr_node.appendChild(newtext)
        if(attr=='date'):
            newtext=doc.createTextNode(date);
            attr_node.appendChild(newtext) 
        if(attr=='deadline'):
            newtext=doc.createTextNode(deadline);
            attr_node.appendChild(newtext)
        if(attr=='version'):
            newtext=doc.createTextNode(version);
            attr_node.appendChild(newtext)
        if(attr=='mastername'):
            newtext=doc.createTextNode(mastername);
            attr_node.appendChild(newtext)
        if(attr=='masterformat'):
            newtext=doc.createTextNode(masterformat);
            attr_node.appendChild(newtext)
        if(attr=='workshopname'):
            newtext=doc.createTextNode(workshopname);
            attr_node.appendChild(newtext)
        if(attr=='workshopformat'):
            newtext=doc.createTextNode(workshopformat);
            attr_node.appendChild(newtext)
        if(attr=='camerafolder'):
            newtext=doc.createTextNode(camerafolder);
            attr_node.appendChild(newtext)
        if(attr=='conceptfolder'):
            newtext=doc.createTextNode(conceptfolder);
            attr_node.appendChild(newtext)
        if(attr=='imagesfolder'):
            newtext=doc.createTextNode(imagesfolder);
            attr_node.appendChild(newtext)
        if(attr=='texturesfolder'):
            newtext=doc.createTextNode(texturesfolder);
            attr_node.appendChild(newtext)
        if(attr=='shadersfolder'):
            newtext=doc.createTextNode(shadersfolder);
            attr_node.appendChild(newtext)
        if(attr=='datafolder'):
            newtext=doc.createTextNode(datafolder);
            attr_node.appendChild(newtext)
        if(attr=='scenefolder'):
            newtext=doc.createTextNode(scenefolder);
            attr_node.appendChild(newtext)        
            
    xml_file = open("P:\\zoobeProjects\\test.xml", "w")
    xml_file.write(doc.toprettyxml())
    xml_file.close()
    '''

def zoobeCreateProjStruct(projName, projPath, projDescription, projStatus, projDate, projDeadline, projVersion, projMasterFiles, projMasterFormat, projWorkshopFiles, projWorkshopFormat, projCameras, projConcepts, projImages, projTextures, projShaders, projData, projScenes):
    
    #Makes main folder of project
    cmds.sysFile( projPath+projName, makeDir=True )
    #Make the inner structure (3 folders)
    cmds.sysFile( (projPath+projName+'/assets'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files'), makeDir=True )
    #Make the working_project structures with the specified folder names
    cmds.sysFile( (projPath+projName+'/working_project/'+projCameras), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projConcepts), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projImages+'/display_items'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projImages+'/zoobe_tt_template'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projTextures+'/textures'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projShaders), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projData+'/_incoming_data'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/_overlord'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/animations/animationstyle/startpose'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/animations/animationstyle/mo_cap/edited'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/animations/animationstyle/mo_cap/raw'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/display_items'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/geo'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/model'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/working_project/'+projScenes+'/rig'), makeDir=True )                                
    #Make the assets folder structures 
    cmds.sysFile( (projPath+projName+'/assets/cameras'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/characters'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/lights'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/stages'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/textures/characters'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/textures/logos'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/textures/props'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/textures/stages'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/assets/videos'), makeDir=True )
    #Make the master export files folder structures 
    cmds.sysFile( (projPath+projName+'/master_export_files/cameras'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/characters'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/lights'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/stages'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/textures/characters'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/textures/logos'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/textures/props'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/textures/stages'), makeDir=True )
    cmds.sysFile( (projPath+projName+'/master_export_files/videos'), makeDir=True )
    
    #Close the project creation options UI
    if(cmds.window('zoobeNewProjectWin', exists=True)):
        cmds.deleteUI('zoobeNewProjectWin')
    
    zoobeUpdateProjectList(projName)
    
def zoobeUpdateProjectList(name):

    cmds.textScrollList('projectsSelList', edit=True, append=name)
    
def zoobeNewAssetUI():

    if(cmds.window('zoobeNewAssetsWin', exists=True)):
        cmds.deleteUI('zoobeNewAssetsWin')
    if(cmds.windowPref('zoobeNewAssetsWin', exists=True)):
        cmds.windowPref('zoobeNewAssetsWin', edit=True, width=210, height = 80)
    
    zoobeNewAssetsWin = cmds.window('zoobeNewAssetsWin', width = 210, height = 80, title= 'New Asset Type')
    zoobeNewAssetsForm = cmds.formLayout('zoobeNewAssetsForm', nd=100)
    zoobeNewAssetText = cmds.text('zoobeNewAssetText', label='Type the name of the asset\n and press "Create"')
    zoobeNewAssetField = cmds.textField('zoobeNewAssetField', width = 200, text='')
    zoobeNewAssetBtn01 = cmds.button('zoobeNewAssetBtn01', width = 95, label='Create')
    zoobeNewAssetBtn02 = cmds.button('zoobeNewAssetBtn02', width = 95, label='Cancel', command="cmds.deleteUI('zoobeNewAssetsWin')")
    
    cmds.formLayout('zoobeNewAssetsForm', edit = True,
    
    af=[
    
    (zoobeNewAssetText, 'left', 40),
    (zoobeNewAssetText, 'top', 2),
    
    (zoobeNewAssetField, 'left', 5),
    (zoobeNewAssetField, 'top', 30),
    
    (zoobeNewAssetBtn01, 'left', 5),
    (zoobeNewAssetBtn01, 'top', 53),
    
    (zoobeNewAssetBtn02, 'left', 110),
    (zoobeNewAssetBtn02, 'top', 53),
    ])
    
    cmds.showWindow('zoobeNewAssetsWin') 
    
def zoobeCreateAssetType(assetName):

    print 'blah'