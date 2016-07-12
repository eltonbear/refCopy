import interfaceV2
import browseInterface
from xmlInfo import makeXMLInfoTextFile
from receipt import makeReceiptTextFile
from tkinter import *
import xml.etree.ElementTree as ET
from xmlModifier import modifier


window1 = Tk()
browse = browseInterface.browse(window1)
window1.mainloop()
fFormat = True
if browse.isOk:
	try:
		tree = ET.parse(browse.filePath)                                    
	except ET.ParseError:                       
		browse.fileFormatIncorrectWarning()
		fFormat = False

	root = tree.getroot() 
	referenceE = root.findall('ReferenceSystem')
	wireE = root.findall('Wire')
	if not referenceE or not wireE:
		browse.fileFormatIncorrectWarning()
		fFormat = False 

	if fFormat:
		makeXMLInfoTextFile(browse.filePath, browse.xmlFolderPath, browse.xmlFileName, referenceE, wireE)
		window2 = Tk()
		GUI = interfaceV2.App(window2, None)
		window2.mainloop()

		if GUI.isOk:
			print("copy: " + str(GUI.refs))
			print("Name: " + str(GUI.names))
			print("Type: " + str(GUI.types))
			print("In main folder path: " + browse.xmlFolderPath + '\n')
			# xmlFilePathNew = modifier(browse.filePath, browse.xmlFolderPath, browse.xmlFileName, GUI.refs, GUI.types, GUI.deps, GUI.wires, referenceE, wireE, tree)
			makeReceiptTextFile(None, browse.xmlFolderPath, browse.xmlFileName, GUI.refs, GUI.names, GUI.types)
			
	print("end of code")



