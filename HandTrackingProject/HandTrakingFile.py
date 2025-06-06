import cv2
import mediapipe as mp
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
pTime = 0

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                ##### If I want to get the id of all landmarks
                #print(id, cx, cy) , if I want the id for all landmarks

                ##### If I want to get the id of specific landmark
                #if id == 8:

                ##### If I want to draw a circle on specific landmark
                #cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f"FPS: {int(fps)}",(20,45),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),2)

    cv2.imshow('Video', img)
    cv2.waitKey(1)