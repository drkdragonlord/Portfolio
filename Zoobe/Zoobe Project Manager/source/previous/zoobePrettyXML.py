import sys
import os
from lxml import etree
import maya.cmds as cmds
import maya.mel as mel

def zoobePrettyXML(name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):

    root_node = etree.Element('zoobeprojects')
    print (root_node.tag)