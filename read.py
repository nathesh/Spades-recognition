import cv2 
cap = cv2.VideoCapture(2)
while(True):
	ret,img = cap.read()
	cv2.imshow('frame',img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
 