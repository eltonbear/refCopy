from os.path import split, exists
from io import open
from os import startfile

def makeReceiptTextFile(newXmlFilePath, xmlFilePath, xmlFolderPath, xmlFileName, refList, typeList, depList, wireList):
	### name receipt file path 
	receiptName = xmlFileName + "_receipt.txt" 
	receiptPath = xmlFolderPath + "/" + receiptName
	
	### Creat receipt file and write in user inputs if xmlfolder is valid
	if exists(xmlFolderPath):																	### chekc if they are the same
		receipt = open(receiptPath, "w")
		receipt.write("Input XML File: " + xmlFilePath + '\n')
		receipt.write("  New XML File: " + newXmlFilePath + '\n\n')
		receipt.write("Reference number to copy:	Reference Type:		Depends on Reference:	 Wire numbers assigned to new copy:\n")
		space10 = "          "
		for n in range(0, len(refList)):  
			### calculate space between type and wire number
			spaceR = ' '*(26-len(refList[n]))
			spaceT = ' '*(28-len(typeList[n]))
			spaceD = ' '*(25-len(depList[n]))
			### write to file                                     													
			receipt.write(space10 + refList[n] + spaceR  + typeList[n] + spaceT + depList[n] + spaceD + ",".join(wireList[n]) + '\n')
		### Close file
		receipt.close()
		### Open receipt file as a window 
		startfile(receiptPath)
