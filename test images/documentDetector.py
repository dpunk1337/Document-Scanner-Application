import cv2
import numpy as np 
from math import sqrt

def houghP(img):
	maxLine=img.shape[0]//3
	minGap=100
	linesP = cv2.HoughLinesP(img, 1, np.pi / 180, 200, None, maxLine, minGap)
	if linesP is not None:
		for i in range(0, len(linesP)):
			l = linesP[i][0]
			cv2.line(img, (l[0], l[1]), (l[2], l[3]), (255), 1, cv2.LINE_AA)

	return img

def hough(img):
	lines = cv2.HoughLines(img,1,np.pi/180, 250) 
	for line in lines: 
		r,theta=line[0]
		a = np.cos(theta) 
		b = np.sin(theta) 
		x0 = a*r 
		y0 = b*r 
		x1 = int(x0 + 3000*(-b)) 
		y1 = int(y0 + 3000*(a))  
		x2 = int(x0 - 3000*(-b)) 
		y2 = int(y0 - 3000*(a)) 
		cv2.line(img,(x1,y1), (x2,y2), (255),2) 

	return img

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
	gauss=cv2.GaussianBlur(gray,(5,5),0)
	canny=cv2.Canny(gauss,20,40)

	dilate=houghP(canny)
	dilate=cv2.dilate(dilate,kernel,iterations=2)
	cv2.imwrite('dilate.jpg',dilate)
	cv2.imshow('window',dilate)
	cv2.waitKey(0)

	cnts,_=cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:5]

	flag=False
	screenCnt=0

	for c in cnts:
		epsilon=0.08*cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c, epsilon, True)

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


cv2.namedWindow('window',cv2.WINDOW_NORMAL)
img=cv2.imread('receipt.jpg')
edit=getWarpedDocumentImage(img)
cv2.imshow('window',edit)
cv2.waitKey(0)








