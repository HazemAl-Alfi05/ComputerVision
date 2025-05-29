#Import libraries
import cv2
import mediapipe as mp
import time
import math



class poseDetector():
    def __init__(self , mode = False , model_complexity = 1 , smooth_landmarks = True , enable_segmentation = False , min_detection_confidence = 0.5 , min_tracking_confidence = 0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.model_complexity,self.smooth_landmarks,self.enable_segmentation,self.min_detection_confidence,self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils # To drawing the landmarks and connections between them.


    def findPose(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)  # converting the image into RGB format.

        if self.results.pose_landmarks:  # checking the landmarks if there exist or not.
             if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)  # Drawing landmarks and the connections between them.
        return img


    def getPosition(self , img , draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id , lm in enumerate(self.results.pose_landmarks.landmark):
                h , w , c = img.shape
                #print(id , lm) # Getting information about the landmarks.
                cx , cy = int(lm.x * w),int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img ,(cx , cy) ,5,(255,0,255) , cv2.FILLED) # Drawing circle over every landmark.
        return self.lmList

    def getAngle(self , img , p1 , p2 , p3 , draw = True):
        x1 , y1 = self.lmList[p1][1:] # The slice part to ignore the id and print other info about landmark.
        x2 , y2 = self.lmList[p2][1:] # The slice part to ignore the id and print other info about landmark.
        x3 , y3 = self.lmList[p3][1:] # The slice part to ignore the id and print other info about landmark.
        angle = math.degrees(math.atan2(y3 - y2,x3-x2) - math.atan2(y1 - y2 , x1 - x2))

        if angle < 0:
            angle += 360
        if draw:
            cv2.line(img , (x1,y1) , (x2 , y2) , (255 , 0 , 0) , 3)
            cv2.line(img , (x2,y2) , (x3 , y3) , (255 , 0 , 0) , 3)
            cv2.circle(img, (x1 , y1), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1 , y1), 13, (0, 0, 255), 2)
            cv2.circle(img, (x2 , y2), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2 , y2), 13, (0, 0, 255), 2)
            cv2.circle(img, (x3 , y3), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3 , y3), 13, (0, 0, 255), 2)
            #cv2.putText(img , str(int(angle)) , (x2 - 50 , y2-50),cv2.FONT_HERSHEY_PLAIN , 1 , (255 , 0 , 255) , 2)
        return angle








def main():
    cap = cv2.VideoCapture(0)  # Video cam
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()  # Reading the image.
        img = detector.findPose(img)
        lmList = detector.getPosition(img,draw=False)
        print(lmList[9] , lmList[12])
        #cv2.circle(img, (lmList[9][1], lmList[9][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.
        #cv2.circle(img, (lmList[12][1], lmList[12][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.
        #cv2.circle(img, (lmList[0][1], lmList[0][2]), 10, (255, 0, 255), cv2.FILLED)  # Drawing circle over every landmark.

        cTime = time.time()  # Getting FPS
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (20, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        cv2.imshow("Image: ", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()