import cv2
import numpy as np 
import copy
import pydialog as pd

# sysWidth=1536
# sysHeight=864
sysWidth,sysHeight=pd.getSysDimensions();
mpW=sysWidth/1536;
mpH=sysHeight/864;

class DrawingArea:
	def __init__(self,x1,y1,WH,wx2,hy2,padxy=0,hidden=False):
		x1=int(mpW*x1);
		y1=int(mpH*y1);
		wx2=int(mpW*wx2);
		hy2=int(mpH*hy2);
		self.padx=int(mpW*padxy);
		self.pady=int(mpH*padxy);

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
		self.blank=np.zeros((self.height,self.width,3),np.uint8)+80
		self.image=copy.copy(self.blank)
		self.originalImage=None
		self.editedImage=None
		self.overlay=None
		self.imgHeight=0
		self.imgWidth=0

		self.padxy=padxy

		self.startCol=0
		self.endCol=0
		self.startRow=0
		self.endRow=0

		self.imgX1=0
		self.imgX2=0
		self.imgY1=0
		self.imgY2=0
		#self.createImage()
	def implementButtonFunction(self,mouseX,mouseY):
		pass

	def setOriginalImage(self,image):
		self.originalImage=image
		self.imgHeight=image.shape[0]
		self.imgWidth=image.shape[1]
		self.startCol,self.startRow,self.endCol,self.endRow=self.screenImagePadding(self.originalImage,self.imgHeight,self.imgWidth,self.height-(2*self.pady),self.width-(2*self.padx))
		self.imgX1=self.startCol+self.x1
		self.imgY1=self.startRow+self.y1
		self.imgX2=self.endCol+self.x1
		self.imgY2=self.endRow+self.y1
		self.editedImage=image
		self.createBlankOverlay()

	def updateEditImage(self,image):
		self.editedImage=image
		self.image=copy.copy(self.blank)
		image=cv2.resize(image,(self.endCol-self.startCol,self.endRow-self.startRow), interpolation = cv2.INTER_AREA)
		self.image[self.startRow:self.endRow,self.startCol:self.endCol]=image


	def createBlankOverlay(self):
		self.overlay=np.zeros((self.imgY2-self.imgY1,self.imgX2-self.imgX1,4),np.uint8)

	def createColorOverlay(self,b,g,r,a):
		self.createBlankOverlay()
		self.overlay[:,:]=(b,g,r,a)

	def screenImagePadding(self,img,he,wi,h,w):

		if(he/wi > h/w):
			newWidth=int(h*wi/he)
			resized=cv2.resize(img, (newWidth,h), interpolation = cv2.INTER_AREA)
			startCol=(((w)-newWidth)//2)+(self.padxy)
			endCol=(((w)+newWidth)//2)+(self.padxy)
			self.image[self.padxy:h+self.padxy,startCol:endCol]=resized
			return (startCol,self.padxy,endCol,self.height-self.padxy)
		else:
			newHeight=int((w)*he/wi)
			resized=cv2.resize(img, (w,newHeight), interpolation = cv2.INTER_AREA)
			startRow=(h-newHeight)//2+self.padxy
			endRow=(h+newHeight)//2+self.padxy
			self.image[startRow:endRow,self.padxy:w+self.padxy]=resized
			return (self.padxy,startRow,self.width-self.padxy,endRow)
