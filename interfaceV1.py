from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from os.path import isfile, split, splitext

class App(Frame):

	def __init__(self, parent):

		Frame.__init__(self, parent)
		self.isOk = False
		self.allEmpty = True
		self.parent = parent
		self.filePath = ""
		self.xmlFolderPath = ""
		self.xmlFileName = "" # with no extension
		self.refs = []
		self.types = []
		self.deps = []
		self.wires = []
		self.refEntries = []
		self.typeEntries = []
		self.depEntries = []
		self.wireEntries = [] # a list of lists
		self.x = 1
		self.y = 1
		self.entryFrame = None
		self.filePathEntry = None
		self.initGUI()
		
	def initGUI(self):
		self.parent.title("Reference Copying")
		### creat a frame for entries
		self.entryFrame = Frame(self, relief = RAISED, borderwidth = 1)
		self.entryFrame.pack(fill = BOTH, expand = True)
		self.pack(fill = BOTH, expand = True)
		self.makeButtons()
		self.addEntry()
		self.filePathEntry = Entry(self, bd = 5)
		self.filePathEntry.pack(side = LEFT, fill = X, expand = True, padx=3, pady=5)
		# self.filePathEntry.grid(row = 1, column = 2)

		
	def addEntry(self):
		### using grid for entries' positions
		### Ref entry
		Label(self.entryFrame, text = "Reference Number: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Er = Entry(self.entryFrame, bd = 5)
		Er.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.refEntries.append(Er)
		self.y += 1

		# ### Type entry
		Lt = Label(self.entryFrame, text = "Reference Type: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Et = Entry(self.entryFrame, bd = 5)
		Et.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.typeEntries.append(Et)
		self.y += 1

		### Dep entry
		Ld = Label(self.entryFrame, text = "Depends on Ref: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Ed = Entry(self.entryFrame, bd = 5)
		Ed.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.depEntries.append(Ed)
		self.y += 1

		### Wire entry
		Lw = Label(self.entryFrame, text = "Wire Numbers: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Ew = Entry(self.entryFrame, bd = 5)
		Ew.grid(row = self.x, column = self.y%8+8, padx=5 , pady=5)
		self.wireEntries.append(Ew)
		self.y += 1
		
		### increment
		self.x = self.x + 1 

	def closeWindow(self):
		self.parent.destroy()

	def makeButtons(self):
		### Create buttons for Cancel, Add, Ok, and Browse and set their positions
		bCancel = Button(self, text = "Cancel", width = 10,command = self.closeWindow)
		bCancel.pack(side = RIGHT,padx=5, pady=5)
		bAdd = Button(self, text = "Add", width = 7, command = self.addEntry)
		bAdd.pack(side = RIGHT, padx=5, pady=5)
		bOk = Button(self, text = "Ok", width = 5, command = self.OK)
		bOk.pack(side = RIGHT, padx=5, pady=5)
		bBrowse = Button(self, text = "Browse", width = 10, command = self.getFilePath)
		bBrowse.pack(side = LEFT, padx=5, pady=5)

	def OK(self):
		### Command when Ok button is clicked	
		self.filePath = self.filePathEntry.get()						
		if self.filePath == "":
			self.emptyFileNameWarning()
		elif not isfile(self.filePath):
			self.incorrectFileNameWarning()
		elif self.getContent():
			self.getFolderAndFileName()
			self.isOk = True
			self.closeWindow()
						
	def getContent(self): 												################### check format---> needs to be number?
		### get inputs in ref, type, dependon, and wire entries. Return ture if successfully get content.
		for num in range(0, len(self.refEntries)):
			ref = self.refEntries[num].get()
			typ = self.typeEntries[num].get()
			dep = self.depEntries[num].get()
			wireList = self.wireEntries[num].get().split(",")
			for n in range(0, len(wireList)):
				wireList[n] = wireList[n].strip()

			if self.appendLists(num + 1, ref, typ, dep, wireList):
				self.refs = []
				self.types = []
				self.deps = []
				self.wires = []
				return False

		if self.allEmpty:
			self.allEntriesEmptyWarning()
			return False

		return True

	def getFilePath(self):
		self.filePath = askopenfilename(filetypes = (("XML files", "*.xml"), ("TXT files", "*.txt"), ("All files", "*.*")))
		self.filePathEntry.delete(0, 'end')
		self.filePathEntry.insert(0, self.filePath)

	def getFolderAndFileName(self):
		self.xmlFolderPath, self.xmlFileName = split(self.filePath)
		self.xmlFileName = splitext(self.xmlFileName)[0]

	def appendLists(self, row, ref, typ, dep, wire):
		'''Append to ref, type, dep, and wire list if no entries is emtpy. 
		   Return true if there is any entries missing. All missing is not missing'''
		if ref and typ and wire[0]:
			self.refs.append(ref)
			self.types.append(typ)
			self.deps.append(dep)
			self.wires.append(wire) 
			self.allEmpty = False
			return False # other three exist(dep does not matter)
		elif (not dep) and (not ref) and (not typ) and (not wire[0]):
			return False # all missing
		elif not ref:
			self.refEntryMissingWarning(row)
			return True 
		elif not typ:
			self.typeEntryMissingWarning(row)
			return True
		elif not wire[0]:
			self.wireEntryMissingWarning(row)
			return True

	### Warnings
	def refEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number is missing!")

	def typeEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", type is missing!")

	def wireEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", wire number(s) is missing!")

	def incorrectFileNameWarning(self):
		messagebox.showinfo("Warning", "File does not exist!")

	def emptyFileNameWarning(self):
		messagebox.showinfo("Warning", "No files selected!")

	def allEntriesEmptyWarning(self):
		messagebox.showinfo("Warning", "Nothing is inputted")



