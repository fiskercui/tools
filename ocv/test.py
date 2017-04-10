#coding=utf-8
import cv2 

img = cv2.imread(".\\texture\\texure.png") 
cv2.namedWindow("Image") 
# print img
cv2.imshow("Image", img) 

cv2.waitKey(0)
cv2.destroyAllWindows()