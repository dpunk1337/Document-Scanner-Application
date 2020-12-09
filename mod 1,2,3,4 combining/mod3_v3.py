import cv2
import numpy as np
import pydialog as pd
import copy
import menu as _m
import button as _b
import screen as _s
import drawingArea as _da
import trackbar as _t
import imgfunctions as _imfu
import dialog as _dlg

# cv2.namedWindow('screen',cv2.WINDOW_NORMAL)
gray=(50,50,50)
sysWidth,sysHeight=pd.getSysDimensions()
screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)+50

backList=list()
backListIndex=0

editionList=list()
editedImageIndex=0

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
	final=drawArea.editedImage

def save(a,b,c,d):
	global final
	final=drawArea.editedImage
	saveFileAddress=pd.saveFile()
	if saveFileAddress is not None:
		cv2.imwrite(saveFileAddress.name,final)

def back(a,menu,c,d):
	global backList,backListIndex
	if backListIndex>0:
		backListIndex-=1
		currentScreen.hideAMenu(menu)
		currentScreen.unhideAMenu(backList[backListIndex])
		backList.pop(backListIndex)
		cv2.imshow('screen',currentScreen.background)	

def okay(a,menu,c,d):
	back(a,menu,c,d)
	menu.resetTrackbars()
	m1.hidden=False

def cancel(a,menu,c,d):
	global editionList,editedImageIndex
	undo(a,menu,c,d)
	editionList.pop(editedImageIndex+1)
	menu.resetTrackbars()
	back(a,menu,c,d)
	m1.hidden=False

def redo(a,b,c,d):
	global editionList,editedImageIndex
	if editedImageIndex < len(editionList)-1:
		editedImageIndex+=1
		drawArea.updateEditImage(editionList[editedImageIndex])
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def undo(a,b,c,d):
	global editionList,editedImageIndex
	if(editedImageIndex>0):
		editedImageIndex-=1
		drawArea.updateEditImage(editionList[editedImageIndex])
		currentScreen.drawAMenu(drawArea)
		cv2.imshow('screen',currentScreen.background)

def open(a,b,c,d):
	global editionList,editedImageIndex
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
		editionList.append(drawArea.editedImage)

		m3.hidden=False	

def functionCommon(menu,dialog):
	global backList,backListIndex
	currentScreen.hideAMenu(menu)
	currentScreen.unhideAMenu(dialog)
	cv2.imshow('screen',currentScreen.background)
	backList.append(menu)
	backListIndex+=1
	m1.hidden=True

def drawAreaChangeShow(img):
	global editedImageIndex,editionList
	drawArea.updateEditImage(img)
	currentScreen.drawAMenu(drawArea)
	cv2.imshow('screen',currentScreen.background)

	editedImageIndex+=1
	if editedImageIndex < len(editionList):
		del editionList[editedImageIndex:]
	editionList.append(drawArea.editedImage)

def tbCommon(img):
	global editedImageIndex,editionList
	drawArea.updateEditImage(img)
	currentScreen.drawAMenu(drawArea)
	editionList[editedImageIndex]=img
	cv2.imshow('screen',currentScreen.background)

def cannyTbFunction(number):
	global editedImageIndex,editionList
	th1=cannyDialog.trackbarList[0].number
	th2=cannyDialog.trackbarList[1].number
	img=_imfu.Canny(editionList[editedImageIndex-1],th1,th2)
	tbCommon(img)

def canny(a,menu,c,d):
	functionCommon(menu,cannyDialog)
	img=_imfu.Canny(drawArea.editedImage,0,0)
	drawAreaChangeShow(img)

def sobel(a,menu,c,d):
	functionCommon(menu,sobelDialog)
	img=_imfu.Sobel(drawArea.editedImage)
	drawAreaChangeShow(img)

def prewitt(a,menu,c,d):
	functionCommon(menu,prewittDialog)
	img=_imfu.Prewitt(drawArea.editedImage)
	drawAreaChangeShow(img)

def robert(a,menu,c,d):
	functionCommon(menu,robertDialog)
	img=_imfu.Robert(drawArea.editedImage)
	drawAreaChangeShow(img)

def averagingTbFunction(number):
	global editedImageIndex,editionList
	k=(2*number)+1
	img=_imfu.Averaging(editionList[editedImageIndex-1],k)
	tbCommon(img)
def averaging(a,menu,c,d):
	functionCommon(menu,averagingDialog)
	img=_imfu.Averaging(drawArea.editedImage,1)
	drawAreaChangeShow(img)

def gaussianTbFunction(number):
	global editedImageIndex,editionList
	k=(2*number)+1
	img=_imfu.Gaussian(editionList[editedImageIndex-1],k)
	tbCommon(img)
def gaussian(a,menu,c,d):
	functionCommon(menu,gaussianDialog)
	img=_imfu.Gaussian(drawArea.editedImage,1)
	drawAreaChangeShow(img)

def medianTbFunction(number):
	global editedImageIndex,editionList
	if number>33:
		number=33
	k=(2*number)+1
	img=_imfu.Median(editionList[editedImageIndex-1],k)
	tbCommon(img)
def median(a,menu,c,d):
	functionCommon(menu,medianDialog)
	img=_imfu.Median(drawArea.editedImage,1)
	drawAreaChangeShow(img)

def bilateralTbFunction(number):
	global editedImageIndex,editionList
	if number>19:
		number=19
	k=(2*number)+1
	img=_imfu.Bilateral(editionList[editedImageIndex-1],k)
	tbCommon(img)
def bilateral(a,menu,c,d):
	functionCommon(menu,bilateralDialog)
	img=_imfu.Bilateral(drawArea.editedImage,1)
	drawAreaChangeShow(img)

def brightnessTbFunction(number):
	global editedImageIndex,editionList
	k=int(number*5.12)
	img=_imfu.Brightness(editionList[editedImageIndex-1],k)
	tbCommon(img)
def brightness(a,menu,c,d):
	functionCommon(menu,brightnessDialog)
	img=_imfu.Brightness(drawArea.editedImage,0)
	drawAreaChangeShow(img)

def hueTbFunction(number):
	global editedImageIndex,editionList
	k=int(number*1.80)
	img=_imfu.Hue(editionList[editedImageIndex-1],k)
	tbCommon(img)
def hue(a,menu,c,d):
	functionCommon(menu,hueDialog)
	img=_imfu.Hue(drawArea.editedImage,0)
	drawAreaChangeShow(img)

def saturationTbFunction(number):
	global editedImageIndex,editionList
	k=int(number*5.12)
	img=_imfu.Saturation(editionList[editedImageIndex-1],k)
	tbCommon(img)
def saturation(a,menu,c,d):
	functionCommon(menu,saturationDialog)
	img=_imfu.Saturation(drawArea.editedImage,0)
	drawAreaChangeShow(img)

def histEqualize(a,menu,c,d):
	functionCommon(menu,histEqualizeDialog)
	img=_imfu.HistogramEqualization(drawArea.editedImage)
	drawAreaChangeShow(img)

def negative(a,menu,c,d):
	functionCommon(menu,negativeDialog)
	img=_imfu.Negative(drawArea.editedImage)
	drawAreaChangeShow(img)

def grayScale(a,menu,c,d):
	functionCommon(menu,grayScaleDialog)
	img=_imfu.GrayScale(drawArea.editedImage)
	drawAreaChangeShow(img)

def laplacian(a,menu,c,d):
	functionCommon(menu,laplacianDialog)
	img=_imfu.Laplacian(drawArea.editedImage)
	drawAreaChangeShow(img)

def common(a,menu,c,d):
	functionCommon(menu,commonDialog)
	img=_imfu.Common(drawArea.editedImage)
	drawAreaChangeShow(img)

def gauss(a,menu,c,d):
	functionCommon(menu,gaussDialog)
	img=_imfu.Gauss(drawArea.editedImage)
	drawAreaChangeShow(img)

def saltnpepper(a,menu,c,d):
	functionCommon(menu,saltnpepperDialog)
	img=_imfu.SaltnPepper(drawArea.editedImage)
	drawAreaChangeShow(img)

def speckle(a,menu,c,d):
	functionCommon(menu,speckleDialog)
	img=_imfu.Speckle(drawArea.originalImage)
	drawAreaChangeShow(img)

def denoise(a,menu,c,d):
	functionCommon(menu,denoiseDialog)
	img=_imfu.Denoise(drawArea.originalImage)
	drawAreaChangeShow(img)

def setm3tom4(a,b,c,d):
	global backList,backListIndex
	currentScreen.hideAMenu(m3)
	currentScreen.unhideAMenu(m4)
	cv2.imshow('screen',currentScreen.background)
	backList.append(m3)
	backListIndex+=1

def setm3tom5(a,b,c,d):
	global backList,backListIndex
	currentScreen.hideAMenu(m3)
	currentScreen.unhideAMenu(m5)
	cv2.imshow('screen',currentScreen.background)
	backList.append(m3)
	backListIndex+=1

def setm3tom6(a,b,c,d):
	global backList,backListIndex
	currentScreen.hideAMenu(m3)
	currentScreen.unhideAMenu(m6)
	cv2.imshow('screen',currentScreen.background)
	backList.append(m3)
	backListIndex+=1

def setm3tom7(a,b,c,d):
	global backList,backListIndex
	currentScreen.hideAMenu(m3)
	currentScreen.unhideAMenu(m7)
	cv2.imshow('screen',currentScreen.background)
	backList.append(m3)
	backListIndex+=1

def setm3tom8(a,b,c,d):
	global backList,backListIndex
	currentScreen.hideAMenu(m3)
	currentScreen.unhideAMenu(m8)
	cv2.imshow('screen',currentScreen.background)
	backList.append(m3)
	backListIndex+=1


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

def functionerMenu(event,x,y,flags,params):
	if drawArea.x1<x<drawArea.x2:
		if drawArea.y1<y<drawArea.y2:
			showXYpos(x,y)
	else:
		if(event==cv2.EVENT_LBUTTONDOWN):
			currentScreen.implementMenuFunction(x,y)



m1nlist=('Main Menu','Next','Undo','Redo')
m1flist=(quitToMainMenu,next,undo,redo)
m1clist=(gray,gray,gray,gray)
m1blist=_b.buttonTableCreator(m1nlist,m1flist,m1clist,2,2,4,325,218,10,10)
m1=_m.Menu(1181,10,False,1526,248,m1blist)


# tb1=_t.Trackbar(10,20,True,325,100,'Brush Size','screen',1,101,changeBrushSize,168)
# tb2=_t.Trackbar(10,20,True,325,100,'Transparency','screen',0,256,changeBrushTransparency,58)
# m3blist.append(tb1)
# m3blist.append(tb2)

# ('Edge Detection','Smoothing','Spatial','Sharpening','Noise','Back','','')
mclist=(gray,gray,gray,gray,gray,gray,gray,gray)

m3nlist=('Edge Detection','Smoothing','Spatial','Sharpening','Noise',' ',' ',' ')
m3flist=(setm3tom4,setm3tom5,setm3tom6,setm3tom7,setm3tom8,passer,passer,passer)
m3blist=_b.buttonTableCreator(m3nlist,m3flist,mclist,8,1,5,325,576,10,10)
m3=_m.Menu(1181,258,False,1526,854,m3blist,False)

m4nlist=('Canny','Sobel','Prewitt','Robert','Back',' ',' ',' ',' ')
m4flist=(canny,sobel,prewitt,robert,back,passer,passer,passer)
m4blist=_b.buttonTableCreator(m4nlist,m4flist,mclist,8,1,5,325,576,10,10)
m4=_m.Menu(1181,258,False,1526,854,m4blist,True)

m5nlist=('Averaging','Gaussian','Median','Bilateral','Back',' ',' ',' ')
m5flist=(averaging,gaussian,median,bilateral,back,passer,passer,passer)
m5blist=_b.buttonTableCreator(m5nlist,m5flist,mclist,8,1,5,325,576,10,10)
m5=_m.Menu(1181,258,False,1526,854,m5blist,True)

m6nlist=('Brightness','Hue','Saturation','Hist Equalize','Negative','Gray','Back',' ')
m6flist=(brightness,hue,saturation,histEqualize,negative,grayScale,back,passer)
m6blist=_b.buttonTableCreator(m6nlist,m6flist,mclist,8,1,7,325,576,10,10)
m6=_m.Menu(1181,258,False,1526,854,m6blist,True)

m7nlist=('Laplacian','Common','Back',' ',' ',' ',' ',' ')
m7flist=(laplacian,common,back,passer,passer,passer,passer,passer)
m7blist=_b.buttonTableCreator(m7nlist,m7flist,mclist,8,1,3,325,576,10,10)
m7=_m.Menu(1181,258,False,1526,854,m7blist,True)

m8nlist=('Gauss','SaltnPepper','Speckle','Denoise','Back',' ',' ',' ')
m8flist=(gauss,saltnpepper,speckle,denoise,back,passer,passer,passer)
m8blist=_b.buttonTableCreator(m8nlist,m8flist,mclist,8,1,5,325,576,10,10)
m8=_m.Menu(1181,258,False,1526,854,m8blist,True)

drawArea=_da.DrawingArea(10,10,False,1171,854,70)

#(self,x1,y1,WH,wx2,hy2,nTabs,ntb,varnamelist,hidden=False)
dialogList=list()
_dlg.Dialog.cancelFunction=cancel
_dlg.Dialog.okayFunction=okay
cannyDialog=_dlg.Dialog(1181,258,False,1526,854,4,2,('th1','th2'),(cannyTbFunction,cannyTbFunction),True)
sobelDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
prewittDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
robertDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)

averagingDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Strength',),(averagingTbFunction,),True)
gaussianDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Strength',),(gaussianTbFunction,),True)
medianDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Strength',),(medianTbFunction,),True)
bilateralDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Strength',),(bilateralTbFunction,),True)
brightnessDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Brightness',),(brightnessTbFunction,),True)
hueDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Hue',),(hueTbFunction,),True)
saturationDialog=_dlg.Dialog(1181,258,False,1526,854,4,1,('Saturation',),(saturationTbFunction,),True)

histEqualizeDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
negativeDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
grayScaleDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
laplacianDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
commonDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
gaussDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
saltnpepperDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
speckleDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)
denoiseDialog=_dlg.Dialog(1181,258,False,1526,854,4,0,(''),(''),True)

dialogList.extend((cannyDialog,sobelDialog,prewittDialog,robertDialog))
dialogList.extend((averagingDialog,gaussianDialog,medianDialog,bilateralDialog))
dialogList.extend((brightnessDialog,hueDialog,saturationDialog,histEqualizeDialog,negativeDialog,grayScaleDialog))
dialogList.extend((laplacianDialog,commonDialog))
dialogList.extend((gaussDialog,saltnpepperDialog,speckleDialog,denoiseDialog))

s1mlist=list()
s1mlist.extend((m1,m3,m4,m5,m6,m7,m8,drawArea))
s1mlist.extend(dialogList)
s1=_s.Screen(copy.copy(screenBlank),s1mlist)

cannyDialog.setTrackbarScreen(s1)
averagingDialog.setTrackbarScreen(s1)
gaussianDialog.setTrackbarScreen(s1)
medianDialog.setTrackbarScreen(s1)
bilateralDialog.setTrackbarScreen(s1)
brightnessDialog.setTrackbarScreen(s1)
hueDialog.setTrackbarScreen(s1)
saturationDialog.setTrackbarScreen(s1)

currentScreen=s1
m3.hidden=True
cv2.setMouseCallback('screen',functionerMenu)
cv2.imshow('screen',currentScreen.background)



moduleImage=cv2.imread('initial.jpg')
imageOpener(moduleImage)
controlFlag=True
final=None

while controlFlag==True:
	cv2.waitKey(1)
