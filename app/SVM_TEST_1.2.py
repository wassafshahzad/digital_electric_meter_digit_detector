import sys
import numpy as np
import cv2

##Main function
def extract(contours,i):
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if (w>h and w>128):
                r=i[y:y+h,x:x+w]
                p=cv2.resize(r,(512,256))
                f=hog1.compute(p)
                f=f.reshape(1,f.shape[0])
                if (svm.predict(np.float32(f))[1].ravel()[0] == 1):
                    ar=image[y:y+h,x:x+w]
                    cv2.imwrite('result\\1.jpg',ar)
                    print("yes")
                    sys.stdout.flush()
                    return
    print("Fail",file=sys.stderr) 


winSize = (512,256)
blockSize = (32,16)
blockStride = (16,8)
cellSize = (16,8)
nbins = 9
derivAperture = 1
winSigma = -1.
histogramNormType = 0
L2HysThreshold = 0.2
gammaCorrection = 1
nlevels = 64
signedGradients = True
  
  
 #Hog 
hog1 = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels,signedGradients)
svm = cv2.ml.SVM_create()
svm=cv2.ml.SVM_load("C:\\Users\\wassaf\\Desktop\\CV\\meter_svm_model2.yml")
svmvec = svm.getSupportVectors()[0]
rho = -svm.getDecisionFunction(0)[0]
svmvec = np.append(svmvec, rho)
hog1.setSVMDetector(svmvec)
 
#Precrocessing
image=cv2.imread(r"{}".format(sys.argv[1]))
image=cv2.resize(image,(512,256))
i = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
th5= cv2.adaptiveThreshold(i,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,7)
im2, contours, hierarchy = cv2.findContours(th5,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
extract(contours,i)

                        



