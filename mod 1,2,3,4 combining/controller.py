import cv2
import numpy as np
import pydialog as pd 
import importlib


startscreen=None
mod2_v3=None
mod3_v3=None
mod1_v2=None
mod4=None
endScreen=None

cv2.namedWindow('screen',cv2.WINDOW_NORMAL)
cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, 1)

while(1):
	if startscreen is not None:
		importlib.reload(startscreen)
	else:
		import startscreen
	moduleCaller=startscreen.moduleCaller
	initial=startscreen.final
	cv2.imwrite('initial.jpg',initial)

	if moduleCaller==0:
		if mod2_v3 is not None:
			importlib.reload(mod2_v3)
		else:
			import mod2_v3
		if mod2_v3.mainMenuFlag==True:
			continue
		initial=mod2_v3.final
		cv2.imwrite('initial.jpg',initial)
		if mod3_v3 is not None:
			importlib.reload(mod3_v3)
		else:
			import mod3_v3
		if mod3_v3.mainMenuFlag==True:
			continue
		initial=mod3_v3.final
		cv2.imwrite('initial.jpg',initial)
		if mod1_v2 is not None:
			importlib.reload(mod1_v2)
		else:
			import mod1_v2
		if mod1_v2.mainMenuFlag==True:
			continue
		final=mod1_v2.final
		cv2.imwrite('final.jpg',final)
		if endScreen is not None:
			importlib.reload(endScreen)
		else:
			import endScreen
	else:
		if mod4 is not None:
			importlib.reload(mod4)
		else:
			import mod4


