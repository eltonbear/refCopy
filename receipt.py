from os.path import split, exists
from io import open
from os import startfile

def makeReceiptTextFile(newXmlFilePath, xmlFilePath, xmlFolderPath, xmlFileName, refList, typeList, depList, wireList):
	### name receipt file path 
	receiptName = xmlFileName + "_receipt.txt" 
	receiptPath = xmlFolderPath + "/" + receiptName
	
	### Creat receipt file and write in user inputs if xmlfolder is valid
	if exists(xmlFolderPath):
		receipt = open(receiptPath, "w")
		receipt.write("   Input XML File: " + xmlFilePath + '\n')
		receipt.write("Modified XML File: " + newXmlFilePath + '\n\n')
		receipt.write("Reference Number:     Copy of Reference:     Reference Type:     Depends on Reference:     Wire Assigned to Copy:\n")
		spaceS = ' '*6
		total = len(refList)
		for n in range(0, total):  
			### calculate space between type and wire number
			newRefNum = total + n + 1
			spaceN = ' '*(23-len(str(newRefNum)))
			spaceR = ' '*(21-len(refList[n]))
			spaceT = ' '*(23-len(typeList[n]))
			spaceD = ' '*(23-len(depList[n]))			
			### write to file                                     													
			receipt.write(spaceS + str(newRefNum) + spaceN + refList[n] + spaceR  + typeList[n] + spaceT + depList[n] + spaceD + ",".join(wireList[n]) + '\n')
		### Close file
		receipt.close()
		### Open receipt file as a window 
		startfile(receiptPath)
