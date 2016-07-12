import interfaceV2
import browseInterface
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

	if fFormat:
		root = tree.getroot()
		referenceE = root.findall('ReferenceSystem')
		wireE = root.findall('Wire')
		numOfRef = len(referenceE)
		numOfWire = len(wireE)
		print("num of ref = " + str(numOfRef))
		print("num of wire = " + str(numOfWire) + '\n')
		window2 = Tk()
		GUI = interfaceV2.App(window2, SOMETHING)
		window2.mainloop()

		if GUI.isOk:
			print("copy: " + str(GUI.refs))
			print("Type: " + str(GUI.types))
			print("Dep: " + str(GUI.deps))
			print("wires: " + str(GUI.wires))
			print("In main folder path: " + browse.xmlFolderPath + '\n')
			xmlFilePathNew = modifier(browse.filePath, browse.xmlFolderPath, browse.xmlFileName, GUI.refs, GUI.types, GUI.deps, GUI.wires, referenceE, wireE, tree)
			makeReceiptTextFile(xmlFilePathNew, browse.filePath, browse.xmlFolderPath, browse.xmlFileName, GUI.refs, GUI.types, GUI.deps, GUI.wires)
			
	print("end of code")



