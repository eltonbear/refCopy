from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from os.path import isfile, split, splitext

class App(Frame):

	def __init__(self, parent, refNameList):            

		Frame.__init__(self, parent)
		self.allEmpty = True
		self.refNameList = refNameList
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
			nam = self.nameEntries[num].get()
			typ = self.typeEntries[num].get()
			if self.ifErrorAndAppendLists(num + 1, ref, nam, typ):
				self.refs = []
				self.names = []
				self.types = []
				return False

		if self.allEmpty:
			self.allEntriesEmptyWarning()
			return False

		return True

	def ifErrorAndAppendLists(self, row, ref, newName, typ):
		''' Append to ref, type, dep, and wire list if no entries is emtpy. 
			Return true if there is any entries missing or incorrect. 
			if all missing, return false
			if all exist, append if all in range and formatted correctly'''
		if ref and newName and typ:
			if self.numberInRange(row, ref, newName):
				self.refs.append(ref)
				self.names.append(newName)
				self.types.append(typ)				 
				self.allEmpty = False
				return False # other three exist(dep does not matter)
			else:
				return True
		elif (not newName) and (not ref) and (not typ):
			return False
		elif not ref:
			self.refEntryMissingWarning(row)
			return True 
		elif not newName:
			self.nameEntryMissingWarning(row)
			return True
		elif not typ:
			self.typeEntryMissingWarning(row)
			return True

	def numberInRange(self, row, oldName, newName):
		""" check if ref and wire numbers are in range. 
			Wire and ref numbers have to be int and grater than 0""" 
		if oldName.isdigit():
			if oldName not in self.refNameList:
				self.refNumOutOfRangeWarning(row)
				return False
		else:
			self.refEntryFormatIncorrect(row)
			return False

		if newName.isdigit():
			if newName in self.refNameList:
				self.nameNumOutOfRangeWarning(row)
				return False
		else:
			self.nameEntryFormatIncorrect(row)
			return False
		return True
			
	### Warnings
	def allEntriesEmptyWarning(self):
		messagebox.showinfo("Warning", "Nothing has been inputted")

	def refEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number missing!")

	def nameEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", name missing!")

	def typeEntryMissingWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", type missing!")

	def refNumOutOfRangeWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number does not exist!")

	def nameNumOutOfRangeWarning(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", name has already been used!")

	def refEntryFormatIncorrect(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", reference number format incorrect!")

	def nameEntryFormatIncorrect(self, row):
		messagebox.showinfo("Warning", "Row " + str(row) + ", name format incorrect!")	

	def incorrectFileNameWarning(self):
		messagebox.showinfo("Warning", "File does not exist!")

	def emptyFileNameWarning(self):
		messagebox.showinfo("Warning", "No files selected!")

# window = Tk()
# GUI = App(window, None)
# window.mainloop()


# print("copy: " + str(GUI.refs))
# print("names: " + str(GUI.names))
# print("Type: " + str(GUI.types))

			
