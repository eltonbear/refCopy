from io import open
from os import startfile
from os.path import exists
import re

import xml.etree.ElementTree as ET ###

def makeXMLInfoTextFile(xmlFilePath, xmlFolderPath, xmlFileName, referenceE, wireE):
	### name Info file path 
	infoName = xmlFileName + "_info.txt" 
	infoPath = xmlFolderPath + "/" + infoName
	
	### Creat Info file and write if xmlfolder is valid
	if exists(xmlFolderPath):
		refName = [] #str
		refNameGap = [] #int
		repeat = []
		numOfwire = len(wireE)
		numOfRef = len(referenceE)

		### obtain gaps
		for i in range(0, numOfRef):
			numberS = re.findall('\d+', referenceE[i].find('Name').text)[0]
			if i > 0:
				refName.append(numberS)
				currNum = int(numberS)
				if currNum - prevNum > 1:
					if prevNum + 1 == currNum - 1:
						refNameGap.append([prevNum + 1])
					else:
						refNameGap.append([prevNum + 1, currNum - 1])
				prevNum = currNum
			else:
				refName.append(numberS)
				prevNum = int(numberS)
		
		### check if there is any repeating names
		singles = set(refName)
		for s in singles:
			count = refName.count(s)
			if count > 1:
				repeat.append([s, count])

		# print(refName)
		# print(refNameGap)
		# print(singles)
		# print(repeat)
		info = open(infoPath, "w")

		### write file path		
		info.write("#XML File: " + xmlFilePath + '\n\n')

		### write repeating ref name if there is any
		info.write("#Repeating Reference:\n")
		if repeat:
			for r in repeat:
				info.write("There are " + str(r[1]) + " R" + r[0] + '\n')
		else:
			info.write("None\n")

		### write first and last ref name
		info.write("\n#First Reference: R" + refName[0] + '\n')
		info.write("#Last Reference:  R" + refName[numOfRef-1] + '\n')

		### write refernce gaps
		info.write("\n#Range of Gaps (included):\n")
		if refNameGap:
			for g in refNameGap:
				if len(g) == 1:
					info.write("R" + str(g[0]) + '\n')
				else:
					info.write("R" + str(g[0]) + ' - R' + str(g[1]) + '\n')
		else:
			info.write("None\n")

		info.write("\n#Number of Wires: " + str(numOfwire) + "\n")

		### Close file
		info.close()
		### Open Info file as a window 
		startfile(infoPath)
	return refName


# p = "C:/Users/eltoshon/Desktop/programTestiing/xmltest1.xml"
# tree = ET.parse(p)                                                     
 
# root = tree.getroot()
# referenceE = root.findall('ReferenceSystem')
# wireE = root.findall('Wire')

# makeXMLInfoTextFile(p, r"C:\Users\eltoshon\Desktop\programTestiing", "xmltest1", referenceE, wireE)
