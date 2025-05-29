import cv2
import mediapipe as mp
import time
import ModuleofHandTraking as htm

pTime = 0 #For fps.

##########Cam position##########
cap = cv2.VideoCapture(0)
wCam , hCam = 640 , 480
cap.set(3,wCam)
cap.set(4,hCam)
##########Cam position##########

detector = htm.HandDetector()
Rtip = [4 , 8 , 12 , 16 , 20]
Ltip = [4 , 8 , 12 , 16 , 20]


while True:
    success , Vid = cap.read()
    Video = detector.findHands(Vid)
    lmList = detector.findPosition(Vid , draw = False)

    ##### Detect fingers except the tum finger rather they open or closed #####
    Rfingers = []
    Lfingers = []

    if len(lmList) !=0:

        ##### Detect if the thump finger is close or open #####

        if lmList[Rtip[0]][1] > lmList[Rtip[0]-1][1]:
            Rfingers.append(1)
        else:
            Rfingers.append(0)
        ##### Detect if the thump finger is close or open #####

        ##### Detect Right fingers except the thump finger rather they open or closed #####
        for x in range(1,5):
           if lmList[Rtip[x]][2] < lmList[Rtip[x]-2][2]:
              Rfingers.append(1)
           else:
              Rfingers.append(0)
        ##### Detect Right fingers except the thump finger rather they open or closed #####

        ##### Detect if the Left thump finger is close or open #####
        if lmList[Rtip[0]][1] < lmList[Rtip[0] - 1][1]:
              Lfingers.append(1)
        else:
              Lfingers.append(0)
        ##### Detect if the Left thump finger is close or open #####

        ##### Detect Left fingers except the thump finger rather they open or closed #####
        for x in range(1, 5):
            if lmList[Rtip[x]][2] < lmList[Rtip[x] - 2][2]:
              Lfingers.append(1)
            else:
              Lfingers.append(0)
              ##### Detect Left fingers except the thump finger rather they open or closed #####

        totalRFingers = Rfingers.count(1)
        totalLFingers = Lfingers.count(1)
        #print(totalRFingers)

        cv2.rectangle(Vid , (20,255) , (170,425) , (0,255,0) , cv2.FILLED)
        cv2.putText(Vid , str(int(totalLFingers)) , (45,390) , cv2.FONT_HERSHEY_PLAIN , 10 , (255,0,0) , 25)
        # If I want to calc for the left hand just write on putText totalLFingers.

    ##########FPS##########
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(Vid , f"FPS: {int(fps)}" , (20 , 45) , cv2.FONT_HERSHEY_PLAIN , 1 , (255,0,255) , 2)
    ##########FPS##########

    cv2.imshow("Image: " , Vid)
    cv2.waitKey(1)