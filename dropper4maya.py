'''
Dropper
by Joseph Hocking www.newarteest.com
MIT license

written in Maya 2017
open in Script Editor window, then Execute

Saves info about objects in the scene:
name, position, rotation, scale, custom attributes
(ignore objects with ~[ somewhere in the name)
Select either XML or JSON for the data format.
'''


import maya.cmds as cmds
import json

# favor the accelerated C implementation, fallback to Python implementation
try:
	import xml.etree.cElementTree as et
except ImportError:
	import xml.etree.ElementTree as et
# http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree


def write_data(filepath, format):
    print("writing scene data...")
    
    data = {
        'OPT_JSON':build_json(),
        'OPT_XML':build_xml(),
    }[format]
    
    f = open(filepath, 'w')
    f.write(data)
    f.close()
#----- end func -----


def build_json():
    dict = {}
    dict["entities"] = []
    
    objects = cmds.ls(type="transform")
    for obj in objects:
        
        # ignore default cameras
        if (cmds.nodeType(cmds.listRelatives(obj, shapes=True)) == "camera" and
        (obj == "persp" or obj == "front" or obj == "side" or obj == "top")):
            continue
        
        if "~[" not in obj.name:
            entity = {"name":obj}
            pos = cmds.xform(obj, query=True, translation=True)
            entity["position"] = {"x":pos[0], "y":pos[1], "z":pos[2]}
            rot = cmds.xform(obj, query=True, rotation=True)
            entity["rotation"] = {"x":rot[0], "y":rot[1], "z":rot[2]}
            scl = cmds.xform(obj, query=True, scale=True, relative=True)
            entity["scale"] = {"x":scl[0], "y":scl[1], "z":scl[2]}
            # custom attributes
            attributes = cmds.listAttr(obj, userDefined=True)
            if (attributes != None):
                for attr in attributes:
                    entity[attr] = cmds.getAttr(obj+"."+attr)
            dict["entities"].append(entity)
        
    return json.dumps(dict, indent=4, sort_keys=True)
#----- end func -----


def build_xml():
    root = et.Element("entities")
    
    objects = cmds.ls(type="transform")
    for obj in objects:
        
        # ignore default cameras
        if (cmds.nodeType(cmds.listRelatives(obj, shapes=True)) == "camera" and
        (obj == "persp" or obj == "front" or obj == "side" or obj == "top")):
            continue
        
        if "~[" not in obj.name:
            e = et.Element("entity")
            et.SubElement(e, "name").text = obj
            pos = cmds.xform(obj, query=True, translation=True)
            et.SubElement(e, "position").attrib = {"x":str(pos[0]), "y":str(pos[1]), "z":str(pos[2])}
            rot = cmds.xform(obj, query=True, rotation=True)
            et.SubElement(e, "rotation").attrib = {"x":str(rot[0]), "y":str(rot[1]), "z":str(rot[2])}
            scl = cmds.xform(obj, query=True, scale=True, relative=True)
            et.SubElement(e, "scale").attrib = {"x":str(scl[0]), "y":str(scl[1]), "z":str(scl[2])}
            # custom attributes
            attributes = cmds.listAttr(obj, userDefined=True)
            if (attributes != None):
                for attr in attributes:
                    et.SubElement(e, attr).text = str(cmds.getAttr(obj+"."+attr))
            root.append(e)
        
    indent(root)
    return et.tostring(root).decode("utf-8")

#http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
#----- end func -----



#----- begin gui -----
class DropperWindow():
    
    def __init__(self):
        self.win = cmds.window("dropperOptionsWindow", title="Export Scene Data", widthHeight=(250, 100))
        cmds.columnLayout()
        
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Save JSON", command=self.onJsonClicked)
        cmds.text(label="JavaScript Object Notation")
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Save XML", command=self.onXmlClicked)
        cmds.text(label="eXtensible Markup Language")
        cmds.setParent("..")
        
        cmds.showWindow(self.win)
        
    def onJsonClicked(self, *args):
        self.saveClicked('OPT_JSON')
        
    def onXmlClicked(self, *args):
        self.saveClicked('OPT_XML')
        
    def saveClicked(self, format):
        cmds.deleteUI("dropperOptionsWindow")
        
        filepath = cmds.fileDialog2(fileMode=0)
        if (filepath == None):
            return
            
        write_data(filepath[0], format)
        
#----- end class -----


DropperWindow()
