from io import open
from os import startfile
from os.path import exists
import re
from os.path import split, splitext

def makeXMLInfoTextFile(xmlFilePath, xmlFolderPath, xmlFileName, referenceE, wireE):
	### name Info file path 
	if xmlFileName[-1].isdigit():
		infoName = xmlFileName[0:-5] + "_info.txt"
	else:
		infoName = xmlFileName + "_info.txt" 
	infoPath = xmlFolderPath + "/" + infoName
	
	### Creat Info file and write if xmlfolder is valid
	if exists(xmlFolderPath):
		latestRefName = [] #str
		refNameGap = [] #int
		repeat = []
		numOfwire = len(wireE)
		numOfRef = len(referenceE)

		### obtain gaps
		for i in range(0, numOfRef):
			numberS = re.findall('\d+', referenceE[i].find('Name').text)[0]
			if i > 0:
				latestRefName.append(numberS)
				currNum = int(numberS)
				if currNum - prevNum > 1:
					if prevNum + 1 == currNum - 1:
						refNameGap.append([prevNum + 1])
					else:
						refNameGap.append([prevNum + 1, currNum - 1])
				prevNum = currNum
			else:
				latestRefName.append(numberS)
				prevNum = int(numberS)
		
		### check if there is any repeating names
		singles = set(latestRefName)
		for s in singles:
			count = latestRefName.count(s)
			if count > 1:
				repeat.append([s, count])

		### write info
		originalRefName = writeText(infoPath, xmlFilePath, repeat, latestRefName, refNameGap, numOfwire, numOfRef)
		### Open Info file as a window 
		startfile(infoPath)
		print("og: " + str(originalRefName))
	return originalRefName, latestRefName

def writeText(InfoFilePath, xmlFilePath, repRef, lRefName, refGap, numW, numR):
	space90 = "@"*90
	space110 = "@"*110 

	if exists(InfoFilePath):
		infoR = open(InfoFilePath, 'r+')
		for i, line in enumerate(infoR):
			if i == 1:
				ogRefName = line[1:-3].split(",")
				break
		infoR.close() 
		info = open(InfoFilePath, 'a')
	else:
		ogRefName = list(map(int, lRefName))
		info = open(InfoFilePath, "w")
		info.write(space110 + '\n')
		info.write(str(ogRefName) + '\n')
		info.write(space110 + '\n')

	info.write(space90 + '\n')
	### write file path		
	info.write("#Input XML File: " + xmlFilePath + '\n\n')
	### write repeating ref name if there is any
	info.write("#Repeating Reference:\n")
	if repRef:
		for r in repRef:
			info.write("There are " + str(r[1]) + " R" + r[0] + '\n')
	else:
		info.write("None\n")
	### write first and last ref name
	info.write("\n#First Reference: R" + lRefName[0] + '\n')
	info.write("#Last Reference:  R" + lRefName[numR-1] + '\n')
	### write refernce gaps
	info.write("\n#Range of Gaps (included):\n")
	if refGap:
		for g in refGap:
			if len(g) == 1:
				info.write("R" + str(g[0]) + '\n')
			else:
				info.write("R" + str(g[0]) + ' - R' + str(g[1]) + '\n')
	else:
		info.write("None\n")
	info.write("\n#Number of Wires: " + str(numW) + "\n")
	info.write('\n' + space90 + '\n')

	### Close file
	info.close()
	return ogRefName
	

# p = "C:/Users/eltoshon/Desktop/programTestiing/xmltest1.xml"
# tree = ET.parse(p)                                                     
 
# root = tree.getroot()
# referenceE = root.findall('ReferenceSystem')
# wireE = root.findall('Wire')

# makeXMLInfoTextFile(p, r"C:\Users\eltoshon\Desktop\programTestiing", "xmltest1", referenceE, wireE)
