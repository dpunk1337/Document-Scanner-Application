import cv2
import numpy as np 
# import button as _b

def passer(button,menu,mouseX,mouseY):
	print((button.x1,button.y1),(button.x2,button.y2))
	print((menu.x1,menu.y1),(menu.x2,menu.y2))
	print(menu.width,menu.height)

def map(n,x1,y1,x2,y2):
	return int((n*(y2-x2)/(y1-x1))+0.5)

class Trackbar:
	def __init__(self,x1,y1,WH,wx2,hy2,name,window,r1,r2,function,padY=0,padX=0):
		# self.hidden=hidden
		self.x1=x1+padX
		self.y1=y1+padY
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
		self.number=0
		self.name=name
		self.window=window
		self.r1=r1
		self.r2=r2
		self.function=function
		self.image=np.zeros((self.height,self.width,3),np.uint8)
		self.hby2=self.height//2
		self.createButtonImage()
		self.createTrackBarImage(r1,10)
	
	def createButtonImage(self):
		buttonWidth=10
		buttonHeight=20
		self.buttonImage=np.zeros((buttonHeight,buttonWidth,3),np.uint8)+255

	
	def createTrackBarImage(self,number,posX):
		cv2.putText(self.image,self.name+' : '+str(number),(10,self.hby2-20),cv2.FONT_HERSHEY_SIMPLEX, 0.6,(240,240,240),1,cv2.LINE_AA)
		track=cv2.rectangle(self.image,(10,self.hby2),(self.width-10,self.hby2+2),(128,128,128),-1)
		self.image[self.hby2-10:self.hby2+10,posX-5:posX+5]=self.buttonImage 

	def setMenu(self,menu):
		self.menu=menu

	def implementFunction(self,posX,posY):
		if self.x1+10 <=posX<= self.x2-10:
			if self.y1 < posY < self.y2:
				self.image=np.zeros((self.height,self.width,3),np.uint8)
				self.number=map(posX-self.x1-10,10,self.width-10,self.r1,self.r2)
				self.createTrackBarImage(self.number,posX-self.x1)
				self.menu.drawAButton(self)
				self.screen.drawAMenu(self.menu)
				cv2.imshow(self.window,self.screen.background)
				self.function(self.number)

	def setTrackbarScreen(self,screen):
		self.screen=screen

	def reset(self):
		self.createButtonImage()
		self.image=np.zeros((self.height,self.width,3),np.uint8)
		self.createTrackBarImage(self.r1,10)

