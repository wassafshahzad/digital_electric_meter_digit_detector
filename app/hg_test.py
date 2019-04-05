import cv2
import numpy as np




winSize = (512,256)
blockSize = (32,16)
blockStride = (16,8)
cellSize = (16,8)
nbins = 18
derivAperture = 1
winSigma = -1.
histogramNormType = 0
L2HysThreshold = 0.2
gammaCorrection = 1
nlevels = 64
signedGradients = True
  
def hog():  
    hog1 = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels,signedGradients)
    svm = cv2.ml.SVM_create()
    svm=cv2.ml.SVM_load("C:\\Users\\wassaf\\Desktop\\CV\\meter_svm_model.yml")
    svmvec = svm.getSupportVectors()[0]
    rho = -svm.getDecisionFunction(0)[0]
    svmvec = np.append(svmvec, rho)
    hog1.setSVMDetector(svmvec)
    return hog1,svm
h = hog()