import cv2 
cap = cv2.VideoCapture("http://172.16.4.64:8080/shot.jpg")
if( cap.isOpened() ) :
    ret,img = cap.read()
    cv2.imshow("win",img)
    cv2.waitKey()
    