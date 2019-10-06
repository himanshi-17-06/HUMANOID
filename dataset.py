#!/usr/bin/env python
# coding: utf-8

# In[4]:
'''
    use comments wherver needed
    using socket for image transmission
    creating dataset

'''
import socket
import cv2
import numpy as np 

def generate_dataset(img, id, img_id):
    cv2.imwrite(r"C:\Users\user\Desktop\data\user."+str(id)+"."+str(img_id)+".jpg",img)
    #cv2.imshow(r"C:\Users\user\Desktop\data\user."+str(id)+"."+str(img_id)+".jpg",img)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    port = 80
    s.bind((IPAddr, port))
    s.listen(1)
    c, addr=s.accept()
    print ("Connection from: "+str(addr))
    #filename = input(str("Please enter the filename of file: "))
    file = open("user."+str(id)+"."+str(img_id)+".jpg",'rb')
    file_data = file.read(12288)  
    c.send(file_data)

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords =[]
    for(x,y,w,h) in features:
        cv2.rectangle(img, (x,y),(x+w,y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x,y,w,h]
        print(coords)
    return coords
# def recognize(img, clf, faceCascade):
#     color={"blue":(255,0,0),"red":(0,0,255),"green":(0,255,0),"white":(255,255,255)}
#     coords = draw_boundary(img, faceCascade, 1.1, 10, color["white"],"Face",clf)
#     return img
    
def detect(img, faceCascade,eyeCascade,noseCascade,mouthCascade,img_id):
    color={"blue":(255,0,0),"red":(0,0,255),"green":(0,255,0),"white":(255,255,255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['green'],"Face")
    if len(coords)==4:
        
        roi_img = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
        user_id = 1
        generate_dataset(roi_img,user_id,img_id)
#         coords = draw_boundary(roi_img, eyeCascade, 1.1, 14, color['red'],"Eyes")
#         coords = draw_boundary(roi_img, noseCascade, 1.1, 5, color['green'],"Nose")
#         coords = draw_boundary(roi_img, mouthCascade, 1.1, 20, color['white'],"Mouth")
    return img


# In[2]:


faceCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_eye.xml")
noseCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\Nariz.xml")
mouthCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\mouth.xml")
#clf = cv2.face.LBPHFaceRecognizer_create()
#clf.read("classifier.yml")
video_capture = cv2.VideoCapture(0)
img_id = 0
# while True:
_, img = video_capture.read()
img = detect(img, faceCascade, eyeCascade, noseCascade, mouthCascade,img_id)
   # img = recognize(img, clf, faceCascade)
cv2.imshow("face detection",img)
img_id += 1
if cv2.waitKey(1) & 0xFF == ord('q'):
    #break
    video_capture.release()
    cv2.destroyAllWindows()





