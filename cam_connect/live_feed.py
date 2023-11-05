import cv2 
from cvzone.HandTrackingModule import HandDetector 
from cvzone.ClassificationModule import Classifier
import numpy as np 
import math
import time

cap = cv2.VideoCapture(0) 
detector = HandDetector(maxHands=1) 
offset = 20
imgSize = 300
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


categorizer = Classifier("Model/keras_model.h5", "Model/labels.txt")

folder = r'C:\Users\18324\Desktop\sign-ify_local\sign-ify-1\cam_connect\Data\E'
counter = 0

while True:
    success, img = cap.read()

    imgOut = img.copy()
    hands, img = detector.findHands(img) 

    if hands:
        hand = hands[0] 
        x, y, w, h = hand['bbox']  

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset] 
        imgCropShape = imgCrop.shape 
        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = categorizer.getPrediction(imgWhite, draw = False)
            print(prediction, index) #see output real time

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = categorizer.getPrediction(imgWhite, draw = False)

        cv2.rectangle(imgOut, (x - offset, y - offset-50), (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOut, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOut, (x-offset, y-offset), (x + w+offset, y + h+offset), (255, 0, 255), 4)