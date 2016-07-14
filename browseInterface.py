from tkinter import *
from tkinter.filedialog import askopenfilename
from os.path import isfile, split, splitext

class browse(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, width = 1000)
		self.parent = parent
		self.filePath = ""
		self.ogFilePath = ""
		self.xmlFolderPath = ""
		self.xmlFileName = "" # with no extension
		self.filePathEntry = None
		self.isOk = False
		self.initGUI()

	def initGUI(self):
		self.parent.title("Reference Copying")
		self.pack(fill = BOTH, expand = True)

		self.entryFrame = Frame(self, relief = RAISED, borderwidth = 1)
		self.entryFrame.pack(fill = BOTH, expand = True)
		self.makeButtons()

		self.filePathEntry = Entry(self.entryFrame, bd = 4, width = 50)
		self.filePathEntry.grid(row = 0, column = 2, columnspan = 5, padx=2, pady=2)

	def makeButtons(self):
		### Create buttons for Cancel, Ok, and Browse and set their positions
		bCancel = Button(self, text = "Cancel", width = 10 ,command = self.closeWindow)
		bCancel.pack(side = RIGHT,padx=5, pady=2)
		bOk = Button(self, text = "Ok", width = 5, command = self.OK)
		bOk.pack(side = RIGHT, padx=5, pady=2)
		bBrowse = Button(self.entryFrame, text = "Browse", width = 10, command = self.getFilePath)
		bBrowse.grid(row = 0, column = 1, padx=3, pady=3)

	def getFilePath(self):
		self.filePath = askopenfilename(filetypes = (("XML files", "*.xml"), ("TXT files", "*.txt"), ("All files", "*.*")))
		self.filePathEntry.delete(0, 'end')
		self.filePathEntry.insert(0, self.filePath)

	def closeWindow(self):
		self.parent.destroy()

	def OK(self):
		### Command when Ok button is clicked	
		self.filePath = self.filePathEntry.get()						
		if self.filePath == "":
			self.emptyFileNameWarning()
		elif not isfile(self.filePath):
			self.incorrectFileNameWarning()
		else:
			self.isOk = True
			self.getFolderAndFileName()	
			self.closeWindow()

	def getFolderAndFileName(self):
		self.xmlFolderPath, self.xmlFileName = split(self.filePath)
		self.xmlFileName = splitext(self.xmlFileName)[0]

	def incorrectFileNameWarning(self):
		messagebox.showinfo("Warning", "File does not exist!")

	def emptyFileNameWarning(self):
		messagebox.showinfo("Warning", "No files selected!")

	def fileFormatIncorrectWarning(self):
		messagebox.showinfo("Warning", "File: " + self.xmlFileName + " - format incorrect!")

	def originalXmlFileMissing(self, ogFileName):
		messagebox.showinfo("Warning", "original XML file - " + ogFileName + " Missing!")