import cv2
import numpy as np 

class Menu:
	def __init__(self,x1,y1,WH,wx2,hy2,buttonList,hidden=False):
		self.hidden=hidden
		self.x1=x1
		self.y1=y1
		if(WH==True):
			self.width=wx2
			self.height=hy2
			self.x2=self.x1+self.width
			self.y2=self.y1+self.height
		else:
			self.x2=wx2
			self.y2=hy2
			self.width=self.x2-self.x1
			self.height=self.y2-self.y1
		self.buttonList=buttonList
		self.createImage()
		self.drawButtons()
		self.buttonListAbsolutePositioning()
		self.setButtonMenu()

	def createImage(self):
		self.image=self.image=np.zeros((self.height,self.width,3),np.uint8)+128

	def drawButtons(self):
		for button in self.buttonList:
			x1=button.x1
			y1=button.y1
			x2=button.x2
			y2=button.y2
			self.image[y1:y2,x1:x2]=button.image

	def drawAButton(self,button):
		x1=button.x1-self.x1
		y1=button.y1-self.y1
		x2=button.x2-self.x2 
		y2=button.y2-self.y2
		self.image[y1:y2,x1:x2]=button.image
			
	def implementButtonFunction(self,mouseX,mouseY):
		mouseX
		mouseY
		for button in self.buttonList:
			x1=button.x1
			y1=button.y1
			x2=button.x2
			y2=button.y2
			if(x1<mouseX<x2):
				if(y1<mouseY<y2):
					button.implementFunction(mouseX,mouseY)
	
	def buttonListAbsolutePositioning(self):
		for button in self.buttonList:
			button.x1+=self.x1
			button.y1+=self.y1
			button.x2+=self.x1
			button.y2+=self.y1

	def setButtonMenu(self):
		for button in self.buttonList:
			button.setMenu(self)
