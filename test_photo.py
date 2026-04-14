"""
Prend une photo à partir de la caméra thermique
"""
import cv2

cam = cv2.VideoCapture(2) #index à changer en fonction de la caméra à utiliser

while True:
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
	k = cv2.waitKey(1)
	if k != -1:
		break
cv2.imwrite('/home/secours/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()
