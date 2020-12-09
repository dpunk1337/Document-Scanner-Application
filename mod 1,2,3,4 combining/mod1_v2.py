import cv2
import numpy as np
import pydialog as pd
import copy
import menu as _m
import button as _b
import screen as _s
import drawingArea as _da
import trackbar as _t
import sys



screenCopy=None
flagg=True

editionList=[]
editedImageIndex=0

overlayBlank=None
overlayList=[]
currentOverlay=None

sysWidth,sysHeight=pd.getSysDimensions()
screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)+50
screenList=list()


bdownflag=False
flag=False

xUnit=sysWidth//10
yUnit=sysHeight//10

gray=(50,50,50)

mainMenuFlag=False
def quitToMainMenu(a,b,c,d):
	global controlFlag,mainMenuFlag
	mainMenuFlag=True
	controlFlag=False

def exitProgram(a,b,c,d):
	raise SystemExit

def exitModule(a,b,c,d):
	global controlFlag
	controlFlag=False

# cv2.namedWindow('screen',cv2.WINDOW_NORMAL)
def next(a,b,c,d):
	global final,controlFlag
	cropped=overlayBlank[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2]
	h,w=drawArea.originalImage.shape[:2]
	resizedOverlay=cv2.resize(cropped,(w,h), interpolation = cv2.INTER_AREA)
	final=blendImage(resizedOverlay,drawArea.originalImage)
	controlFlag=False


def save(button,menu,mouseX,mouseY):
	global final
	cropped=overlayBlank[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2]
	h,w=drawArea.originalImage.shape[:2]
	resizedOverlay=cv2.resize(cropped,(w,h), interpolation = cv2.INTER_AREA)
	final=blendImage(resizedOverlay,drawArea.originalImage)
	saveFileAddress=pd.saveFile()
	if saveFileAddress is not None:
		cv2.imwrite(saveFileAddress.name,final)

def redo(button,menu,mouseX,mouseY):
	global editedImageIndex,screenList
	if editedImageIndex < len(editionList)-1:
		editedImageIndex+=1
		currentScreen.background[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2]=copy.copy(editionList[editedImageIndex])
		overlayBlank[drawArea.y1:drawArea.y2,drawArea.x1:drawArea.x2]=copy.copy(overlayList[editedImageIndex])
		cv2.imshow('screen',currentScreen.background)

def undo(button,menu,mouseX,mouseY):
	global editedImageIndex,screenList,overlayList
	if(editedImageIndex>0):
		editedImageIndex-=1
		currentScreen.background[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2]=copy.copy(editionList[editedImageIndex])
		overlayBlank[drawArea.y1:drawArea.y2,drawArea.x1:drawArea.x2]=copy.copy(overlayList[editedImageIndex])
		cv2.imshow('screen',currentScreen.background)

def createScreenColor():
	global screenCopy,currentOverlay,overlayBlank
	screenCopy=copy.copy(currentScreen.background)
	screenCopy=cv2.cvtColor(screenCopy,cv2.COLOR_BGR2BGRA)
	screenCopy=createColorScreen(screenCopy)

	currentOverlay=np.zeros((sysHeight,sysWidth,4),np.uint8)
	currentOverlay[:]=(brush.b,brush.g,brush.r,255-brush.transparency)
	currentOverlay=blendCurrentandBlank(currentOverlay,overlayBlank)

def createColorScreen(img):
	over=np.zeros_like(img)
	over[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2]=(brush.b,brush.g,brush.r,255-brush.transparency)
	return screenBlend(over,img)

def drawOnOverlay(x,y):
	global currentOverlay,overlayBlank
	sizeHalf=(brush.size//2)
	y1=y-sizeHalf
	y2=y+brush.size-sizeHalf
	x1=x-sizeHalf
	x2=x+brush.size-sizeHalf
	currentScreen.background[y1:y2,x1:x2]=blender(brush.image,screenCopy[y1:y2,x1:x2],currentScreen.background[y1:y2,x1:x2])
	overlayBlank[y1:y2,x1:x2]=blender(brush.image,currentOverlay[y1:y2,x1:x2],overlayBlank[y1:y2,x1:x2])

def drawImage():
	print('hi hi hi')
	pass

# final=blendImage(resizedOverlay,drawArea.originalImage)
def blendImage(img1,img2):
	b1,g1,r1,a1=cv2.split(img1)
	b2,g2,r2=cv2.split(img2)
	
	a1_255=a1/255
	l=np.ones_like(a1_255)
	a2_255=l-a1_255

	avgb=b1*a1_255+b2*a2_255
	avgg=g1*a1_255+g2*a2_255
	avgr=r1*a1_255+r2*a2_255

	avgb=avgb.astype(np.uint8)
	avgg=avgg.astype(np.uint8)
	avgr=avgr.astype(np.uint8)	

	return cv2.merge((avgb,avgg,avgr))

	# currentOverlay=blendCurrentandBlank(currentOverlay,overlayBlank)
def blendCurrentandBlank(current_overlay,overlay_blank):
	T=brush.transparency/255

	edit=cv2.addWeighted(current_overlay,1-T,overlay_blank,T,0)
	retn,thresh=cv2.threshold(overlay_blank[:,:,3],1,255,cv2.THRESH_BINARY)
	thresh_inv=cv2.bitwise_not(thresh)
	current_overlay=cv2.bitwise_and(current_overlay,current_overlay,mask=thresh_inv)

	b,g,r,a=cv2.split(edit)
	a=a.astype(float)
	a+=0.3*a
	a[a>255]=255	
	a=a.astype(np.uint8)
	edit=cv2.merge((b,g,r,a))

	edit=cv2.bitwise_and(edit,edit,mask=thresh)
	edit=cv2.add(edit,current_overlay)
	return edit

def screenBlend(img1,img2):
	b1,g1,r1,a1=cv2.split(img1)
	b2,g2,r2,a2=cv2.split(img2)
	
	a1_255=a1/255
	l=np.ones_like(a1_255)
	a2_255=l-a1_255

	avgb=b1*a1_255+b2*a2_255
	avgg=g1*a1_255+g2*a2_255
	avgr=r1*a1_255+r2*a2_255

	avgb=avgb.astype(np.uint8)
	avgg=avgg.astype(np.uint8)
	avgr=avgr.astype(np.uint8)	

	return cv2.merge((avgb,avgg,avgr))

def blender(brushImage,overlayImage,regularImage):
	overlayImage=cv2.bitwise_and(overlayImage,overlayImage,mask=brush.mask)
	regularImage=cv2.bitwise_and(regularImage,regularImage,mask=brush.inv_mask)
	return cv2.add(overlayImage,regularImage)

def nothing(a):
	pass

def changeBrushTransparency(transparency):
	brush.setTransparency(transparency)

def changeBrushSize(number):
	brush.setSize(number+1)

def showBrush(posX,posY):
	sizeHalf=(brush.size//2)
	y1=posY-sizeHalf
	y2=posY+brush.size-sizeHalf
	x1=posX-sizeHalf
	x2=posX+brush.size-sizeHalf
	
	copyScreen=copy.copy(currentScreen.background)
	edit=copyScreen[y1:y2,x1:x2]

	T=brush.transparency/255
	prop=cv2.cvtColor(copy.copy(brush.image),cv2.COLOR_BGRA2BGR)
	prop=cv2.addWeighted(prop,1-T,copy.copy(edit),T,0)
	prop=cv2.bitwise_and(prop,prop,mask=brush.mask)
	edit=cv2.bitwise_and(edit,edit,mask=brush.inv_mask)
	edit=cv2.add(prop,edit)

	#edit=blendImage(brush.image,edit)
	copyScreen[y1:y2,x1:x2]=edit
	cv2.imshow('screen',copyScreen)

def showXYpos(posX,posY):
	posX-=drawArea.imgX1+1
	posY-=drawArea.imgY1+1
	posX=str(posX)
	posY=str(posY)
	currentScreen.background[0:10,:]=np.zeros((10,sysWidth,3),np.uint8)+50
	cv2.putText(currentScreen.background,' X: '+posX+' Y: '+posY,(5,9),cv2.FONT_HERSHEY_SIMPLEX,.4,(255,255,255),1)
	cv2.imshow('screen',currentScreen.background)

def open(button,menu,mouseX,mouseY):
	global screenImageIndex,editionList,editedImageIndex,overlayBlank
	img=cv2.imread(pd.getFile())
	imageOpener(img)

def imageOpener(img):
	global final
	if (img is not None):
		final=img
		drawArea.image=copy.copy(drawArea.blank)
		currentScreen.drawAMenu(drawArea)
		drawArea.setOriginalImage(img)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

		editionList.clear()
		editedImageIndex=0
		editionList.append(copy.copy(currentScreen.background)[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2])

		overlayList.clear()
		overlayBlank=np.zeros((sysHeight,sysWidth,4),np.uint8)
		overlayList.append(copy.copy(overlayBlank)[drawArea.y1:drawArea.y2,drawArea.x1:drawArea.x2])

def highlightdoodleBF(button,menu,mouseX,mouseY):
	if button.name=='Highlight':
		brush.type=1
		brush.createHighlightImage()
		m3blist[19].changeColor(128,128,128)
		m3blist[18].changeColor(50,50,50)
	else:
		brush.type=0
		brush.createDoodleImage()
		m3blist[19].changeColor(50,50,50)
		m3blist[18].changeColor(128,128,128)
	menu.drawAButton(m3blist[18])
	menu.drawAButton(m3blist[19])
	currentScreen.drawAMenu(menu)
	cv2.imshow('screen',currentScreen.background)

def map(n,x1,y1,x2,y2):
	return int((n*(y2-x2)/(y1-x1))+0.5)

def sets1m3(button,menu,mouseX,mouseY):
	currentScreen.hideAMenu(menu)
	currentScreen.unhideAMenu(m3)
	cv2.imshow('screen',currentScreen.background)

def chooseColor(button,menu,mouseX,mouseY):
	b,g,r=button.image[6,6]
	b=int(b)
	g=int(g)
	r=int(r)
	brush.setColor(b,g,r)
	m3blist[0].changeColor(b,g,r)
	menu.drawAButton(m3blist[0])
	currentScreen.drawAMenu(menu)
	cv2.imshow('screen',currentScreen.background)

def functionerMenu(event,x,y,flags,params):
	global flag,bdownflag,flagg,editedImageIndex,editionList,overlayList,currentOverlay
	if drawArea.x1<x<drawArea.x2:
		if drawArea.y1<y<drawArea.y2:
			showXYpos(x,y)
			showBrush(x,y)
			flag=True
			if(event==cv2.EVENT_LBUTTONDOWN):
				createScreenColor()
				bdownflag=True
				drawOnOverlay(x,y)
				cv2.imshow('screen',currentScreen.background)
			elif(event==cv2.EVENT_MOUSEMOVE):
				if(bdownflag):
					cv2.imshow('screen',currentScreen.background)
					# cv2.imshow('overlay',overlayBlank)
					drawOnOverlay(x,y)
			elif(event==cv2.EVENT_LBUTTONUP):
				bdownflag=False
				drawOnOverlay(x,y)
				editedImageIndex+=1
				if editedImageIndex < len(editionList):
					del overlayList[editedImageIndex:]
					del editionList[editedImageIndex:]
				editionList.append(copy.copy(currentScreen.background)[drawArea.imgY1:drawArea.imgY2,drawArea.imgX1:drawArea.imgX2])
				overlayList.append(copy.copy(overlayBlank)[drawArea.y1:drawArea.y2,drawArea.x1:drawArea.x2])

	else:
		if flag==True:
			flag=False
			cv2.imshow('screen',currentScreen.background)
		if(event==cv2.EVENT_LBUTTONDOWN):
			currentScreen.implementMenuFunction(x,y)
	
def passer(button,menu,mouseX,mouseY):
	print((button.x1,button.y1),(button.x2,button.y2))
	print((menu.x1,menu.y1),(menu.x2,menu.y2))
	print(menu.width,menu.height)


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
				number=map(posX-self.x1-10,10,self.width-10,self.r1,self.r2)
				self.createTrackBarImage(number,posX-self.x1)
				self.menu.drawAButton(self)
				currentScreen.drawAMenu(self.menu)
				cv2.imshow(self.window,currentScreen.background)
				self.function(number)

class Brush:
	def __init__(self):
		self.type=0
		self.b=0
		self.g=0
		self.r=0
		self.size=1
		self.transparency=0
		self.createDoodleImage()

		#self.image=cv2.cvtColor(self.image,cv2.BGR2BGRA)
	def createDoodleImage(self):
		self.image=np.zeros((self.size,self.size,4),np.uint8)
		cv2.circle(self.image,(self.size//2,self.size//2),self.size//2,(self.b,self.g,self.r,255-self.transparency),-1)
		_,self.mask=cv2.threshold(self.image[:,:,3],1,255,cv2.THRESH_BINARY)
		self.inv_mask=cv2.bitwise_not(self.mask)

	def createHighlightImage(self):
		self.image=np.zeros((self.size,self.size,4),np.uint8)
		cv2.rectangle(self.image,(int(self.size/2.5),0),(int(self.size//1.7),self.size),(self.b,self.g,self.r,255-self.transparency),-1)
		_,self.mask=cv2.threshold(self.image[:,:,3],1,255,cv2.THRESH_BINARY)
		self.inv_mask=cv2.bitwise_not(self.mask)

	def setColor(self,b,g,r):
		self.b=b 
		self.g=g 
		self.r=r
		if self.type:
			self.createHighlightImage()
		else:
			self.createDoodleImage()

	def setSize(self,size):
		self.size=size
		if self.type:
			self.createHighlightImage()
		else:
			self.createDoodleImage()
	
	def setTransparency(self,transparency):
		self.transparency=transparency
		if self.type:
			self.createHighlightImage()
		else:
			self.createDoodleImage()

brush=Brush()

m1nlist=('Main Menu','Next','Undo','Redo')
m1flist=(quitToMainMenu,next,undo,redo)
m1clist=(gray,gray,gray,gray)
m1blist=_b.buttonTableCreator(m1nlist,m1flist,m1clist,2,2,4,325,218,10,10)
m1=_m.Menu(1181,10,False,1526,248,m1blist)

m3nlist=('C','','','','','','','','','','','','','','','')
m3flist=(passer,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor,chooseColor)
m3clist=((0,0,0),(255,255,255),(128,128,128),(0,0,0),(0,0,255),(128,0,255),(255,0,255),(255,0,128),(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,0),(0,255,128),(0,255,255),(0,128,255))
m3blist=_b.buttonTableCreator(m3nlist,m3flist,m3clist,4,4,16,325,288,10,298)
tb1=_t.Trackbar(10,20,True,325,100,'Brush Size','screen',1,101,changeBrushSize,168)
tb2=_t.Trackbar(10,20,True,325,100,'Transparency','screen',0,256,changeBrushTransparency,58)
m3blist.append(tb1)
m3blist.append(tb2)
m3blist.extend(_b.buttonTableCreator(('Highlight','Doodle'),(highlightdoodleBF,highlightdoodleBF),((128,128,128),gray),1,2,2,345-20,62,10,10))
m3=_m.Menu(1181,258,False,1526,854,m3blist,False)

drawArea=_da.DrawingArea(10,10,False,1171,854,70)

s1mlist=(m1,m3,drawArea)
s1=_s.Screen(copy.copy(screenBlank),s1mlist)

tb1.setTrackbarScreen(s1)
tb2.setTrackbarScreen(s1)

overlayBlank=np.zeros((sysHeight,sysWidth,4),np.uint8)
overlayList.append(copy.copy(overlayBlank)[drawArea.y1:drawArea.y2,drawArea.x1:drawArea.x2])

overlayBrush=np.zeros_like(brush.image)

currentScreen=s1
cv2.setMouseCallback('screen',functionerMenu)
cv2.imshow('screen',currentScreen.background)

# screenCopy=copy.copy(currentScreen.background)
# while(1):
# 	cv2.imshow('screen',currentScreen.background)
# 	k = cv2.waitKey(1) & 0xFF
# 	if k == 27:
# 		break

moduleImage=cv2.imread('initial.jpg')
imageOpener(moduleImage)
controlFlag=True
final=None

while controlFlag==True:
	cv2.waitKey(1)















		
