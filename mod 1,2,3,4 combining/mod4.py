import cv2
import numpy as np 
import pydialog as pd
import button as _b
import menu as _m
import screen as _s
import copy
import drawingArea as _d
import pyperclip
from pyzbar import pyzbar

# sysWidth=1536
# sysHeight=864

sysWidth,sysHeight=pd.getSysDimensions()
screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)+50
gray=(50,50,50)

bdownflag=False
loadFlag=False
originalImage=None

barcodes=None
barcodeDataList=list()
currentBarcode=None

mainMenuFlag=False
def quitToMainMenu(a,b,c,d):
	global controlFlag,mainMenuFlag
	mainMenuFlag=True
	controlFlag=False

def eraseText():
	s1.drawAMenu(m1)

def drawGreenRectangle():
	global currentBarcode,barcodes
	img=drawArea.editedImage
	for barcode in barcodes:
		(x,y,w,h)=barcode.rect
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
	if currentBarcode is not None:
		(x,y,w,h)=currentBarcode.rect
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	drawArea.updateEditImage(img)
	currentScreen.drawAMenu(drawArea)
	cv2.imshow('screen',currentScreen.background)

def copyData(a,b,c,d):
	global currentBarcode
	if currentBarcode is not None:
		barcodeData=currentBarcode.data.decode('utf-8')
		pyperclip.copy(barcodeData)

def cropText(text):
	if len(text)>110:
		text=text[:100]
		text=text+'....'
	return text

def showBarcodeData(_x,_y):
	global barcodes,currentBarcode
	h=drawArea.imgY2-drawArea.imgY1
	w=drawArea.imgX2-drawArea.imgX1
	x=int(_x*originalImage.shape[1]/w)
	y=int(_y*originalImage.shape[0]/h)
	showBarcode=None
	for barcode in barcodes:
		(xx,yy,ww,hh)=barcode.rect
		if xx < x < xx+ww:
			if yy< y <yy+hh:
				showBarcode=barcode
	currentBarcode=showBarcode
	drawGreenRectangle()
	showABarcode(currentBarcode)

def showABarcode(barcode):
	if barcode is not None:
		eraseText()
		barcodeData=barcode.data.decode('utf-8')
		barcodeType=barcode.type 
		text="{}".format(barcodeData)
		text=cropText(text)
		cv2.putText(currentScreen.background,text,(330,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
		cv2.imshow('screen',currentScreen.background)
	else:
		# cv2.putText(image,text, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
		eraseText()
		cv2.putText(currentScreen.background,"Please click one of the red box to see the data here and press Copy Data button to copy it to clipboard.", (325,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
		cv2.imshow('screen',currentScreen.background)


def drawBarcodes(image):
	global barcodes,barcodeDataList
	barcodes=pyzbar.decode(image)
	for barcode in barcodes:
		(x,y,w,h)=barcode.rect
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)

		barcodeData=barcode.data.decode('utf-8')
		barcodeType=barcode.type 
		barcodeDataList.append(barcodeData)

		text="{} ({})".format(barcodeData, barcodeType)
		drawArea.updateEditImage(image)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def imageOpener(img):
	global originalImage
	global loadFlag
	global final
	if (img is not None):
		loadFlag=True
		originalImage=img
		final=None
		drawArea.image=copy.copy(drawArea.blank)
		currentScreen.drawAMenu(drawArea)
		drawArea.setOriginalImage(img)
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def functionerMenu(event,x,y,flags,params):
	global bdownflag
	if drawArea.x1<x<drawArea.x2 and drawArea.y1<y<drawArea.y2:
		if loadFlag==True:
			if(event==cv2.EVENT_LBUTTONDOWN):
				showBarcodeData(x-drawArea.imgX1,y-drawArea.imgY1)
	else:
		if(event==cv2.EVENT_LBUTTONDOWN):
			currentScreen.implementMenuFunction(x,y)


m1=_m.Menu(10,10,False,1526,60,_b.buttonTableCreator(('Main Menu','Copy Data'),(quitToMainMenu,copyData),(gray,gray),1,10,2,1506,40,5,5),False)
drawArea=_d.DrawingArea(10,70,False,1526,854,5)
s1mlist=(m1,drawArea)
s1=_s.Screen(copy.copy(screenBlank),s1mlist)

currentScreen=s1
cv2.setMouseCallback('screen',functionerMenu)
cv2.imshow('screen',currentScreen.background)

final=None
# img=cv2.imread('image.jpg')
# imageOpener(img)
moduleImage=cv2.imread('initial.jpg')
imageOpener(moduleImage)
controlFlag=True
drawBarcodes(copy.copy(originalImage))
showABarcode(None)

while controlFlag==True:
	cv2.waitKey(1)



