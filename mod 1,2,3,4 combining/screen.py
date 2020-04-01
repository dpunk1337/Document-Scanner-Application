import numpy as np 
import cv2

class Screen:
	def __init__(self,image,menuList):
		self.menuList=menuList
		self.background=image
		self.drawMenus()

	def drawMenus(self):
		for menu in self.menuList:
			if(menu.hidden==False):
				x1=menu.x1
				y1=menu.y1
				x2=menu.x2
				y2=menu.y2
				self.background[y1:y2,x1:x2]=menu.image
	
	def drawAMenu(self,menu):
		if(menu.hidden==False):
			x1=menu.x1
			y1=menu.y1
			x2=menu.x2
			y2=menu.y2
			self.background[y1:y2,x1:x2]=menu.image


	def implementMenuFunction(self,mouse_x,mouse_y):
		for menu in self.menuList:
			if(menu.hidden==False):
				x1=menu.x1
				y1=menu.y1
				x2=menu.x2
				y2=menu.y2
				if x1<mouse_x<x2 :
					if y1<mouse_y<y2 :
						menu.implementButtonFunction(mouse_x,mouse_y)
						break;

	def hideAMenu(self,menu):
		x1=menu.x1
		y1=menu.y1
		x2=menu.x2
		y2=menu.y2
		self.background[y1:y2,x1:x2]=np.zeros((menu.height,menu.width,3),np.uint8)+50
		menu.hidden=True

	def unhideAMenu(self,menu):
		x1=menu.x1
		y1=menu.y1
		x2=menu.x2
		y2=menu.y2
		self.background[y1:y2,x1:x2]=menu.image 
		menu.hidden=False
