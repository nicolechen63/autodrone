import cv2 as cv

CAMERA_HEIGHT = 720
CAMERA_WIDTH = 1920

cap = cv.VideoCapture(1)

cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)

while (True):
    ret, frame = cap.read()

    cv.imshow('cam', frame)

    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
