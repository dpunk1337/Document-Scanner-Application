import cv2
import numpy as np 
import button as _b
import menu as _m
import screen as _s
import copy
import drawingArea as _d
import pydialog as pd
import documentDetector as _dd

sysWidth=1536
sysHeight=864
screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)+50
gray=(50,50,50)
currentScreen=None

loadFlag=None

cropImage=None
propImage=None
originalImage=None
bdownflag=False
circleRadius=40
pointList=list()
currentPointIndex=None

# cv2.namedWindow('screen',cv2.WINDOW_NORMAL)
mainMenuFlag=False
def quitToMainMenu(a,b,c,d):
	global controlFlag,mainMenuFlag
	mainMenuFlag=True
	controlFlag=False

def exitProgram(a,b,c,d):
	raise SystemExit

def next(a,b,c,d):
	global final,controlFlag
	controlFlag=False
	final=propImage

def save(a,b,c,d):
	global final
	final=propImage
	saveFileAddress=pd.saveFile()
	if saveFileAddress is not None:
		cv2.imwrite(saveFileAddress.name,final)

def rotate(a,b,c,d):
	global originalImage
	global propImage,loadFlag,propImage
	if loadFlag==True and m2_2.hidden:
		originalImage=cv2.transpose(originalImage)
		originalImage=cv2.flip(originalImage,1)
		propImage=cv2.transpose(propImage)
		propImage=cv2.flip(propImage,1)	
		drawArea.image=copy.copy(drawArea.blank)
		currentScreen.drawAMenu(drawArea)
		drawArea.setOriginalImage(propImage)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def done(a,b,c,d):
	global pointList,propImage,originalImage
	sets1m2_1()
	propImage=_dd.getWarped(copy.copy(originalImage),pointList)
	drawArea.image=copy.copy(drawArea.blank)
	currentScreen.drawAMenu(drawArea)
	drawArea.setOriginalImage(propImage)
	currentScreen.drawAMenu(drawArea)
	cv2.imshow('screen',currentScreen.background)

def sets1m2_1():
	currentScreen.hideAMenu(m2_2)
	currentScreen.unhideAMenu(m2_1)
	cv2.imshow('screen',currentScreen.background)

def sets1m2_2():
	currentScreen.hideAMenu(m2_1)
	currentScreen.unhideAMenu(m2_2)
	cv2.imshow('screen',currentScreen.background)

def map(n,x1,y1,x2,y2):
	return int((n*(y2-x2)/(y1-x1))+0.5)

def changePointCoordinates(x,y):
	global currentPoint,pointList,cropImage
	if currentPointIndex!=None:
		x=map(x,drawArea.imgX1,drawArea.imgX2,0,cropImage.shape[1])
		y=map(y,drawArea.imgY1,drawArea.imgY2,0,cropImage.shape[0])
		pointList[currentPointIndex][0]=x
		pointList[currentPointIndex][1]=y
		tl,tr,br,bl=pointList
		cropImage=copy.copy(originalImage)
		cropImage=drawRectangle(cropImage,tl,tr,br,bl)
		drawArea.updateEditImage(cropImage)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def insideCircle(x,y):
	global pointList,currentPointIndex,circleRadius,cropImage
	x=map(x,drawArea.imgX1,drawArea.imgX2,0,cropImage.shape[1])
	y=map(y,drawArea.imgY1,drawArea.imgY2,0,cropImage.shape[0])
	for i in range(4):
		xl=x-pointList[i][0]
		yl=y-pointList[i][1]
		if -circleRadius < xl < circleRadius:
			if -circleRadius < yl < circleRadius:
				currentPointIndex=i
				return True
	return False

def resizePoints(tl,tr,br,bl,im1shape,im2shape):
	ratioX=im2shape[1]/im1shape[1]
	ratioY=im2shape[0]/im1shape[0]
	tl[0]=int(tl[0]*ratioX)
	tr[0]=int(tr[0]*ratioX)
	br[0]=int(br[0]*ratioX)
	bl[0]=int(bl[0]*ratioX)
	tl[1]=int(tl[1]*ratioY)
	tr[1]=int(tr[1]*ratioY)
	br[1]=int(br[1]*ratioY)
	bl[1]=int(bl[1]*ratioY)


def drawRectangle(image,tl,tr,br,bl):
	global circleRadius,pointList
	cv2.line(image,(bl[0],bl[1]),(tl[0],tl[1]),(0,0,255),5)
	cv2.line(image,(tl[0],tl[1]),(tr[0],tr[1]),(0,0,255),5)
	cv2.line(image,(tr[0],tr[1]),(br[0],br[1]),(0,0,255),5)
	cv2.line(image,(br[0],br[1]),(bl[0],bl[1]),(0,0,255),5)
	cv2.circle(image,(bl[0],bl[1]),circleRadius,(0,170,255),9)
	cv2.circle(image,(tl[0],tl[1]),circleRadius,(0,170,255),9)
	cv2.circle(image,(tr[0],tr[1]),circleRadius,(0,170,255),9)
	cv2.circle(image,(br[0],br[1]),circleRadius,(0,170,255),9)
	return image


def crop(button,menu,mouseX,mouseY):
	global cropImage,pointList
	if loadFlag:
		sets1m2_2()

		cropImage=copy.copy(originalImage)
		tl,tr,br,bl=_dd.getPoints(originalImage)
		pointList=(tl,tr,br,bl)
		cropImage=drawRectangle(cropImage,tl,tr,br,bl)
		drawArea.image=copy.copy(drawArea.blank)
		currentScreen.drawAMenu(drawArea)
		drawArea.setOriginalImage(cropImage)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def open(button,menu,mouseX,mouseY):
	img=cv2.imread(pd.getFile())
	imageOpener(img)

def imageOpener(img):
	global originalImage
	global propImage,loadFlag
	global final
	if (img is not None):
		loadFlag=True
		originalImage=img
		propImage=_dd.getWarpedDocumentImage(img)
		final=propImage
		drawArea.image=copy.copy(drawArea.blank)
		currentScreen.drawAMenu(drawArea)
		drawArea.setOriginalImage(propImage)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def showXYpos(posX,posY):
	posX-=drawArea.imgX1+1
	posY-=drawArea.imgY1+1
	posX=str(posX)
	posY=str(posY)
	currentScreen.background[0:10,:]=np.zeros((10,sysWidth,3),np.uint8)+50
	cv2.putText(currentScreen.background,' X: '+posX+' Y: '+posY,(5,9),cv2.FONT_HERSHEY_SIMPLEX,.4,(255,255,255),1)
	cv2.imshow('screen',currentScreen.background)

def passer(button,menu,mouseX,mouseY):
	print((button.x1,button.y1),(button.x2,button.y2))
	print((menu.x1,menu.y1),(menu.x2,menu.y2))
	print(menu.width,menu.height)
	print(button.width,button.height)

def functionerMenu(event,x,y,flags,params):
	global bdownflag,currentPointIndex
	# global flag,bdownflag,flagg,editedImageIndex,editionList
	if drawArea.x1<x<drawArea.x2 and drawArea.y1<y<drawArea.y2:
		showXYpos(x,y)
			# flag=True
		if loadFlag==True:
			if(event==cv2.EVENT_LBUTTONDOWN):
				if insideCircle(x-drawArea.imgX1,y-drawArea.imgY1)==True:
					bdownflag=True
			elif(event==cv2.EVENT_MOUSEMOVE):
				if(bdownflag):
					changePointCoordinates(x-drawArea.imgX1,y-drawArea.imgY1)
			elif(event==cv2.EVENT_LBUTTONUP):
				bdownflag=False
				changePointCoordinates(x-drawArea.imgX1,y-drawArea.imgY1)
				currentPointIndex=None
	else:
		# if flag==True:
		# 	flag=False
		# 	cv2.imshow('screen',currentScreen.background)
		if(event==cv2.EVENT_LBUTTONDOWN):
			currentScreen.implementMenuFunction(x,y)


#screenList.append
m1nlist=('Main Menu','Next','Rotate')
m1flist=(quitToMainMenu,next,rotate)
m1clist=(gray,gray,gray)
m1blist=_b.buttonTableCreator(m1nlist,m1flist,m1clist,3,1,3,172-20,618,10,10)
m1=_m.Menu(1343+10,0+10,False,1536-10,638,m1blist)

m2_1=_m.Menu(1353,638,False,1526,854,_b.buttonTableCreator(('Crop',' '),(crop,passer),(gray,gray),1,1,1,152,206,10,0),False)
m2_2=_m.Menu(1353,638,False,1526,854,_b.buttonTableCreator(('Done','Reset'),(done,crop),(gray,gray),2,1,2,152,206,10,0),True)

drawArea=_d.DrawingArea(10,10,False,1343,854,70)

s1mlist=(m1,m2_1,m2_2,drawArea)
s1=_s.Screen(copy.copy(screenBlank),s1mlist)


currentScreen=s1
cv2.setMouseCallback('screen',functionerMenu)
cv2.imshow('screen',currentScreen.background)

# screenCopy=copy.copy(currentScreen.background)
# while(1):
# 	cv2.imshow('screen',currentScreen.background)
# 	k = cv2.waitKey(1) & 0xFF
# 	if k == 27:
# 		break

final=None
moduleImage=cv2.imread('initial.jpg')
imageOpener(moduleImage)
controlFlag=True


while controlFlag==True:
	cv2.waitKey(1)