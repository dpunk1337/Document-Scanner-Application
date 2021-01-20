import cv2
import numpy as np 
import pydialog as pd 

# sysWidth=1536
# sysHeight=864
sysWidth,sysHeight=pd.getSysDimensions();
mpW=sysWidth/1536;
mpH=sysHeight/864;

def passer(button,menu,mouseX,mouseY):
	print((button.x1,button.y1),(button.x2,button.y2))
	print((menu.x1,menu.y1),(menu.x2,menu.y2))
	print(menu.width,menu.height)

def buttonTableCreator(nameList,functionList,colorList,rows,cols,Nbuttons,menuWidth,menuHeight,xPad=0,yPad=0):
	buttonTableList=list()
	buttonWidth=menuWidth//cols
	buttonHeight=menuHeight//rows
	k=0
	for i in range(rows):
		for j in range(cols):
			if(nameList[k]!=' '):
				x=j*buttonWidth+xPad
				y=i*buttonHeight+yPad
				buttonTableList.append(Button(nameList[k],functionList[k],x,y,True,buttonWidth,buttonHeight,colorList[k]))
			k=k+1
			if k==Nbuttons:
				break;
		if k==Nbuttons:
			break;
	return buttonTableList

class Button:
	font=cv2.FONT_HERSHEY_SIMPLEX
	def __init__(self,name,function,x1,y1,WH,wx2,hy2,color=(80,80,80),fontSize=0.7):
		x1=int(mpW*x1)
		y1=int(mpH*y1)
		wx2=int(mpW*wx2)
		hy2=int(mpH*hy2)
		fontSize=(mpH*fontSize if mpH<mpW else mpW*fontSize)

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
		self.name=name
		self.function=function
		self.image=np.zeros((self.height,self.width,3),np.uint8)
		self.createImage(color[0],color[1],color[2],fontSize)

	def createImage(self,b,g,r,fontSize):
		self.image=cv2.rectangle(self.image,(0,0),(self.width,self.height),(b,g,r),-1)
		self.image=cv2.rectangle(self.image,(0,0),(self.width,self.height),(20,20,20),5)
		textSize=cv2.getTextSize(self.name,self.font,fontSize,2)[0]
		textX=int((self.width-(textSize[0]))/2)
		textY=int((self.height+textSize[1])/2)
		cv2.putText(self.image,self.name,(textX,textY), self.font, fontSize,(240,240,240),(2 if sysWidth>1300 else 1),cv2.LINE_AA)

	def implementFunction(self,mouseX,mouseY):
		self.function(self,self.menu,mouseX,mouseY)

	def changeFunction(self,newFunction):
		self.function=newFunction

	def setMenu(self,menu):
		self.menu=menu

	def changeColor(self,b,g,r):
		self.createImage(b,g,r,0.7)
