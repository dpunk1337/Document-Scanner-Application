import cv2
import numpy as np

def Canny(img,th1,th2):
	img=cv2.Canny(img,th1,th2)
	img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
	return img

def Sobel(img):
	sobelKernel1=np.array(([-1,-2,-1],[0,0,0],[1,2,1]))
	sobelKernel2=np.array(([1,2,1],[0,0,0],[-1,-2,-1]))
	edit1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	sy1=cv2.filter2D(edit1,-1,sobelKernel1)
	sx1=cv2.filter2D(edit1,-1,np.transpose(sobelKernel1))
	sy2=cv2.filter2D(edit1,-1,sobelKernel2)
	sx2=cv2.filter2D(edit1,-1,np.transpose(sobelKernel2))
	edit1=cv2.add(sx1,sx2)
	edit2=cv2.add(sy1,sy2)
	edit=cv2.add(edit1,edit2)
	edit=cv2.cvtColor(edit,cv2.COLOR_GRAY2RGB)
	return edit


def Prewitt(img):
	sobelKernel1=np.array(([-1,-1,-1],[0,0,0],[1,1,1]))
	sobelKernel2=np.array(([1,1,1],[0,0,0],[-1,-1,-1]))
	edit1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	sy1=cv2.filter2D(edit1,-1,sobelKernel1)
	sx1=cv2.filter2D(edit1,-1,np.transpose(sobelKernel1))
	sy2=cv2.filter2D(edit1,-1,sobelKernel2)
	sx2=cv2.filter2D(edit1,-1,np.transpose(sobelKernel2))
	edit1=cv2.add(sx1,sx2)
	edit2=cv2.add(sy1,sy2)
	edit=cv2.add(edit1,edit2)
	edit=cv2.cvtColor(edit,cv2.COLOR_GRAY2RGB)
	return edit

def Robert(img):
	robertKernel1=np.array(([1,0],[0,-1]))
	robertKernel2=np.array(([0,1],[-1,0]))
	robertKernel3=np.array(([-1,0],[0,1]))
	robertKernel4=np.array(([0,-1],[1,0]))
	edit1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	sy1=cv2.filter2D(edit1,-1,robertKernel1)
	sy2=cv2.filter2D(edit1,-1,robertKernel2)
	sx1=cv2.filter2D(edit1,-1,robertKernel3)
	sx2=cv2.filter2D(edit1,-1,robertKernel4)
	edit1=cv2.add(sy1,sy2)
	edit2=cv2.add(sx1,sx2)
	edit=cv2.add(edit1,edit2)
	edit=cv2.cvtColor(edit,cv2.COLOR_GRAY2RGB)
	return edit

#################################################################################################	
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################		

def Averaging(img,nK):
	return cv2.blur(img,(nK,nK))

def Gaussian(img,nK):
	return cv2.GaussianBlur(img,(nK,nK),20)

def Median(img,nK):
	return cv2.medianBlur(img,nK)

def Bilateral(img,nK):
	return cv2.bilateralFilter(img,nK,75,75)
#################################################################################################	
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################	

def Brightness(img,value):
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	if(value < 256):
		value=255-value
		lim=value
		v[v<lim]=0
		v[v>=lim]-=value
	else:
		value=value-256
		lim = 255 - value
		v[v > lim] = 255
		v[v <= lim] += value
		
	final_hsv = cv2.merge((h, s, v))
	edit = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return edit

def Hue(img,value):
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	lim = 179-value
	h[h >lim]-=np.uint8(lim)
	h[h <= lim] += value
	final_hsv = cv2.merge((h, s, v))
	edit = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return edit

def Saturation(img,value):
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	if(value < 256):
		value=255-value
		lim=value
		s[s<lim]=0
		s[s>=lim]-=value
	else:
		value=value-256
		lim = 255 - value
		s[s > lim] = 255
		s[s <= lim] += value
	final_hsv = cv2.merge((h, s, v))
	edit = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	return edit

def HistogramEqualization(img):
	b,g,r=cv2.split(img)
	b=cv2.equalizeHist(b)
	g=cv2.equalizeHist(g)
	r=cv2.equalizeHist(r)
	return cv2.merge((b,g,r))

def Negative(img):
	b,g,r=cv2.split(img)
	l=np.zeros_like(b)+255
	return cv2.merge((l-b,l-g,l-r))

def GrayScale(img):
	return(cv2.cvtColor(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR))

#################################################################################################	
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

def Laplacian(img):
	kernel=np.array(([0,1,0],[1,-4,1],[0,1,0]))
	edit=cv2.filter2D(img,-1,kernel)
	img=cv2.subtract(img,edit)
	return img

def Common(img):
	kernel=np.array(([-1,-1,-1],[-1,9,-1],[-1,-1,-1]))
	edit=cv2.filter2D(img,-1,kernel)
	img=cv2.subtract(img,edit)
	return edit

#################################################################################################	
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
def Gauss(image):
	row,col,ch= image.shape
	mean = 0
	var = 0.02
	sigma = 0.9
	gauss = np.random.normal(mean,sigma,(row,col,ch))
	gauss = gauss.reshape(row,col,ch)
	noisy = image + gauss
	noisy=noisy.astype(np.uint8)
	return noisy

def SaltnPepper(image):
	row,col,ch = image.shape
	s_vs_p = 0.5
	amount = 0.004
	out = np.copy(image)
	# Salt mode
	num_salt = np.ceil(amount * image.size * s_vs_p)
	coords = [np.random.randint(0, i - 1, int(num_salt))
	      for i in image.shape]
	out[coords] = 1
	# Pepper mode
	num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
	coords = [np.random.randint(0, i - 1, int(num_pepper))
	      for i in image.shape]
	out[coords] = 0
	return out

def Poisson(image):
	vals = len(np.unique(image))
	vals = 2 ** np.ceil(np.log2(vals))
	noisy = np.random.poisson(image * vals) / float(vals)
	return noisy

def Speckle(image):
	row,col,ch = image.shape
	gauss = np.random.randn(row,col,ch)
	gauss = gauss.reshape(row,col,ch)        
	noisy = image + image * gauss * 0.08
	noisy=noisy.astype(np.uint8)
	return noisy

def Denoise(img):
	return cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
