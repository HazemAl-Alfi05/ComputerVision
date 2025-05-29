# imports libraries
import cv2
import mediapipe as mp
import time
# Video cam
cap = cv2.VideoCapture(0)
pTime = 0
mpFaceDetction = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils    # object for drawing the face detection
faceDetection =mpFaceDetction.FaceDetection() # We skip the parameters because there initial declare in class (FaceDetector)

while True:
    success , img = cap.read()  # Reading the image.
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)  # Turn the image into RGB format.
    if results.detections:
        for id,detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih , iw , ic= img.shape   # variables to make the bounding box.
            bbox = int(bboxC.xmin *iw), int(bboxC.ymin * ih), \
                int(bboxC.width * iw) , int(bboxC.height * ih) # Making the bounding box.
            cv2.rectangle(img , bbox, (255,0,255) , 2)  # make a shape.
            # Make the percentage of detecting (Up to 100%).
            cv2.putText(img , f'{int(detection.score[0] * 100)}%' , (bbox[0], bbox[1] - 20) , cv2.FONT_HERSHEY_PLAIN ,  2, (0 ,255 ,0) , 2)
            
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    cv2.putText(img , f"FPS: {int(fps)}" , (20,40) , cv2.FONT_HERSHEY_PLAIN ,  1, (255 ,0 ,0) , 2)
    pTime = cTime
    #Making the fps to make sure that image detection time close to the real time.


    cv2.imshow("Image", img)
    cv2.waitKey(1)



