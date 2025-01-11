import cv2

cap = cv2.VideoCapture(0)  # 0 is usually the default camera
if not cap.isOpened():
    print("Camera not accessible")
else:
    print("Camera is accessible")
cap.release()