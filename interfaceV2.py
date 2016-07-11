from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from os.path import isfile, split, splitext

class App(Frame):

	def __init__(self, parent, refLimit):            

		Frame.__init__(self, parent)
		self.allEmpty = True
		self.refNameElements = [] ############## passed in
		self.isOk = False
		self.parent = parent
		self.refs = []
		self.types = []
		self.names= []
		self.refEntries = []
		self.typeEntries = []
		self.nameEntries = []
		self.x = 1
		self.y = 1
		self.entryFrame = None
		self.initGUI()
		
	def initGUI(self):
		self.parent.title("Reference Copying")
		### creat a frame for entries
		self.entryFrame = Frame(self, relief = RAISED, borderwidth = 1)
		self.entryFrame.pack(fill = BOTH, expand = True)
		self.pack(fill = BOTH, expand = True)
		self.makeButtons()
		self.addEntry()
		
	def addEntry(self):
		### using grid for entries' positions
		### Ref entry
		Label(self.entryFrame, text = " Reference to copy:  R").grid(row = self.x, column = self.y%6, pady=5)
		self.y += 1
		Er = Entry(self.entryFrame, bd = 5, width = 4)
		Er.grid(row = self.x, column = self.y%6 , pady=5)
		self.refEntries.append(Er)
		self.y += 1

		### Name entry
		Ln = Label(self.entryFrame, text = "    Name:  R").grid(row = self.x, column = self.y%6 , pady=5)
		self.y += 1
		En = Entry(self.entryFrame, bd = 5, width = 4)
		En.grid(row = self.x, column = self.y%6, pady=5)
		self.nameEntries.append(En)
		self.y += 1

		### Type entry
		Lt = Label(self.entryFrame, text = "    Type:").grid(row = self.x, column = self.y%6, pady=5)
		self.y += 1
		Et = Entry(self.entryFrame, bd = 5, width = 9)
		Et.grid(row = self.x, column = self.y%6+6, padx = 5, pady=5)
		self.typeEntries.append(Et)
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

	def OK(self):
		### Command when Ok button is clicked				
		if self.getContent():
			self.isOk = True
			self.closeWindow()
						
	def getContent(self): 
		''' Get inputs in ref, name, and type entries. Return true if successful'''
		for num in range(0, len(self.refEntries)):
			ref = self.refEntries[num].get()
			nam = self.nameEntries[num].get() ####### this will be the dependoon
			typ = self.typeEntries[num].get()
			if self.IfErrorAndappendLists(num + 1, ref, nam, typ):
				self.refs = []
				self.types = []
				self.deps = []
				return False

		if self.allEmpty:
			self.allEntriesEmptyWarning()
			return False

		return True

	def IfErrorAndappendLists(self, row, ref, nam, typ):
		''' Append to ref, type, dep, and wire list if no entries is emtpy. 
			Return true if there is any entries missing or incorrect. 
			All missing is not missing'''
		if ref and typ and wire:
			if self.numberInRange(row, ref, dep, wire):
				self.refs.append(ref)
				self.types.append(typ)
				self.deps.append(dep)
				self.wires.append(wire) 
				self.allEmpty = False
				return False # other three exist(dep does not matter)
			else:
				return True
		elif (not dep) and (not ref) and (not typ) and (not wire):
			return False # all missing
		elif not ref:
			self.refEntryMissingWarning(row)
			return True 
		elif not typ:
			self.typeEntryMissingWarning(row)
			return True
		elif not wire:
			self.wireEntryMissingWarning(row)
			return True

	def numberInRange(self, row, ref, nam):   ###################################### ref num needs to be in the list, and nam needs to be in the gap
		""" check if ref and wire numbers are in range. 
			Wire and ref numbers have to be int and grater than 0""" 
		try:
			if int(ref) > self.refLimit or int(ref) < 1:
					self.refNumOutOfRnageWarning(row)
					return False
		except: 
			self.refEntryFormatIncorrect(row)
			return False

		try:
			if (dep != '') and (int(dep) > self.refLimit or int(dep) < 1):
				self.depNumOutOfRnageWarning(row)
				return False 
		except:
			self.depEntryFormatIncorrect(row)
			return False

		for n in range(0, len(wire)):
			try:
				if int(wire[n]) > self.wireLimit or int(wire[n]) < 1:   
					self.wireNumOutOfRnageWarning(row)
					return False
			except:
				self.wireEntryFormatIncorrect(row)
				return False

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

	def refNumOutOfRnageWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number out of range!")

	def depNumOutOfRnageWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", dependence number out of range!")

	def wireNumOutOfRnageWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", wire number out of range!")

	def refEntryFormatIncorrect(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number format incorrect!")

	def depEntryFormatIncorrect(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", dep number format incorrect!")

	def wireEntryFormatIncorrect(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", wire input format incorrect!")
