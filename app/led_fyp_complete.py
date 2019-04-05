import cv2
import numpy as np
from ftp import four_point_transform
from hg import hog
import sys
import os
image = cv2.imread(r"{}".format(sys.argv[1]))

#print(image)
hog1,svm=hog()
# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge mapr
def pre_process(image):
    image = cv2.resize(image,(1024,512))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    
#sd,kil=cv2.threshold ( gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU );
#cv2.imshow("Canyy",kil)
    im2, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours,gray,image


def extract_led(image):
    contours,gray,image=pre_process(image)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if (w>256 and w>h ):
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)     
            warped = four_point_transform(gray,box.reshape(4, 2))
            val =   four_point_transform(image,box.reshape(4, 2))
            p=cv2.resize(warped,(1024,512))
            f=hog1.compute(p)
            f=f.reshape(1,f.shape[0])
            svm.predict(np.float32(f))[1].ravel()[0]
            #print(svm.predict(np.float32(f))[1].ravel()[0])
            if (svm.predict(np.float32(f))[1].ravel()[0] == 1):
                war=cv2.resize(val,(512,128))
                cv2.imwrite('result\\1.jpg',war)
                print("yes")
                sys.stdout.flush()
                return
                
    print("Fail",file=sys.stderr)
        
            #print(svm.predict(np.float32(f))[1].ravel()[0]):
        
                    
extract_led(image)
