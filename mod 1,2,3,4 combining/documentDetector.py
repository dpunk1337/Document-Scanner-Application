import cv2
import numpy as np 
from math import sqrt

def getDistance(pt1,pt2):
	x1,y1=pt1
	x2,y2=pt2
	return sqrt(pow(x1-x2,2)+pow(y1-y2,2))

def arrangeFourPoints(points):
	rectangle=np.zeros((4,2),np.float32)

	summation=points.sum(axis=1)
	rectangle[0]=points[np.argmin(summation)]
	rectangle[2]=points[np.argmax(summation)]

	difference=np.diff(points,axis=1)
	rectangle[1]=points[np.argmin(difference)]
	rectangle[3]=points[np.argmax(difference)]

	return rectangle

def fourPointTransform(image,points):
	rectangle=arrangeFourPoints(points)
	tl,tr,br,bl=rectangle

	width1=getDistance(tl,tr)
	width2=getDistance(bl,br)
	maxWidth=max(int(width1),int(width2))

	height1=getDistance(tl,bl)
	height2=getDistance(tr,br)
	maxHeight=max(int(height1),int(height2))

	newPoints=np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0,maxHeight-1]],np.float32)
	perspectiveMatrix=cv2.getPerspectiveTransform(rectangle,newPoints)
	warped=cv2.warpPerspective(image,perspectiveMatrix,(maxWidth,maxHeight))

	return warped

def getDocumentContour(img):
	kernel=np.ones((3,3))
	H,W,_=img.shape
	area=H*W
	areaThreshold=area*0.8

	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gauss=cv2.GaussianBlur(gray,(5,5),3)
	canny=cv2.Canny(gauss,0,20)
	dilate=cv2.dilate(canny,kernel,iterations=2)

	_,cnts,_=cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:10]

	flag=False
	screenCnt=0

	for c in cnts:
		epsilon=cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c, 0.03*epsilon, True)
		approx=cv2.convexHull(approx)
		# cv2.namedWindow('coco',cv2.WINDOW_NORMAL)
		# edit=np.zeros_like(img)
		# cv2.drawContours(edit,[approx],-1,(0,255,0),3)
		# cv2.imshow('coco',edit)
		# cv2.waitKey(0)

		if len(approx)==4 and cv2.contourArea(c)<areaThreshold :
			screenCnt=approx
			flag=True
			break
	return screenCnt,flag


def highlightDocument(img):
	screenCnt,flag=getDocumentContour(img)
	if(flag):
		cv2.drawContours(img,[screenCnt],-1,(0,255,0),3)
	return img

def getWarpedDocumentImage(img):
	screenCnt,flag=getDocumentContour(img)
	if(flag):
		warped=fourPointTransform(img,screenCnt.reshape(4,2))
		return warped
	else:
		return img

def getPoints(img):
	screenCnt,flag=getDocumentContour(img)
	if(flag):
		rectangle=arrangeFourPoints(screenCnt.reshape(4,2))
		tl,tr,br,bl=rectangle
		return rectangle 
	else:
		return [[0,0],[0,0],[0,0],[0,0]]

def getWarped(img,pointList):
	points=np.zeros((4,2),np.float32)
	for i in range(4):
		points[i][0]=pointList[i][0]
		points[i][1]=pointList[i][1]

	warped=fourPointTransform(img,points)
	return warped










