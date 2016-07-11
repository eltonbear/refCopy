from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from os.path import isfile, split, splitext

class App(Frame):

	def __init__(self, parent, refLimit, wireLimit):            

		Frame.__init__(self, parent)
		self.allEmpty = True
		self.refLimit = refLimit
		self.wireLimit = wireLimit
		self.isOk = False
		self.parent = parent
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
		Label(self.entryFrame, text = "Reference Number: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Er = Entry(self.entryFrame, bd = 5, width = 4)
		Er.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.refEntries.append(Er)
		self.y += 1

		# ### Type entry
		Lt = Label(self.entryFrame, text = "Reference Type: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Et = Entry(self.entryFrame, bd = 5, width = 9)
		Et.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.typeEntries.append(Et)
		self.y += 1

		### Dep entry
		Ld = Label(self.entryFrame, text = "Depends on Ref: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Ed = Entry(self.entryFrame, bd = 5, width = 4)
		Ed.grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.depEntries.append(Ed)
		self.y += 1

		### Wire entry
		Lw = Label(self.entryFrame, text = "Wire Numbers: ").grid(row = self.x, column = self.y%8, padx=5 , pady=5)
		self.y += 1
		Ew = Entry(self.entryFrame, bd = 5, width = 25)
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

	def OK(self):
		### Command when Ok button is clicked				
		if self.getContent():
			self.isOk = True
			self.closeWindow()
						
	def getContent(self): 
		''' Get inputs in ref, type, dependon, and wire entries. Return true if successful'''
		for num in range(0, len(self.refEntries)):
			ref = self.refEntries[num].get()
			typ = self.typeEntries[num].get()
			dep = self.depEntries[num].get()
			wireList = []
			wireListTemp = self.wireEntries[num].get().split(",")
			for n in range(0, len(wireListTemp)):
				temp = wireListTemp[n].strip()
				if temp != "":
					wireList.append(temp)

			if self.IfErrorAndappendLists(num + 1, ref, typ, dep, wireList):
				self.refs = []
				self.types = []
				self.deps = []
				self.wires = []
				return False

		if self.allEmpty:
			self.allEntriesEmptyWarning()
			return False

		return True

	def IfErrorAndappendLists(self, row, ref, typ, dep, wire):
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

	def numberInRange(self, row, ref, dep, wire):  
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
