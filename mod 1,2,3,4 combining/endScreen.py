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
final=cv2.imread('final.jpg')

def exitProgram(a,b,c,d):
	raise SystemExit

def save(a,b,c,d):
	saveFileAddress=pd.saveFile()
	if saveFileAddress is not None:
		cv2.imwrite(saveFileAddress.name,final)

def mainMenu(a,b,c,d):
	global controlFlag
	controlFlag=False


sysWidth,sysHeight=pd.getSysDimensions()
gray=(50,50,50)
# screenBlank=np.zeros((sysHeight,sysWidth,3),np.uint8)
folder='background/'
imageNames=('end (1).jpg','end (2).jpg','end (3).jpg','end (4).jpg','end (5).jpg','end (6).jpg')
chosenOne=random.choice(imageNames)
screenBlank=cv2.imread(folder+chosenOne)


def functionerMenu(event,x,y,flags,params):
	if(event==cv2.EVENT_LBUTTONDOWN):
		s1.implementMenuFunction(x,y)

m1=_m.Menu(568,282,False,968,582,_b.buttonTableCreator(('Save','Main Menu','Exit'),(save,mainMenu,exitProgram),(gray,gray,gray),3,1,3,380,280,10,10))
s1=_s.Screen(copy.copy(screenBlank),(m1,))
cv2.imshow('screen',s1.background)
cv2.setMouseCallback('screen',functionerMenu)

while controlFlag==True:
	cv2.waitKey(1)
