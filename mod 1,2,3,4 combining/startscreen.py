import cv2
import numpy as np
import pydialog as pd
import copy
import menu as _m
import button as _b
import screen as _s
import random


moduleCaller=0
controlFlag=True
final=None

def exitProgram(a,b,c,d):
	raise SystemExit

def setModuletoZero(a,b,c,d):
	global moduleCaller,final,controlFlag
	final=cv2.imread(pd.getFile())
	if final is not None:
		moduleCaller=0
		controlFlag=False

def setModuletoOne(a,b,c,d):
	global moduleCaller,final,controlFlag
	final=cv2.imread(pd.getFile())
	if final is not None:	
		moduleCaller=1
		controlFlag=False


sysHeight=864
sysWidth=1536
gray=(50,50,50)
# screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)
folder='background/'
imageNames=('start (1).jpg','start (2).jpg','start (3).jpg','start (4).jpg','start (5).jpg','start (6).jpg')
chosenOne=random.choice(imageNames)
screenBlank=cv2.imread(folder+chosenOne)


def functionerMenu(event,x,y,flags,params):
	if(event==cv2.EVENT_LBUTTONDOWN):
		s1.implementMenuFunction(x,y)

m1=_m.Menu(568,282,False,968,582,_b.buttonTableCreator(('Document Perspective Corrector','Image QR code detector','Exit'),(setModuletoZero,setModuletoOne,exitProgram),(gray,gray,gray),3,1,3,380,280,10,10))
s1=_s.Screen(copy.copy(screenBlank),(m1,))
cv2.imshow('screen',s1.background)
cv2.setMouseCallback('screen',functionerMenu)

while controlFlag==True:
	cv2.waitKey(1)
