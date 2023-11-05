import maya.cmds as mc
import maya.mel as mel
import os

def exportAnimationToOgre(filename, frameRange="timeline"):
    start = end = 0
    if frameRange=="timeline":
        start = mc.playbackOptions(q=1, min=1)
        end   = mc.playbackOptions(q=1, max=1)
    else:
        start = mc.currentTime( q=1)
        end = start+1

    path = os.path.split(filename)
    ext = os.path.splitext(path[1])
    options = ""
    
    #if we have a selection export that else export everything
    selection = mc.ls( sl=1)
    if not selection: options += " -all"
    #options += " -all"

    #run export command
    options += ' -skeletonClip "%s" startEnd %d %d frames sampleByFrames %d' % (ext[0],start,end,1)
    options = " -outDir \"" + path[0] +"/\"" + options
    options += " -lu pref -scale 1.00 -skeletonAnims -skelBB -np bindPose"
    options = options.replace( "/", "\\\\")

    mel.eval('doEnableNodeItems false all')
    
    dagPoses_pre = mc.ls(type="dagPose")
    try:
        mel.eval( "ogreExport"+options)
    except:
        mc.confirmDialog( title='Error', message='Export failed! See command window log for more infos...', button=['Ok'], defaultButton='Ok')
    dagPoses_post = mc.ls(type="dagPose")
    for pose in dagPoses_post:
        if( pose not in dagPoses_pre):
            print("Delete Pose: %s" % pose)
            mc.delete(pose)

    mel.eval('doEnableNodeItems true all')

def exportPoseToOgre(filename):
   exportAnimationToOgre(filename, "frame")

# for batcher
def run_exportAnimationToOgre(*args, **kwargs):
    exportAnimationToOgre(*args, **kwargs)
