import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement

def modifier(xmlFilePath, xmlFolderPath, xmlFileName, refList, typeList, depList, wireList):
	### make a ElementTree object and find its root (highest node)
	tree = ET.parse(xmlFilePath)                                                     ######### nothing is entered????
	root = tree.getroot()
	### make two lists of all reference elements(objects) and wire elements(objects)
	referenceE = root.findall('ReferenceSystem')
	wireE = root.findall('Wire')
	numOfRef = len(referenceE)
	numOfWire = len(wireE)
	for n in range(0, len(refList)):
		### Create reference(copy) with according names, types, and dependency
		### And insert them after the last referenceSystem if ref entry is not empty
		if refList[n]:
			for r in referenceE:
				if refList[n] == r.find('Name').text:
					copy = writeARefCopy(r, numOfRef + 1, typeList[n], depList[n])
					root.insert(numOfRef, copy)
					numOfRef += 1
					break

		### change wire's ref information		
		modifyWireRefInfo(wireList[n], refList[n], str(numOfRef), wireE)

	### write to a new xml file
	newXmlFilePath = xmlFolderPath + "/" + xmlFileName + "_new.xml"
	tree.write(newXmlFilePath)
	return newXmlFilePath

def writeARefCopy(refToCopy, nameOfRef, typ, dependon):
	### creat new referenceSystem node
	newRef = Element('ReferenceSystem')
	newName = SubElement(newRef, 'Name')
	newName.text = str(nameOfRef)
	newType = SubElement(newRef, 'Type')
	newType.text = typ
	####################################### 									can depend be empty? is it the same as the original ?
	newDep = SubElement(newRef, 'Dependon')
	newDep.text = dependon
	#######################################
	### creat two nodes that refer to original points objects(elements)
	for p in refToCopy.findall('Point'):
		newRef.append(p)
	### formatting xml text so it prints nicly 
	indent(newRef, 1)
	### return the reference(address) of the ref element
	return newRef

def modifyWireRefInfo(listOfWires, oldRefWireWasOn, newRefWireAssignedTo, wireElement):
	wireToEdit = list(map(int, listOfWires))
	print("old: " + oldRefWireWasOn)
	print("new: " + newRefWireAssignedTo +'\n') ###### wire can not be more than num of wireelement
	for wire in wireToEdit:
		print("wire number: " + str(wire))
		for bond in wireElement[wire-1].findall('Bond'):
			print("wire's ref num: " + bond.find('Refsys').text)
			if bond.find('Refsys').text == oldRefWireWasOn:
				bond.find('Refsys').text = newRefWireAssignedTo
				print("changed to: " + bond.find('Refsys').text)
			else:
				print("no changes")
		print("\n")

### in-place prettyprint formatter found online --> http://effbot.org/zone/element-lib.htm#prettyprint 
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i















	

