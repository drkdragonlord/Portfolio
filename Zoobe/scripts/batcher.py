###############################################################################
#    Module:       batcher
#    Date:         17.05.2013
#    Author:       Oleg Solovjov    
#
#    Description:    Run selected python script on all files in directory.
#
#    Globals: 
#
#    Classes: 
#
#    Functions:
#
###############################################################################

###############################################
#import zoobeOgreExporter as ze
#reload(ze)
#import rig_v2.batcher as b
#reload(b)
#import rig_v2.exportAnimationToOgre as e
#reload(e)

#inDir='C:/zoobestar/tmp/source_animations'
#outDir='C:/zoobestar/tmp/source_animations/OUT'
#rigFileName='C:/zoobestar/tmp/bunny_basic__master_export_file_rig.mb'
#scriptName = 'C:/Users/oleg/workspace/zoobe/src/rig_v2/exportAnimationToOgre.py'
#filesToProcess = ['C:/zoobestar/tmp/source_animations/shy_pets_stand_exit_02_129.mb']
#br = b.Batcher(inDir=None, outDir=outDir, rigFileName=rigFileName, scriptName=scriptName,filesToProcess=filesToProcess)
#kwargs = {'frameRange':'timeline', 'bakeAnimation':True}
#br.setScriptKwargs(kwargs)
#br.run()


import os
import logging
import inspect

from PyQt4 import QtCore

import maya.cmds as mc
import maya.OpenMaya as OM


class Batcher(object):
    
    ANIM_RIG_SUFFIX = '_rig'
    SCRIPT_EXT = '.py'

    IGNORE_DIR_SUFFIX = '_IGNORE'
    FUNC_PREFIX = 'run_'

    def __init__(self, inDir=None, outDir=None, rigFileName=None, scriptName=None, logger=None, filesToProcess=None, doSaveFile=True):
        print '\n\n\n WORK THIS BATCHER \n\n\n'
        self.logger = self.setLogger(logger, outDir)

        self.fileList = None

        if filesToProcess:
            self.fileList = self.setFileList(filesToProcess)
        
        self.inDir = self.setInDir(inDir)

        if self.inDir:
            self.fileList = self.getFilesToProcess()
            
        self.outDir = self.setOutDir(outDir)
        self.rigFileName = self.setRigFileName(rigFileName)
        self.scriptName = self.setScriptName(scriptName)

        self.doSaveFile = doSaveFile
        self.scriptArgs = ( )
        self.scriptKwargs = {} 
        
        self.module = None
        self.func = None

        # signals for Qt progres bar
        self.pb = None
        self.batchDone = QtCore.pyqtSignal(bool)
        self.partBatchDone = QtCore.pyqtSignal(int)
        
        # CheckFileCallback for fixing bad character rig references
        self.logger.info("\n\n\naddCheckFileCallback was added.\n\n\n")
        self.checkFileCallbackId = OM.MSceneMessage.addCheckFileCallback(OM.MSceneMessage.kBeforeReferenceCheck, 
                                                                         Batcher.replaceRigRefCb,
                                                                         self)
    def __del__(self):
        ''' Clean up scene, remove callBacks. '''
        OM.MMessage.removeCallback(self.checkFileCallbackId)
        self.logger.info("addCheckFileCallback was deleted.\n\n\n")
        
    @staticmethod    
    def replaceRigRefCb(retCode, fileObject, b):
        ''' 
            CheckFileCallback for fixing bad character rig references.
            ClientData is batch exporter logger. 
        '''
        rf = fileObject.rawFullName()
        if os.path.basename(rf).find('_rig') > -1:
            b.logger.warning("\n\n\nMSG: Can't find rig file '%s' it would be resolved with '%s'.\n\n\n" % \
                                (rf, b.rigFileName))
            fileObject.setRawFullName(b.rigFileName)
            fileObject.overrideResolvedFullName(b.rigFileName)
            
        OM.MScriptUtil.setBool(retCode, True) 

    def run(self):
        ''' Run givien script on all files in given directory. '''
        fileNum = len(self.fileList)
        for i, f in enumerate(self.fileList):
            if self.pb:
                pbVal = float(i)/float(fileNum) * 100.0
                self.pb.setValue(int(pbVal))
                #self.partBatchDone.emit(pbVal)
                #self.batchDone.emit(True)
                
            of = self.composeOutFile(f)
            self.openMayaFile(f)
            self.runScript(of)
            if self.doSaveFile:
                self.saveMayaFile(of)
                
        self.pb.setValue(100)

    def runScript(self, of):
        m = os.path.basename(self.scriptName).replace('.py', '')
        
        mod = __import__("rig_v2." + m, {}, {}, [m])
        reload(mod)
        
        funcList = []
        for n, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__name__.find(Batcher.FUNC_PREFIX) > -1: 
                funcList.append(o)

        for f in funcList:
            self.logger.info("Running function '%s()'" % f.__name__)
            args = (of)
            f(of, **self.scriptKwargs)

    def composeOutFile(self, f):
        return self.outDir + '/' + os.path.basename(f)
        
    def setScriptKwargs(self, kwargs):  
        self.scriptKwargs = {}
        self.scriptKwargs.update(kwargs)

    def setScriptArgs(self, *args):
        self.scriptArgs = args
        print self.scriptArgs
        
    def setProgressBarWidget(self, pb):
        ''' Set Qt progress bar widget. '''
        self.pb = pb
        
    ###############################################################################
    #
    #    Files and directories
    #
    ############################################################################### 
    def setInDir(self, d):
        if self.fileList:  # got files to process, no need in input directory
            return d
        
        if d is None or not os.path.isdir(d):
            msg = "Can't find given input directory '%s'." % d
            self.logger.error(msg)
            raise NameError, msg
        
        return d

    def setFileList(self, filesToProcess):
        for f in filesToProcess:
            if not os.path.isfile(f):
                msg = "Can't find given file '%s' from files to process list." % f
                self.logger.error(msg)
                raise NameError, msg

        from copy import deepcopy
        
        return deepcopy(filesToProcess)
        
    def setOutDir(self, d):
        if d is None or not os.path.isdir(d):
            msg = "Can't find given output directory '%s'." % d
            self.logger.error(msg)
            raise NameError, msg
        
        return d
    
    def setScriptName(self, f):
        if f is None or not Batcher.isScriptFile(f):
            msg = "Can't find given script file '%s'." % f
            self.logger.error(msg)
            raise NameError, msg
        
        return f

    def setRigFileName(self, rigFileName):
        if rigFileName is None or len(rigFileName) == 0:
            return None
        
        if not os.path.isfile(rigFileName):
            msg = "Can't find given rig file '%s'." % rigFileName
            self.logger.error(msg)
            raise NameError, msg

        if not Batcher.isRig(rigFileName):
            msg = "Given file '%s' isn't rig file." % rigFileName
            self.logger.error(msg)
            raise NameError, msg
        
        return rigFileName
    
    def openMayaFile(self, inFile):
        if not os.path.isfile(inFile):
            msg = "Can't find file %s." % inFile
            self.logger.error(msg)
            raise NameError, msg

        self.logger.info("Opening maya file '%s'" % inFile)
        
        # Open file 
        mc.file( force=True, new=True, iv=True ) # file/new for clean up
        try:
            mc.file( inFile, o=True, force=True, iv=True)
        except (RuntimeError, TypeError, NameError):
            msg = "Can't open given file %s." % inFile
            self.logger.error(msg)
            raise NameError, msg

    def saveMayaFile(self, f):
        try:
            self.logger.info("Saving maya file '%s'" % f)
            mc.file(rn=f)
            mc.file(f=True, iv=True, save=True, type='mayaBinary')
        except (RuntimeError, TypeError, NameError):
            msg = "Can't save given file %s." % f
            self.logger.error(msg)
            raise NameError, msg
        
    @staticmethod
    def isMayaFile(f):
        ''' Return true if given file is valid Maya filr, otherwise false. '''
        if f is None or not os.path.isfile(f):
            return False
        
        _, ext = os.path.splitext(f)
        if not ext == '.mb':
            return False
        
        return True
    
    @staticmethod
    def isRig(f):
        ''' Return true if given file is valid Maya rig, otherwise false. '''
        
        #if not Batcher.isMayaFile(f) and os.path.basename(f).find(Batcher.ANIM_RIG_SUFFIX) < 0:
        if not Batcher.isMayaFile(f):
            return False      
        
        return True

    @staticmethod
    def isScriptFile(f):
        ''' Return true if given file is valid python script, otherwise false. '''
        if f is None or not os.path.isfile(f):
            return False

        _, ext = os.path.splitext(f)
        if not ext == Batcher.SCRIPT_EXT:
            return False

        return True
    
    def getFilteredFileList(self, d, filterFunc):
        ''' Get all files in given directory. '''
        if d is None or not os.path.isdir(d):
            msg = "Can't find given directory '%s'." % d
            self.logger.error(msg)
            raise NameError, msg
        
        resultList = []
        for f in os.listdir(d):
            f = d + '/' + f
            if os.path.isfile(f):
                if filterFunc(f):
                    resultList.append(f.replace('\\', '/'))
        
        
        return resultList

    def getFilesToProcess(self):
        return self.getFilteredFileList(self.inDir, self.isMayaFile)
    
    ###############################################################################
    #
    #    References
    #
    ###############################################################################
     
    @staticmethod
    def getRefFileList():
        ''' Return list of referenced files or empty list.'''
        return mc.file(q=True, r=True, withoutCopyNumber=False)     
     
    def getFirstAnimRigReference(self):
        ''' Return first animation rig reference file name or None.'''
        for f in Batcher.getRefFileList():
            if Batcher.isRig(f):
                return f

        msg = "Can't find referensed animation rig in scene '%s'." % mc.file(q=True, sn=True)
        self.logger.error(msg)
        return None
    
    @staticmethod
    def getRefNodeFromRefFileName(fileName):
        ''' Return Maya reference node from given referenced file name. '''
        return mc.file(fileName, q=True, rfn=True)
        
    def replaceReference(self, refNode, f):
        if f is None or not os.path.isfile(f):
            msg = "Can't find given file '%s' for replace reference." % f
            self.logger.error(msg)
            raise NameError, msg
        
        mc.file(f, loadReference=refNode, type='mayaBinary')

    ###############################################################################
    #
    #    Logger
    #
    ############################################################################### 
    def setLogger(self, logger, outDir):
        if not os.path.isdir(outDir):
            raise NameError, "Can't find output directory '%s'." % outDir
        if not logger:
            print "Create new logger for batch process." 
            logFileName = outDir + '/BatchLogger.log'
            logger = Batcher.createLogger('BatchLogger', logFileName)
            
        return logger
    
    @staticmethod
    def createLogger(loggerName, logFileName):
        ''' Create rotating file logger. '''
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(logFileName)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger 
