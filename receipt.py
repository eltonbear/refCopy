from os.path import split, exists
from io import open
from os import startfile

def makeReceiptTextFile(newXmlFilePath, xmlFolderPath, xmlFileName, refList, nameList, typeList):
	### name receipt file path 
	receiptName = xmlFileName + "_receipt.txt" 
	receiptPath = xmlFolderPath + "/" + receiptName
	
	### Creat receipt file and write in user inputs if xmlfolder is valid
	if exists(xmlFolderPath):
		receipt = open(receiptPath, "w")
		receipt.write("   Input XML File: " + xmlFolderPath + '/' + xmlFileName + '.xml' + '\n')
		receipt.write("Modified XML File: " + newXmlFilePath + '\n\n')
		receipt.write("Reference to Copy:     New Name:     Reference Type:\n")
		spaceS = ' '*7 + 'R'
		total = len(refList)
		for n in range(0, total):  
			### calculate space between type and wire number
			spaceR = ' '*(17-len(refList[n])) + 'R' 
			spaceN = ' '*(16-len(nameList[n]))	
			### write to file                                     													
			receipt.write(spaceS + refList[n] + spaceR  + nameList[n] + spaceN + typeList[n] + '\n')
		### Close file
		receipt.close()
		### Open receipt file as a window 
		startfile(receiptPath)
