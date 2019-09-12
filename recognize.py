#!/usr/bin/env python
# coding: utf-8

# In[5]:
import io
import socket
import struct
import pickle
import cv2

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(),500))  # ADD IP HERE
server_socket.listen(0)
conn,address = server_socket.accept()


def generate_dataset(img, id, img_id):
    cv2.imwrite(r"C:\Users\user\Desktop\data\user."+str(id)+"."+str(img_id)+".jpg",img)
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text,clf):
    #gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      
    features = classifier.detectMultiScale(img, scaleFactor, minNeighbors)
    coords =[]
    for(x,y,w,h) in features:
        cv2.rectangle(img, (x,y),(x+w,y+h), color, 2)
        id, acc = clf.predict(img[y:y+h,x:x+w])
        if (id==1):
            cv2.putText(img, "Saloni-{}".format(acc), (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        if (id==2):
            cv2.putText(img, "Himanshi-{}".format(acc), (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        conn.send(str(id).encode('utf-8'))

        coords = [x,y,w,h]
    return coords,img
def recognize(img, clf, faceCascade):
    color={"blue":(255,0,0),"red":(0,0,255),"green":(0,255,0),"white":(255,255,255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color["white"],"Face",clf)
    return img
    
def detect(img, faceCascade,eyeCascade,noseCascade,mouthCascade,img_id):
    color={"blue":(255,0,0),"red":(0,0,255),"green":(0,255,0),"white":(255,255,255)}
    coords,img = draw_boundary(img, faceCascade, 1.1, 10, color['blue'],"Face")
    if len(coords)==4:
        
        roi_img = img[coords[1]:coords[1]+coords[3],coords[0]:coords[0]+coords[2]]
        user_id = 1
        generate_dataset(roi_img,user_id,img_id)
#         coords = draw_boundary(roi_img, eyeCascade, 1.1, 14, color['red'],"Eyes")
#         coords = draw_boundary(roi_img, noseCascade, 1.1, 5, color['green'],"Nose")
#         coords = draw_boundary(roi_img, mouthCascade, 1.1, 20, color['white'],"Mouth")
    return img


# In[6]:


faceCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_eye.xml")
noseCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\Nariz.xml")
mouthCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\mouth.xml")
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.yml")
data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    #print(frame.size)
    img = recognize(frame, clf, faceCascade)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

server_socket.close()
# video_capture = cv2.VideoCapture(0)
# img_id = 0
# while True:
#     _, img = video_capture.read()
#     #img = detect(img, faceCascade, eyeCascade, noseCascade, mouthCascade,img_id)
#     img = recognize(img, clf, faceCascade)
#     cv2.imshow("face detection",img)
#     img_id += 1
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# video_capture.release()
# cv2.destroyAllWindows()


# In[ ]:




