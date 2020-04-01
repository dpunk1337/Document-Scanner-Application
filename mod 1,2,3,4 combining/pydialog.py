import tkinter as tk
from tkinter import filedialog

def getSysDimensions():
	root=tk.Tk()
	root.withdraw()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	return screen_width,screen_height

def getFile():
	root=tk.Tk()
	root.withdraw()
	file_path=filedialog.askopenfilename()
	return file_path

def saveFile():
	root=tk.Tk()
	root.withdraw()
	file_path=filedialog.asksaveasfile(mode='w')
	return file_path