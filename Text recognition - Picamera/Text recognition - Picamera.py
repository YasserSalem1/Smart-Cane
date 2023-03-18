import cv2
from pytesseract import pytesseract
import pyttsx3
from pytesseract import Output
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 

pytesseract.tesseract_cmd = "/usr/bin/tesseract"
engine = pyttsx3.init()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    image_data = pytesseract.image_to_data(image,output_type=Output.DICT)
    cv2.imshow("Frame", image)

    for i,word in enumerate(image_data['text']):
        
            if word != "":
                print(word)
                engine.say(word)
                engine.runAndWait()

    key = cv2.waitKey(1) & 0xFF
    raw_capture.truncate(0)