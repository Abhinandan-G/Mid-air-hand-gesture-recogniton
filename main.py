import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np


folderPath = "Tracking"

width,height = 1280,720
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

pathImages = os.listdir(folderPath)
print(pathImages)

buttonPressed = False
buttonCounter = 0
buttonDelay = 80

annotations = []
annotationNumber  = -1
annotationStart = False

gestureThreshold = 400
imageNumber = 0
hs,ws = 120,213


detector = HandDetector(detectionCon=0.8,maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFulImage = os.path.join(folderPath,pathImages[imageNumber])
    imageCurrent = cv2.imread(pathFulImage)

    hands, img = detector.findHands(img)
    #cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmlist = hand['lmList']
        indexFinger = lmlist[8][0],lmlist[8][1]


        # xval = int(np.interp(lmlist[8][0],[width//2,width],[0,width]))
        # yval = int(np.interp(lmlist[8][1], [150, height-150], [0, height]))
        # indexFinger = xval, yval

        if(cy<=gestureThreshold):
            if(fingers==[1,0,0,0,0]):
                #print("Thumb")
                if(imageNumber>0):
                    buttonPressed = True
                    imageNumber -= 1

            if (fingers == [0, 0, 0, 0, 1]):
                #print("Sundu viral")
                if(imageNumber< len(pathImages)-1):
                    buttonPressed = True
                    imageNumber += 1

        if (fingers == [0, 1, 1, 0, 0]):
            cv2.circle(imageCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if (fingers == [0, 1, 0, 0, 0]):
            # if(annotationStart is False):
            #     annotationStart = True
            #     annotationNumber +=1
            #     annotations.append([])


            cv2.circle(imageCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations.append(indexFinger)

        else:
            annotationStart = False

    if(buttonPressed):
        buttonCounter+=1
        if(buttonCounter>buttonDelay):
            buttonCounter=0
            buttonPressed=False
        #print(fingers)

    for i in range (len(annotations)):
        if(i!=0):
            cv2.line(imageCurrent,annotations[i-1],annotations[i],(0,0,200),12)

    imgSmall = cv2.resize(img,(ws,hs))
    h,w,_ = imageCurrent.shape
    imageCurrent[0:hs,0:ws] = imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imageCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break