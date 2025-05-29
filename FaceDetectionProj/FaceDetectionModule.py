import cv2
import mediapipe as mp
import time



class FaceDetector():
    def __init__(self , min_detection_confidence=0.5 , model_selection=0 ):
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection
        self.mpFaceDetction = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetction.FaceDetection()
    def findFaces(self,img,draw = True):



         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
         results = self.faceDetection.process(imgRGB)
         bboxes = []

         if results.detections:
            for id, detection in enumerate(results.detections):

                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                int(bboxC.width * iw), int(bboxC.height * ih)


                bboxes.append([bbox , detection.score])
                if draw:
                    self.fancyDraw(img , bbox)

                cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 255, 0), 2)
         return bboxes , img
    def fancyDraw(self , img , bbox , length = 30 , tk = 5 , rt = 1):
        x , y , w , h = bbox
        x1 , y1 = x+w , y+h
        cv2.rectangle(img, bbox, (255, 0, 255), rt)

        cv2.line(img,(x,y) , (x+length,y) , (0 , 255 , 0) , tk)
        cv2.line(img,(x,y) , (x,y+length) , (0 , 255 , 0) , tk)
        # Top Left (x , y)
        cv2.line(img, (x1, y), (x1 - length, y), (0, 255, 0), tk)
        cv2.line(img, (x1, y), (x1, y + length), (0, 255, 0), tk)
        # Top Right (x , y)
        cv2.line(img, (x, y1), (x + length, y1), (0, 255, 0), tk)
        cv2.line(img, (x, y1), (x, y1 - length), (0, 255, 0), tk)
        # Bottom Left
        cv2.line(img, (x1, y1), (x1 - length, y1), (0, 255, 0), tk)
        cv2.line(img, (x1, y1), (x1, y1 - length), (0, 255, 0), tk)
        #Bottom Right

        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()

    while True:
        success , img = cap.read()
        bboxes , img = detector.findFaces(img)
        cTime = time.time()
        print(bboxes)
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img , f'FPS: {int(fps)}' , (10,45) , cv2.FONT_HERSHEY_PLAIN, 2 , (255 ,0 , 255) , 2)
        cv2.imshow("Image: ",img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()