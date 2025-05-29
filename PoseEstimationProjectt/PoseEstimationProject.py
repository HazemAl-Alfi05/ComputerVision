import cv2
import mediapipe as mp
import time
import PoseEstimationModule as pem

cap = cv2.VideoCapture(0)  # Video cam
pTime = 0
detector = pem.poseDetector()
while True:
    success, img = cap.read()  # Reading the image.
    img = detector.findPose(img)
    lmList = detector.getPosition(img,draw=False)
    if len(lmList) != 0:
        print(lmList[9] , lmList[12])
        cv2.circle(img, (lmList[9][1], lmList[9][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.
        cv2.circle(img, (lmList[12][1], lmList[12][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.
        cv2.circle(img, (lmList[0][1], lmList[0][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.

    cTime = time.time()  # Getting FPS
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cv2.imshow("Image: ", img)
    cv2.waitKey(1)