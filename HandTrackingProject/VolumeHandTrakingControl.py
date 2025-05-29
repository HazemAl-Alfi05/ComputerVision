import cv2
import mediapipe as mp
import time
import ModuleofHandTraking as ht
import math
import numpy as np
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume



cap = cv2.VideoCapture(0)
#### Parameters for our camera size ####
cW , cH = 640 , 480
cap.set(3,cW)
cap.set(4,cH)
#### Parameters for our camera size ####

pTime = 0 # To calc FPS.

detector = ht.HandDetector() # Object to use HandDetector class

######### Access the volume of the device ########
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_ , CLSCTX_ALL , None)
volume = cast(interface , POINTER(IAudioEndpointVolume))
######### Access the volume of the device ########



volume_range = volume.GetVolumeRange() # The range of the volume. (min: -65.25 - max: 0.0)


minVol = volume_range[0] # Min volume.
maxVol = volume_range[1] # Max volume.
vol = 0
volBAR = 400
volPer = 0




while True:
    success , Vid = cap.read()
    video = detector.findHands(Vid) # Drawing the hand landmarks and connection between them.
    lmList = detector.findPosition(video , draw = False) # Getting landmarks positions
    if len(lmList) != 0:
     # print(lmList[4] , lmList[8])

      x1 , y1 = lmList[4][1] , lmList[4][2] # Center of First circle.
      x2 , y2 = lmList[8][1] , lmList[8][2] # Center of Second circle.
      clx , cly = (x1+x2)//2 , (y1+y2)//2 # Center of line.
      cv2.circle(Vid , (x1,y1) , 10 , (0,255,0) , cv2.FILLED) # Circle 1
      cv2.circle(Vid , (x2,y2) , 10 , (0,255,0) , cv2.FILLED) # Circle 2
      cv2.line(Vid , (x1,y1),(x2,y2), (0,255,0),2) # Line between circles.
      cv2.circle(Vid , (clx,cly) , 10 , (0,255,0) , cv2.FILLED) # Circle in the center of line.


      length = math.hypot(x2-x2 , y2-y1) # The length of line.
      # Hand Range --> 20 - 210
      # Volume Range --> -65 - 0


      ######## Convert (Hand range numbers) to (Volume range numbers) ########
      vol = np.interp(length , [20 , 210] , [minVol , maxVol])
      ######## Convert (Hand range numbers) to (Volume range numbers) ########
      volBAR = np.interp(length, [20, 210], [400, 150])
      volPer = np.interp(length , [20,210] , [0 , 100])
      volume.SetMasterVolumeLevel(vol, None)  # Set the state of volume.


      if length < 20:
          cv2.circle(Vid, (clx, cly), 10, (0, 0, 255), cv2.FILLED)  # Min length of the line.
          cv2.putText(Vid , "Muted" , (50,70) , cv2.FONT_HERSHEY_PLAIN , 1 , (0,0,0) , 2)


    # Calculate the FPS #
    cTime = time.time()
    fps = 1  / (cTime - pTime)
    pTime = cTime
    cv2.putText(Vid , f'FPS: {int(fps)}' , (20 ,45) , cv2.FONT_HERSHEY_PLAIN , 1 , (0,0,255) , 2)
    # Calculate the FPS #

    ######## Rectangle of the volume state ########
    cv2.rectangle(Vid , (50,150) , (85,400) , (0,255,0) , 3)
    cv2.rectangle(Vid , (50,int(volBAR)) , (85,400) , (0,255,0) , cv2.FILLED)
    cv2.putText(Vid,f'{int(volPer)}%' , (40,450) , cv2.FONT_HERSHEY_PLAIN , 1 , (0,0,0) , 2)
    ######## Rectangle of the volume state ########


    cv2.imshow("Image: " , Vid)
    cv2.waitKey(1)

