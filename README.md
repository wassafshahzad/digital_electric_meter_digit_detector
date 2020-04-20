# Introduction
As a part of my final year project for my bachelors degree,I took on the task to develop a digital meter reader using OpenvCV and TensorFlow.
The project has two parts an android app built using ionic and a desktop app developed using ElectronJs.

# Image Processing Part : 
There are two parts of this module as well.The first part was developed using openCV and second part was developed using tensorflow objectdetection API.

## LED Cropping Module:
The first part of the modules was used to crop the led containing the digits of units consumed to be passed to the object detection module.
We first binarize the image and then we isolate the contours having  width > height, we should call them LED'S canditate set. We isolate them on w > h as LED'S and rectangular shape.
Then from the candiate set we use HOG and a feature extarctor and SVM as classifier to get the LED which is passed to the object detection module.

## Object Detection Module:
The second part of the module was used to isolate and classify digits on the led to read the units consumed.
We train the model on GCP on a custom dataset.We user LabelImgpy to to annotate the date.
The model we used a RestNet with the default feature extractor.


# Desktop Application:
The application demo was developed using eldectronJs.
