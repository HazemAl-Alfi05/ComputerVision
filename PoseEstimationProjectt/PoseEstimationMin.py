#Import libraries
import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils # To drawing the landmarks and connections between them.

cap = cv2.VideoCapture(0) # Video cam
pTime = 0

while True:
    success , img = cap.read() # Reading the image.

    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB) # converting the image into RGB format.

    if results.pose_landmarks: # checking the landmarks if there exist or not.
        mpDraw.draw_landmarks(img , results.pose_landmarks , mpPose.POSE_CONNECTIONS) # Drawing landmarks and the connections between them.
        for id , lm in enumerate(results.pose_landmarks.landmark):
            h , w , c = img.shape
            print(id , lm) # Getting information about the landmarks.
            cx , cy = int(lm.x * w),int(lm.y * h)
            cv2.circle(img ,(cx , cy) ,5,(255,0,255) , cv2.FILLED) # Drawing circle over every landmark.

    cTime = time.time() # Getting FPS to know if detect clause to the real time or not.
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img , f"FPS: {int(fps)}" , (20 , 45) , cv2.FONT_HERSHEY_PLAIN , 2 , (255,0,255) , 2)

    cv2.imshow("Image: ",img)
    cv2.waitKey(1)

