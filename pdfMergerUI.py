#!/usr/bin/python
from Tkinter import *
from Tkinter import Tk
from ScrolledText import *
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import tkMessageBox
import tkFileDialog
import Tkconstants
import os
import sys

import datetime
import glob

class pdfMergerUI(Frame):
	
	def __init__(self, root):

		Frame.__init__(self, root)
		self.returned_values = {}    # Create an empty dict.
		if (os.name == 'nt'):
			x = 750
		else:
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
		if (os.name == 'nt'):
			img = self.resource_path("pdfmerger.ico")
			root.iconbitmap(default=img)
		
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

		self.scrolledLogger = ScrolledText(state='disabled', width=90, height=10, background="black", fg="white")
		self.scrolledLogger.grid(row=5, column=0, rowspan=2, columnspan=3, padx=paddingX, pady=paddingY)

		self.start = Button(text='Begin', command=self.start)
		self.start.grid(row=4, column=0, columnspan=2, padx=paddingX, pady=paddingY)
        
		self.info = Button(text='Information', command=self.info)
		self.info.grid(row=4, column=1, padx=paddingX, pady=paddingY)
		
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

	# Yes No question message box
	def info(self):
		#os.system('info.txt')
		f= open(self.resource_path("info.txt"))
		self.messageBox("Information", f.read())
        
	def getSourceDir(self):
		self.browseSource.delete('1.0', END)
		self.returned_values['sourceDir'] = tkFileDialog.askdirectory(**self.dir_opt)
		self.browseSource.insert(INSERT, self.returned_values['sourceDir'])

	def getDestDir(self):
		self.browseDest.delete('1.0', END)
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
		self.source = self.browseSource.get("1.0","end-1c")
		self.destination = self.browseDest.get("1.0","end-1c")
		if (self.source== ""):
			self.log("Warning: No source directory has been entered")
			self.warningBox("Warning", "No source directory has been entered")

		if (self.destination == ""):
			self.log("Warning: No destination directory has been entered")
			self.warningBox("Warning", "No destination directory has been entered")

		if (self.destination != "" and self.source != ""):
			self.log("Starting")
			if self.returned_values['interlace'] == True:
				self.interlace()
			else:
				self.merge()

	def log(self, msg):
		self.scrolledLogger.configure(state='normal')
		self.scrolledLogger.insert(END, msg + "\n")
		self.scrolledLogger.see('end')
		self.scrolledLogger.configure(state='disabled')

	def merge(self):
		(pdfFiles, pdfNo) = self.initPdfFunc()
		sourceDIR = self.source + "/"
		destinationDIR = self.destination + "/"
		if (len(pdfFiles) > 0):
			saveFile = "merged_" + str(pdfNo) + "_" + str(datetime.date.today()) + ".pdf"
			merger = PdfFileMerger()
			self.log("Merging....")
			for filename in pdfFiles:
				merger.append(PdfFileReader(os.path.join(sourceDIR, filename), 'rb'))
			merger.write(os.path.join(destinationDIR, saveFile).encode("utf8"))
			string = "Done file save to %s%s" % (destinationDIR, saveFile)
			self.log(string)
		else:
			string = "Warning: Found no pdf files in %s" % (sourceDIR)
			self.log(string)

	def interlace(self):
		(pdfFiles, pdfNo) = self.initPdfFunc()
		sourceDIR = self.source + "/"
		destinationDIR = self.destination + "/"
		if (len(pdfFiles) > 0):
			document1 = PdfFileReader(open(sourceDIR + pdfFiles[0], 'rb'))
			document2 = PdfFileReader(open(sourceDIR + pdfFiles[1], 'rb'))
			saveFile = "interlaced_" + str(pdfNo) + "_" + str(datetime.date.today()) + ".pdf"
			self.log("Interlacing....")
			inter = PdfFileWriter()
			interlacedFile = os.path.join(destinationDIR, saveFile)
			for i in range(document1.getNumPages()):
				document2pagecount =  document2.getNumPages()
				document2page = document2pagecount - i
				inter.addPage(document1.getPage(i))
				inter.addPage(document2.getPage(document2page-1))
				output_stream = file(interlacedFile, "wb")
				inter.write(output_stream)

			string = "Done file save to %s%s" % (destinationDIR, saveFile)
			self.log(string)
		else:
			string = "Warning: Found no pdf files in %s" % (sourceDIR)
			self.log(string)

	def initPdfFunc(self):
		sourceDIR = self.source + "/"
		destinationDIR = self.destination + "/"
		pdfFiles = 0
		pdfNumber = 0
		if (os.path.isdir(sourceDIR)):
			if (not os.path.isdir(destinationDIR)):
				self.log("Making sestination directory")
				os.mkdir(destinationDIR)

			pdf_files = [f for f in os.listdir(sourceDIR) if f.endswith('pdf')]
			pdf_files.sort()

			if (len(pdf_files) > 1):
				if self.returned_values['interlace'] == True:
					inter_files = [f for f in os.listdir(destinationDIR) if f.startswith('interlaced_')]
					pdfNumber = len(inter_files) + 1
				else:
					merged_files = [f for f in os.listdir(destinationDIR) if f.startswith('merged_')]
					pdfNumber = len(merged_files) + 1

		else:
			self.log("Source directory does not exist")
			
		return (pdf_files, pdfNumber)
        
	def resource_path(self, relative):
		if hasattr(sys, "_MEIPASS"):
			return os.path.join(sys._MEIPASS, relative)
            
		return os.path.join(relative)
        
if __name__=='__main__':
	
	root = Tk()
	pdfMergerUI(root)
	root.mainloop()

	