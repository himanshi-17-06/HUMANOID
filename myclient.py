import io
import socket
import struct
import cv2
import pickle

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Ipaddr = str(input("Enter ip: "))
client_socket.connect((Ipaddr,500))  # ADD IP HERE
def generate_dataset(img, id, img_id):
    cv2.imwrite(r"C:\Users\user\Desktop\data\user."+str(id)+"."+str(img_id)+".jpg",img)
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text,clf):
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords =[]
    for(x,y,w,h) in features:
        cv2.rectangle(img, (x,y),(x+w,y+h), color, 2)
        #id, acc = clf.predict(gray_img[y:y+h,x:x+w])
        id = client_socket.recv(1024)
        if (id==1):
            cv2.putText(img, "Himanshi-{}".format(acc), (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        if (id==2):
            cv2.putText(img, "Saloni-{}".format(acc), (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
    

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
faceCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\haarcascade_eye.xml")
noseCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\Nariz.xml")
mouthCascade = cv2.CascadeClassifier(r"C:\Users\user\Desktop\mouth.xml")
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.yml")

# Make a file-like object out of the connection
    # Start a preview and let the camera warm up for 2 seconds
cap=cv2.VideoCapture(0)
    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)

while True:
    ret,img=cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pickle.dumps(gray)
    client_socket.sendall(struct.pack("L", len(data)) + data)
    
    
    img = recognize(frame, clf, faceCascade)
    cv2.imshow('img',img)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break

client_socket.close()
cap.release()
cv2.destroyAllWindows()

