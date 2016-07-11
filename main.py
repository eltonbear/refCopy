import interfaceV1
from receipt import makeReceiptTextFile
from tkinter import *
from xmlModifier import modifier

window = Tk()
GUI = interfaceV1.App(window)
window.mainloop()
print("ref to copy: ")
print(GUI.refs)
print("Type: ")
print(GUI.types)
print("Dep: ")
print(GUI.deps)
print("wires: ")
print(GUI.wires)
print("In Main FOLDER PATH: " + GUI.xmlFolderPath +'\n\n')

if GUI.isOk:
	print("In If statement")
	XmlFilePathNew = modifier(GUI.filePath, GUI.xmlFolderPath, GUI.xmlFileName, GUI.refs, GUI.types, GUI.deps, GUI.wires)
	makeReceiptTextFile(XmlFilePathNew, GUI.filePath, GUI.xmlFolderPath, GUI.xmlFileName, GUI.refs, GUI.types, GUI.deps, GUI.wires)
	
print("end of code")