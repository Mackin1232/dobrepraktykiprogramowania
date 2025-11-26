import numpy as np
import cv2
import requests

def nr_ppl(url):
    img = requests.get(url).content
    img = cv2.imdecode(np.frombuffer(img,np.uint8),-1)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    frame = cv2.resize(img,[640,480])
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
    boxes = np.array([[x,y,x+w,y+h] for (x,y,w,h) in boxes])
    return len(boxes)

print(nr_ppl("https://previews.123rf.com/images/gdolgikh/gdolgikh1504/gdolgikh150400087/38738606-group-of-happy-young-people-isolated-on-white-background.jpg"))