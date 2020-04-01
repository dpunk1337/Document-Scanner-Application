import cv2
import numpy as np 
import button as _b
import trackbar as _t

gray=(80,80,80)

class Dialog:
	cancelFunction=None
	okayFunction=None
	def __init__(self,x1,y1,WH,wx2,hy2,nTabs,nTb,varNameList,functionList,hidden=False):
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
		self.tabHeight=self.height//nTabs
		self.buttonList=list()
		self.trackbarList=list()
		self.createImage()
		self.createDialogButtons()
		self.createDialogTrackbars(nTb,varNameList,functionList)
		self.drawButtons()
		self.buttonListAbsolutePositioning()
		self.setButtonMenu()

	def createImage(self):
		self.image=self.image=np.zeros((self.height,self.width,3),np.uint8)+128

	def createDialogButtons(self):
		blist=_b.buttonTableCreator(('okay','cancel'),(Dialog.okayFunction,Dialog.cancelFunction),(gray,gray),1,2,2,self.width-20,self.tabHeight-20,10,10)
		self.buttonList.extend(blist)

	def createDialogTrackbars(self,nTb,varNameList,functionList):
		for i in range(nTb):
			tb=_t.Trackbar(10,(i+1)*self.tabHeight,True,self.width-20,self.tabHeight-10,varNameList[i],'screen',1,101,functionList[i])
			self.trackbarList.append(tb)
			tb.setMenu(self)
		self.buttonList.extend(self.trackbarList)

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

	def buttonListAbsolutePositioning(self):
		for button in self.buttonList:
			button.x1+=self.x1
			button.y1+=self.y1
			button.x2+=self.x1
			button.y2+=self.y1

	def setButtonMenu(self):
		for button in self.buttonList:
			button.setMenu(self)

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
	def setTrackbarScreen(self,screen):
		for trackbar in self.trackbarList:
			trackbar.setTrackbarScreen(screen)

	def setButtonMenu(self):
		for button in self.buttonList:
			button.setMenu(self)

	def resetTrackbars(self):
		for trackbar in self.trackbarList:
			trackbar.reset()
			self.drawAButton(trackbar)