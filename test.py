import cv2 
import numpy as np
from keras.models import load_model
import serial
import sys
import time


arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
signal_ready = "Ready..."
arduino.write(signal_ready.encode())
print ("Connection to Arduino...")

model = load_model("./model-008")
results_dict = {0:'without mask',1:'mask'}
frame_color = {0: (0,0,255), 1:(0,255,0)}
arduino_dict = {0: 'entrada negada', 1: 'entrada liberada'}

camera = cv2.VideoCapture(0) #device padrao
if not camera.isOpened():
    print("Error:  cannot open video")
    exit()


detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    (working, frame) = camera.read()
    rects = detector.detectMultiScale(frame,scaleFactor=1.1, minNeighbors=5, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)

    for (fX, fY, fW, fH) in rects: 
        roi = frame[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (180, 180))
        roi_v = roi/255.0
        roi_detc = np.reshape(roi_v,(1,180,180,3))
        roi_detc = np.vstack([roi_detc])
        result = model.predict(roi_detc)
          
        label = np.argmax(result,axis=1)[0]
                
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), frame_color[label], 2)
        cv2.putText(frame, results_dict[label], (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, frame_color[label], 2)
        data = arduino_dict[label]
                
    arduino.write(data.encode())
    cv2.imshow("LIVE", frame)

    key = cv2.waitKey(10)
    if key == 27: 
        break
            
camera.release()
cv2.destroyAllWindows()  
