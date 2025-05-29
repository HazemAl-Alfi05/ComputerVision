import cv2
import mediapipe as mp
import numpy as np
import time
import PoseEstimationModule as pm

cap = cv2.VideoCapture(r"C:\Users\DRT\Downloads\4259068-uhd_3840_2160_25fps.mp4")
detector = pm.poseDetector()
count = 0
dir = 0


pTime = 0 # to calc fps
while True:
    success , Vid = cap.read()
    Vid = cv2.resize(Vid , (1280 , 720))
    Video =  detector.findPose(Vid , draw = False)
    lmList = detector.getPosition(Vid , draw = False)
    if len(lmList) != 0:
        # Right arm.
       # angle  = detector.getAngle(Vid , 12 , 14 , 16)
        angle = detector.getAngle(Vid , 11 , 13 , 15 , draw = True)

        per = np.interp(angle , (210 , 310),(0,100))
        bar = np.interp(angle , (220 , 310) , (650 , 100))

        # Check for the dumbbell curls.
        color = (255,0,255)
        if per == 100:
            color = (0,255,0)
            if dir == 0:
                count+=0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count+=0.5
                dir = 0

        print(count)
        # Drawing counter for curling.


        # Drawing bar to check if the curl is done.
        cv2.rectangle(Vid, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(Vid, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(Vid , f"{int(per)} %" , (1100,75) , cv2.FONT_HERSHEY_PLAIN , 4 , color , 4)

        cv2.rectangle(Vid, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(Vid, f"{int(count)}", (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(Vid , f"FPS: {int(fps)}" , (20,45) , cv2.FONT_HERSHEY_PLAIN , 1 , (255,0,255) , 2)


    cv2.imshow("Image: " , Vid)
    cv2.waitKey(1)