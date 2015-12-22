#!/usr/bin/python
from Tkinter import *
from ScrolledText import *
import tkMessageBox
import tkFileDialog
import Tkconstants


class pdfMergerUI(Frame):
	
	def __init__(self, root):

		Frame.__init__(self, root)
		self.returned_values = {}    # Create an empty dict.
		x = 700
		y = 350
		paddingX = 5
		paddingY = 5
		# Present some values
		self.returned_values['interlace'] = False
		self.returned_values['sourceDir'] = None
		self.returned_values['destDir'] = None

		# options for buttons
		button_opt = {'anchor': 'e', 'padx': 30, 'pady': 10}
		# options for labels
		text_opt = {'anchor': 'w', 'padx': 30, 'pady': 10}
		
		root.resizable(width=False, height=False)
		root.geometry('{}x{}'.format(x, y))
		root.wm_title("PDF Merger")
		
		# define buttons, text views and scroll views
		self.browseSource = Text(text=self.returned_values['sourceDir'], width=70,height=1)
		self.browseSource.grid(row=1, column=0, padx=paddingX, pady=paddingY)
		
		self.browseButtonSource = Button(text='Browse for source', command=self.getSourceDir, width=17,height=1)
		self.browseButtonSource.grid(row=1, column=1, padx=paddingX, pady=paddingY)

		self.browseButtonDest = Button(text='Browse for destination', command=self.getDestDir, width=17,height=1)
		self.browseButtonDest.grid(row=2, column=1, padx=paddingX, pady=paddingY)

		self.browseDest = Text(text=self.returned_values['destDir'], width=70,height=1)
		self.browseDest.grid(row=2, column=0, padx=paddingX, pady=paddingY)

		self.interlaceOp = Checkbutton(text='Enable interlacing', command=self.setInterlace, width=17,height=1)
		self.interlaceOp.grid(row=3, column=1, padx=paddingX, pady=paddingY)

		self.scrolledLogger = ScrolledText(state='disabled', width=90, height=10)
		self.scrolledLogger.grid(row=5, column=0, rowspan=2, columnspan=3, padx=paddingX, pady=paddingY)

		self.start = Button(text='Begin', command=self.start)
		self.start.grid(row=4, column=0, columnspan=2, padx=paddingX, pady=paddingY)
		
		# defining options for opening a directory
		self.dir_opt = options = {}
		options['mustexist'] = False
		options['parent'] = root
		options['title'] = 'Choose a Directory'

	# Message box method
	def messageBox(self, title, message):
		return tkMessageBox.showinfo(title, message)

	def warningBox(self, title, message):
		return tkMessageBox.showwarning(title, message)

	# Yes No question message box
	def yesNo(self, title, question):
		return tkMessageBox.askyesno(title, question)

	def getSourceDir(self):
		self.returned_values['sourceDir'] = tkFileDialog.askdirectory(**self.dir_opt)
		self.browseSource.insert(INSERT, self.returned_values['sourceDir'])

	def getDestDir(self):
		self.returned_values['destDir']  = tkFileDialog.askdirectory(**self.dir_opt)
		self.browseDest.insert(INSERT, self.returned_values['destDir'])

	def setInterlace(self):
		if self.returned_values['interlace'] == True:
			self.messageBox('Interlacing', "Interlacing option has been removed")
			self.returned_values['interlace'] = False
			self.log("Interlacing disabled")
		else:
			self.messageBox('Interlacing', "This option will interlace pages of 2 PDF files")
			self.returned_values['interlace'] = True
			self.log("Interlacing enabled")

	def start(self):
		self.log("Starting")
		if (self.returned_values['sourceDir'] == None):
			self.warningBox("Warning", "No source directory has been entered")
		if (self.returned_values['destDir'] == None):
			self.warningBox("Warning", "No destination directory has been entered")


		# if self.returned_values['interlace'] == True:
		# 	self.interlace(self.returned_values['sourceDir'], self.returned_values['destDir'])
		# else:
		# 	self.merge(self.returned_values['sourceDir'], self.returned_values['destDir'])

	def log(self, msg):
		self.scrolledLogger.configure(state='normal')
		self.scrolledLogger.insert(END, msg + "\n")
		self.scrolledLogger.see('end')
		self.scrolledLogger.configure(state='disabled')

if __name__=='__main__':
	
	root = Tk()
	pdfMergerUI(root)
	root.mainloop()

	