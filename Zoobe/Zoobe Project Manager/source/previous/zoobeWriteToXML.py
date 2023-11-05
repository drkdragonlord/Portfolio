import sys
import os
from xml.dom.minidom import Document, parse, parseString, Element
import xml.dom.minidom as md
import maya.cmds as cmds
import maya.mel as mel
    
def zoobeWriteNewXML(name, path, description, status, date, deadline, version, mastername, masterformat, workshopname, workshopformat, camerafolder, conceptfolder, imagesfolder, texturesfolder, shadersfolder, datafolder, scenefolder):
	
    doc = Document()
	
    root_node = doc.createElement('zoobeprojects')
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
            newtext=doc.createTextNode(path + projName+'\\');
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

    xml_file = open("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml", "w")#WORK
    #xml_file = open("C:\\Users\\Dark Dragonlord\\Dropbox\\zoobe\\src\\test\\test.xml", "w")#HOME
    xml_file.write(doc.toxml(encoding='utf-8'))
    #toprettyxml(doc, 'utf-8')
    xml_file.close()
    zoobeCleanXML("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")  
    
def zoobeReadXML(name):
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
                zoobeGetProjectNode(file, name)
            else:
                print 'No file found, creating a new Projects XML document!'
        else:
            print 'No XML Douments found, creating ane Projects XML document!'

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
    
def zoobeGetProjectNode(file, newProjectName):
    projects = file.getElementsByTagName("project")
    print projects
    zoobeGetPNames(file, projects, newProjectName)
    #for line in file:
        #projects = file.getElementsByTagName("project")
        #print line

def zoobeGetText(nodelist):
    textArray = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            textArray.append(node.data)
    return ''.join(textArray)
    
def zoobeGetPNames(file, projects, newProjectName):
    doc = file#parse("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")
    for project in projects:
        name = project.getElementsByTagName("name")[0]
        eProj = "%s" % zoobeGetText(name.childNodes)
        if (len(eProj) == len(newProjectName)):
            if(eProj==newProjectName):
                print "Project name '" + newProjectName + "' already exists"
                break
            else:
                zoobeAppendNewProject(doc)
                '''
                root_node = doc.getElementsByTagName("zoobeprojects")[0]
                print zoobeprojects
                proj_node = doc.createElement("project")
                root_node.appendChild(proj_node)
                openFile = open("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml", 'w')
                openFile.write(doc.toxml(encoding='utf-8'))
                openFile.close()
                #openFile.write(doc.toxml(encoding='utf-8'))
                #toprettyxml(doc, 'utf-8')
                #openFile.close()
                zoobeCleanXML("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")
                '''
        else:
            continue
                
def zoobeAppendNewProject(doc):
    
    root_node = doc.getElementsByTagName("zoobeprojects")[0]
    proj_node = doc.createElement("project")
    root_node.appendChild(proj_node)
    openFile = open("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml", 'w')
    openFile.write(doc.toxml(encoding='utf-8'))
    openFile.close()
    zoobeCleanXML("C:\\Users\\Juan\\Dropbox\\zoobe\\src\\test\\test.xml")

                
        
                
                









